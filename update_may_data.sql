USE weatherdb;

-- Limpar dados antigos (antes de maio)
DELETE FROM raspdata WHERE YEAR(Timestamp) < 2026 OR (YEAR(Timestamp) = 2026 AND MONTH(Timestamp) < 5);
DELETE FROM forecast WHERE YEAR(TIMESTAMP) < 2026 OR (YEAR(TIMESTAMP) = 2026 AND MONTH(TIMESTAMP) < 5);

-- Inserir dados de maio/2026 na tabela RaspData
INSERT INTO raspdata (rcID, Timestamp, Temp, Humidity, Pressure, Wind_speed, Pluv, Lux) VALUES
(1, '2026-05-25 14:30:00', 27.5, 65, 1013.2, 8, 0, 45000),
(1, '2026-05-25 15:00:00', 28.1, 62, 1013.5, 7, 0, 48000),
(1, '2026-05-25 15:30:00', 28.8, 60, 1013.8, 6, 0, 52000),
(1, '2026-05-26 10:00:00', 25.2, 70, 1012.5, 9, 2, 42000),
(1, '2026-05-27 09:00:00', 24.8, 72, 1011.9, 10, 5, 38000),
(1, '2026-05-28 11:00:00', 26.3, 68, 1012.8, 8, 1, 46000);

-- Inserir dados de previsão diária para maio
INSERT INTO forecast (rcID, TIMESTAMP, c_Temp, c_Humidity, c_Pressure, c_Wind_speed, c_Pluv, c_Lux, Temp_min, Temp_max, Feels_like, General) VALUES
(1, '2026-05-25', 27.5, 65, 1013.2, 8, 0, 45000, 22, 29, 26, 'Nuvens'),
(1, '2026-05-26', 25.2, 70, 1012.5, 9, 2, 42000, 20, 26, 24, 'Chuva'),
(1, '2026-05-27', 24.8, 72, 1011.9, 10, 5, 38000, 19, 25, 23, 'Chuva'),
(1, '2026-05-28', 26.3, 68, 1012.8, 8, 1, 46000, 21, 27, 25, 'Nuvens');
