export function transformForecastData(backendData) {
  if (!backendData || !backendData.hourly_forecast) return null;

  const transformed = {};

  backendData.hourly_forecast.forEach((dayItem) => {
    // Group by date key (e.g., "2026-01-28")
    transformed[dayItem.date] = dayItem.hours.map((hourItem) => {
      const dateObj = new Date(hourItem.timestamp);
      // Format X-Axis time label (e.g., "14:00")
      const timeLabel = dateObj.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
      });

      return {
        ...hourItem,
        time: timeLabel, // Required by the Chart component
      };
    });
  });

  return transformed;
}