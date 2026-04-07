import { useState, useEffect } from "react";
import { useApi } from "../useAPI";
import { useSocketEvent } from "../useSocketEvent";
import { notify } from "../../services/notify";

export function useForecastData(stationId) {
  const [data, setData] = useState(null);
  const { request, loading, error } = useApi();

  // 1. HTTP Request (Immediate Load)
  useEffect(() => {
    if (!stationId) return;

    // Reset data or keep previous data depending on preference. 
    // Setting to null forces skeleton loading on station switch.
    setData(null); 

    request({
      method: "get",
      url: `/api/stations/${stationId}/forecast`,
    })
      .then((response) => {
        setData(response.data);
      })
      .catch(() => {
        notify.error("Erro ao carregar dados da previsão.");
      });
  }, [stationId, request]);

  // 2. Socket Listener (Real-time Updates)
  // This replaces the need for useForecastUpdates in the component
  const eventName = stationId ? `update_forecast_${stationId}` : null;
  
  useSocketEvent(eventName, (newData) => {
    // When socket sends data, update the state
    setData(newData);
  });

  return { data, loading, error };
}