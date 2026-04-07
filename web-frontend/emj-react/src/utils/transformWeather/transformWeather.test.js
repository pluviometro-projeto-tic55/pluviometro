import { describe, it, expect } from "vitest";
import { transformWeatherData } from "../TransformWeather";

describe("transformWeatherData", () => {
  it("deve transformar corretamente os dados do clima", () => {
    const mockData = [
      {
        date: "2026-01-28",
        max_temp: 30.4,
        min_temp: 20.6,
        heat_index: 32.2,
        avg_wind_speed: 10.8,
        cloudiness: 0.5,
      },
    ];

    const result = transformWeatherData(mockData);

    expect(result[0].day).toBe("Hoje");
    expect(result[0].maxTemp).toBe(30);
    expect(result[0].minTemp).toBe(21);
    expect(result[0].feelsLike).toBe(32);
    expect(result[0].windSpeed).toBe(11);
    expect(result[0].rainChance).toBe(0);
    expect(result[0].cloudiness).toBe(0.5);
  });

  it("deve usar nome do dia para índices diferentes de 0", () => {
    const mockData = [
      {
        date: "2026-01-28",
        max_temp: 30,
        min_temp: 20,
        heat_index: 32,
        avg_wind_speed: 10,
        cloudiness: 0.5,
      },
      {
        date: "2026-01-29",
        max_temp: 28,
        min_temp: 19,
        heat_index: 30,
        avg_wind_speed: 9,
        cloudiness: 0.3,
      },
    ];

    const result = transformWeatherData(mockData);

    expect(result[1].day).not.toBe("Hoje");
  });
});
