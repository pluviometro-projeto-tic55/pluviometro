BEGIN
    UPDATE RaspClient rc
    LEFT JOIN (
        -- Subconsulta para pegar a última leitura de cada rcID
        SELECT rd1.rcID, rd1.temp, rd1.humidity, rd1.pressure, rd1.lux, rd1.timestamp
        FROM RaspData rd1
        WHERE rd1.timestamp = (SELECT MAX(rd2.timestamp) 
                              FROM RaspData rd2 
                              WHERE rd2.rcID = rd1.rcID)
    ) last_rd ON rc.rcID = last_rd.rcID
    SET rc.Status = CASE
        -- Nunca enviou dados ou o último dado tem mais de 10 minutos
        WHEN last_rd.timestamp IS NULL 
             OR last_rd.timestamp < NOW() - INTERVAL 10 MINUTE THEN 'Offline - Verifique se a estação está ligada!'
        
        -- Ambos sensores com problema
        WHEN (last_rd.temp IS NULL OR last_rd.humidity IS NULL OR last_rd.pressure IS NULL)
        AND last_rd.lux IS NULL THEN 'Falha em ambos sensores - (Temperatura, Umidade, Pressão e Luminosidade)'

        -- Sensor BME280 retornando NULL (Erro no sensor)
        WHEN last_rd.temp IS NULL 
             OR last_rd.humidity IS NULL 
             OR last_rd.pressure IS NULL THEN 'Falha no Sensor BME280 (Temperatura, Umidade e Pressão)'
        
        -- Sensor de Luminosidade retornando NULL
        WHEN last_rd.lux IS NULL THEN 'Falha no Sensor de Luminosidade'
        
        -- Tudo certo
        ELSE 'Online'
    END;
END
