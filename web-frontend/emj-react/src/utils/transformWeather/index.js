export function transformWeatherData(data) {
  return data.map((dayData, index) => {
    const [year, month, day] = dayData.date.split("-").map(Number);
    const dateObj = new Date(year, month - 1, day); 

    const dayName = dateObj.toLocaleDateString("pt-BR", {
      weekday: "long",
    });

    const formattedDate = dateObj.toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "short",
    });

    return {
      day: index === 0 ? "Hoje" : dayName,
      date: formattedDate,
      maxTemp: Math.round(dayData.max_temp),
      minTemp: Math.round(dayData.min_temp),
      feelsLike: Math.round(dayData.heat_index),
      windSpeed: Math.round(dayData.avg_wind_speed),
      rainChance: 0, //mockado por enquanto
      cloudiness: dayData.cloudiness,
    };
  });
}
