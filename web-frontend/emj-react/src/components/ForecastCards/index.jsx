import { useMemo } from "react";
import BaseCard from "../UI/BaseCard";
import { getFormattedDate } from "../../utils/dateUtils";
import { Cloud, Droplets, Thermometer } from "lucide-react";
import PropTypes from "prop-types";
import Skeleton from "react-loading-skeleton";
import "./style.css";

function ForecastCards({ externalData, loading }) {
  const forecast = useMemo(() => {
    if (!externalData?.forecast_4days || externalData.forecast_4days.length === 0) {
      return [];
    }
    return externalData.forecast_4days;
  }, [externalData]);

  if (loading) {
    return (
      <BaseCard>
        <div className="forecast-container">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="forecast-card-skeleton">
              <Skeleton height={20} />
              <Skeleton height={40} />
              <Skeleton height={20} />
            </div>
          ))}
        </div>
      </BaseCard>
    );
  }

  if (!forecast || forecast.length === 0) {
    return (
      <BaseCard>
        <div className="forecast-empty">
          <p>Dados de previsão não disponíveis</p>
        </div>
      </BaseCard>
    );
  }

  return (
    <BaseCard>
      <div className="forecast-header">
        <h3 className="forecast-title">Previsão de 4 Dias</h3>
      </div>
      <div className="forecast-container">
        {forecast.map((day, index) => (
          <div key={index} className="forecast-card">
            <div className="forecast-date">
              {day.date && getFormattedDate(day.date).shortDate}
            </div>

            <div className="forecast-temps">
              <div className="temp-item max">
                <Thermometer size={16} color="var(--text-red)" />
                <span className="temp-label">Máx</span>
                <span className="temp-value">{Math.round(day.max_temp)}°</span>
              </div>
              <div className="temp-item min">
                <Thermometer size={16} color="var(--text-blue)" />
                <span className="temp-label">Mín</span>
                <span className="temp-value">{Math.round(day.min_temp)}°</span>
              </div>
            </div>

            <div className="forecast-condition">
              <div className="condition-item">
                <Droplets size={16} />
                <span>{day.rain_chance}%</span>
              </div>
              <div className="condition-text">
                {day.condition || "Sem dados"}
              </div>
            </div>
          </div>
        ))}
      </div>
    </BaseCard>
  );
}

ForecastCards.propTypes = {
  externalData: PropTypes.shape({
    forecast_4days: PropTypes.arrayOf(
      PropTypes.shape({
        date: PropTypes.string,
        max_temp: PropTypes.number,
        min_temp: PropTypes.number,
        rain_chance: PropTypes.number,
        condition: PropTypes.string,
      })
    ),
  }),
  loading: PropTypes.bool,
};

export default ForecastCards;
