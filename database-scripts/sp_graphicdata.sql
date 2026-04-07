BEGIN

IF p_variable = 'temp' THEN

    SELECT
        DATE(timestamp) AS day_date,
        HOUR(timestamp) AS hour_day,
        ROUND(AVG(temp), 2) AS avghour_temp
    FROM RaspData
    WHERE rcID = p_rcID  
      AND timestamp >= p_data_ini
      AND timestamp < (p_data_fim + INTERVAL 1 DAY)
    GROUP BY DATE(timestamp),HOUR(timestamp)
    ORDER BY day_date, hour_day;

ELSEIF p_variable = 'humidity' THEN

    SELECT
        DATE(timestamp) AS day_date,
        HOUR(timestamp) AS hour_day,
        ROUND(AVG(humidity), 2) AS avghour_humidity
    FROM RaspData
    WHERE rcID = p_rcID  
      AND timestamp >= p_data_ini
      AND timestamp < (p_data_fim + INTERVAL 1 DAY)
    GROUP BY DATE(timestamp),HOUR(timestamp)
    ORDER BY day_date, hour_day;
    
ELSEIF p_variable = 'pressure' THEN

    SELECT
        DATE(timestamp) AS day_date,
        HOUR(timestamp) AS hour_day,
        ROUND(AVG(pressure), 2) AS avghour_pressure
    FROM RaspData
    WHERE rcID = p_rcID  
      AND timestamp >= p_data_ini
      AND timestamp < (p_data_fim + INTERVAL 1 DAY)
    GROUP BY DATE(timestamp),HOUR(timestamp)
    ORDER BY day_date, hour_day;
    

ELSEIF p_variable = 'wind_speed' THEN

    SELECT
        DATE(timestamp) AS day_date,
        HOUR(timestamp) AS hour_day,
        ROUND(AVG(wind_speed), 2) AS avghour_wind_speed
    FROM RaspData
    WHERE rcID = p_rcID  
      AND timestamp >= p_data_ini
      AND timestamp < (p_data_fim + INTERVAL 1 DAY)
    GROUP BY DATE(timestamp),HOUR(timestamp)
    ORDER BY day_date, hour_day;
    
END IF;

END
