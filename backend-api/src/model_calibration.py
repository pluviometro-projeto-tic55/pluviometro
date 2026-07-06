"""
Model Calibration Module - VAR Model Validation Framework
Provides comprehensive backtesting, metrics calculation, and lag optimization
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.tsa.api import VAR
from src.var_data import prepare_var_data


def calculate_metrics(y_true, y_pred, metric_names=None):
    """
    Calculate RMSE, MAE, MAPE for each variable
    
    Args:
        y_true: DataFrame with true values
        y_pred: DataFrame with predicted values  
        metric_names: List of metric names to calculate
        
    Returns:
        dict with metrics per variable
    """
    if metric_names is None:
        metric_names = ['rmse', 'mae', 'mape']
    
    metrics = {}
    
    # Convert Index to list to avoid ambiguity
    columns = list(y_true.columns)
    
    for col in columns:
        col_true = y_true[col].values
        col_pred = y_pred[col].values
        
        # Filter NaN values
        valid_idx = ~(np.isnan(col_true) | np.isnan(col_pred))
        col_true_clean = col_true[valid_idx]
        col_pred_clean = col_pred[valid_idx]
        
        if len(col_true_clean) == 0:
            metrics[col] = {m: np.nan for m in metric_names}
            continue
        
        col_metrics = {}
        
        if 'rmse' in metric_names:
            col_metrics['rmse'] = np.sqrt(mean_squared_error(col_true_clean, col_pred_clean))
        
        if 'mae' in metric_names:
            col_metrics['mae'] = mean_absolute_error(col_true_clean, col_pred_clean)
        
        if 'mape' in metric_names:
            # MAPE = mean(|true - pred| / |true|) * 100
            # Avoid division by zero
            with np.errstate(divide='ignore', invalid='ignore'):
                mape_values = np.abs((col_true_clean - col_pred_clean) / np.abs(col_true_clean)) * 100
                mape_values = mape_values[np.isfinite(mape_values)]
                if len(mape_values) > 0:
                    col_metrics['mape'] = np.mean(mape_values)
                else:
                    col_metrics['mape'] = np.nan
        
        metrics[col] = col_metrics
    
    return metrics


def backtest_var_model(rc_id, train_days=180, test_days=7):
    """
    Backtest VAR model on historical data
    
    Args:
        rc_id: Station ID
        train_days: Days to use for training
        test_days: Days to use for testing
        
    Returns:
        dict with backtest results and metrics
    """
    try:
        # Prepare data
        result = prepare_var_data(rc_id, train_days + test_days)
        
        if result['status'] != 'success':
            return {'status': 'error', 'message': result.get('message', 'Data preparation failed')}
        
        df = result['data']
        
        if len(df) < train_days + test_days:
            return {'status': 'error', 'message': 'Insufficient data for backtest'}
        
        # Split train/test
        n_train = len(df) - test_days
        train_data = df.iloc[:n_train]
        test_data = df.iloc[n_train:]
        
        # Train VAR model
        model = VAR(train_data)
        var_fit = model.fit(maxlags=50, ic='aic')
        
        # Make predictions
        lag_order = var_fit.k_ar
        predictions = var_fit.forecast(train_data.values[-lag_order:], steps=len(test_data))
        
        # Create prediction DataFrame
        pred_df = pd.DataFrame(predictions, columns=train_data.columns, index=test_data.index)
        
        # Calculate metrics
        metrics = calculate_metrics(test_data, pred_df)
        
        return {
            'status': 'success',
            'lag_order': lag_order,
            'train_size': len(train_data),
            'test_size': len(test_data),
            'metrics': metrics
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def find_optimal_lags(rc_id, train_days=180, max_lags=72):
    """
    Find optimal lag order using AIC/BIC
    
    Args:
        rc_id: Station ID
        train_days: Days to use for training
        max_lags: Maximum lags to test
        
    Returns:
        dict with optimal lag recommendations
    """
    try:
        result = prepare_var_data(rc_id, train_days)
        
        if result['status'] != 'success':
            return {'status': 'error', 'message': result.get('message', 'Data preparation failed')}
        
        df = result['data']
        
        model = VAR(df)
        lag_order = model.select_order(maxlags=max_lags)
        
        return {
            'status': 'success',
            'aic': lag_order.aic,
            'bic': lag_order.bic,
            'fpe': lag_order.fpe,
            'hq': lag_order.hq,
            'recommendation': max(lag_order.aic, lag_order.bic)
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def print_calibration_report(rc_id):
    """
    Print comprehensive calibration report
    
    Args:
        rc_id: Station ID
    """
    print(f"\n{'='*60}")
    print(f"VAR Model Calibration Report - Station {rc_id}")
    print(f"{'='*60}\n")
    
    # 7-day backtest
    print("7-DAY BACKTEST")
    print("-" * 60)
    result_7 = backtest_var_model(rc_id, train_days=180, test_days=7)
    
    if result_7['status'] == 'success':
        print(f"Lag Order: {result_7['lag_order']}")
        print(f"Train Size: {result_7['train_size']} | Test Size: {result_7['test_size']}")
        print("\nMetrics by Variable:")
        for var, metrics in result_7['metrics'].items():
            print(f"  {var}:")
            for metric, value in metrics.items():
                if not np.isnan(value):
                    print(f"    {metric.upper()}: {value:.4f}")
    else:
        print(f"Error: {result_7['message']}")
    
    # 14-day backtest
    print("\n\n14-DAY BACKTEST")
    print("-" * 60)
    result_14 = backtest_var_model(rc_id, train_days=180, test_days=14)
    
    if result_14['status'] == 'success':
        print(f"Lag Order: {result_14['lag_order']}")
        print(f"Train Size: {result_14['train_size']} | Test Size: {result_14['test_size']}")
        print("\nMetrics by Variable:")
        for var, metrics in result_14['metrics'].items():
            print(f"  {var}:")
            for metric, value in metrics.items():
                if not np.isnan(value):
                    print(f"    {metric.upper()}: {value:.4f}")
    else:
        print(f"Error: {result_14['message']}")
    
    # Optimal lags
    print("\n\nOPTIMAL LAG ANALYSIS")
    print("-" * 60)
    result_lags = find_optimal_lags(rc_id, train_days=180, max_lags=72)
    
    if result_lags['status'] == 'success':
        print(f"AIC Recommendation: {result_lags['aic']} lags")
        print(f"BIC Recommendation: {result_lags['bic']} lags")
        print(f"FPE Recommendation: {result_lags['fpe']} lags")
        print(f"HQ Recommendation: {result_lags['hq']} lags")
    else:
        print(f"Error: {result_lags['message']}")
    
    print(f"\n{'='*60}\n")
