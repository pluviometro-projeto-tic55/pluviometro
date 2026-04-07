import { useSocketEvent } from "../useSocketEvent";

export function useWeatherUpdates(stationId, setWeatherData) {
  const eventName = stationId ? `update_weather_${stationId}` : null;

  useSocketEvent(eventName, setWeatherData);
}
