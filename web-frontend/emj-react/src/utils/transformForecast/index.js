export function transformForecastData(backendData) {
  if (!backendData || !backendData.daily_summary || !Array.isArray(backendData.daily_summary)) return {};

  const transformed = {};
  const today = new Date().toISOString().split('T')[0];

  backendData.daily_summary
    .filter(day => day.date >= today)
    .slice(0, 4)
    .forEach((dayItem) => {
      const min = dayItem.min_temp;
      const max = dayItem.max_temp;
      const hours = [];

      // Criamos 8 pontos no dia (de 3 em 3 horas) para simular a curva
      for (let i = 0; i < 8; i++) {
        const hour = i * 3;
        // Fórmula simples para criar uma curva (senoide) entre a min e a max
        const val = min + (max - min) * (Math.sin((i / 8) * Math.PI) * 0.5 + 0.5);
        
        hours.push({
          time: `${hour.toString().padStart(2, '0')}:00`,
          temperature: Math.round(val),
          heat_index: dayItem.heat_index,
          wind_speed: dayItem.avg_wind_speed,
          humidity: dayItem.humidity ?? 0,
          pressure: dayItem.pressure ?? 0,
          rain: dayItem.rain_mm ?? dayItem.rain ?? 0
        });
      }
      transformed[dayItem.date] = hours;
    });

  return transformed;
}