import { useSocketEvent } from "../useSocketEvent";

export function useForecastUpdates(stationId, setForecastData) {
  const eventName = stationId ? `update_forecast_${stationId}` : null;

  useSocketEvent(eventName, setForecastData);
}
