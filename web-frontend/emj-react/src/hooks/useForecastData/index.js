import { useState, useEffect } from "react";
import { useApi } from "../useAPI";
import { useSocketEvent } from "../useSocketEvent";
import { notify } from "../../services/notify";

function normalizeForecastPayload(payload) {
  if (!payload || typeof payload !== "object") {
    return null;
  }

  if (Array.isArray(payload.daily_summary)) {
    return payload;
  }

  if (Array.isArray(payload.forecast_4days)) {
    return {
      daily_summary: payload.forecast_4days.map((item) => ({
        date: item.date,
        max_temp: item.max_temp,
        min_temp: item.min_temp,
        heat_index: item.avg_temp,
        avg_wind_speed: 0,
        cloudiness: 0,
      })),
    };
  }

  return null;
}

export function useForecastData(stationId) {
  const [data, setData] = useState(null);
  const { request, loading, error } = useApi();

  // 1. HTTP Request (Immediate Load)
  useEffect(() => {
    if (!stationId) return;

    // Reset data or keep previous data depending on preference. 
    // Setting to null forces skeleton loading on station switch.
    setData(null); 

    const fetchForecast = () => request({
      method: "get",
      url: `/api/stations/${stationId}/forecast`,
    })
      .then((response) => {
        setData(normalizeForecastPayload(response.data));
      })
      .catch(() => {
        notify.error("Erro ao carregar dados da previsão.");
      });

    fetchForecast();

    // Fallback para evitar previsao travada quando o socket fica indisponivel.
    const interval = setInterval(fetchForecast, 300000);

    return () => clearInterval(interval);
  }, [stationId, request]);

  // 2. Socket Listener (Real-time Updates)
  // This replaces the need for useForecastUpdates in the component
  const eventName = stationId ? `update_forecast_${stationId}` : null;
  
  useSocketEvent(eventName, (newData) => {
    setData(normalizeForecastPayload(newData));
  });

  return { data, loading, error };
}