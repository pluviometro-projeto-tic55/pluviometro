import { Droplets, Wind, Gauge, CloudRain, GitCompare } from "lucide-react";
import "./style.css";
import BaseCard from "../UI/BaseCard";
import Skeleton from "react-loading-skeleton";

export default function WeatherDetails({ weather, loading }) {
  const skeletonItems = Array.from({ length: 4 });

  const items = [
    {
      title: "Umidade",
      value: `${Math.round(weather?.humidity ?? 0)}%`,
      description: weather?.humidity_status,
      icon: (
        <Droplets
          className="w-5 h-5 3xl:w-8 3xl:h-8"
          color={"var(--text-900)"}
        />
      ),
    },
    {
      title: "Vento",
      value: `${Math.round(weather?.wind_speed ?? 0)} km/h`,
      description: weather?.wind_speed_status,
      icon: (
        <Wind className="w-5 h-5 3xl:w-8 3xl:h-8" color={"var(--text-900)"} />
      ),
    },
    {
      title: "Pressão",
      value: `${Math.round(weather?.pressure ?? 0)} hPa`,
      description: weather?.pressure_trend_status,
      icon: (
        <Gauge className="w-5 h-5 3xl:w-8 3xl:h-8" color={"var(--text-900)"} />
      ),
    },
    {
      title: "Chuva",
      value: `${weather?.rain_mm ?? 0} mm`,
      description: "Precipitação acumulada",
      icon: (
        <CloudRain
          className="w-5 h-5 3xl:w-8 3xl:h-8"
          color={"var(--text-900)"}
        />
      ),
    },
  ]; // <--- Faltava este fechamento de array

  return (
    <div className="weather-details-grid">
      {loading || !weather
        ? skeletonItems.map((_, index) => (
            <BaseCard key={index}>
              <div className="h-full flex justify-around flex-col">
                <Skeleton width={120} height={14} />
                <Skeleton width={100} height={14} />
                <Skeleton width={120} height={14} />
              </div>
            </BaseCard>
          ))
        : items.map((item) => (
            <BaseCard key={item.title}>
              <div className="h-full flex justify-around flex-col">
                <div className="flex justify-between items-center">
                  <p className="text-sm 3xl:text-lg 4xl:text-2xl text-(--text-600)">
                    {item.title}
                  </p>
                  {item.icon}
                </div>

                <p className="text-lg 3xl:text-3xl 4xl:text-4xl font-bold text-(--text-900)">
                  {item.value}
                </p>
                <p className="text-sm 3xl:text-lg 4xl:text-2xl text-(--text-600)">
                  {item.description}
                </p>
              </div>
            </BaseCard>
          ))}
    </div>
  );
}