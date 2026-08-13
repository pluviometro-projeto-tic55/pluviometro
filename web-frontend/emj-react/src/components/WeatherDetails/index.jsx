import { Droplets, Wind, Gauge, CloudRain } from "lucide-react";

import "./style.css";

import BaseCard from "../UI/BaseCard";

import Skeleton from "react-loading-skeleton";



export default function WeatherDetails({ weather, loading }) {

  const skeletonItems = Array.from({ length: 4 });

  const isExternalHumidityActive = weather?.humidity === 100 && weather?.external_humidity != null;
  const currentHumidity = isExternalHumidityActive ? weather.external_humidity : weather?.humidity;
  const humidityDescription = isExternalHumidityActive ? "Muito Úmido (Externo)" : weather?.humidity_status;

  const items = [

    {

      title: "Umidade",

      value: currentHumidity != null ? `${Math.round(currentHumidity)}%` : "-",

      description: humidityDescription,

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
      value: (() => {
        // Lógica de fallback: usa external_rain_mm se o valor local for 0 ou nulo
        const isExternalRainActive = (!weather?.rain_mm || weather.rain_mm === 0) && weather?.external_rain_mm != null && weather.external_rain_mm > 0;
        const currentRain = isExternalRainActive ? weather.external_rain_mm : (weather?.rain_mm ?? 0);
        return `${Math.round(currentRain)} mm`;
      })(),
      description: (() => {
        const isExternalRainActive = (!weather?.rain_mm || weather.rain_mm === 0) && weather?.external_rain_mm != null && weather.external_rain_mm > 0;
        return isExternalRainActive ? "Precipitação Acumulada" : "Milímetros acumulados";
      })(),
      icon: (
        <CloudRain
          className="w-5 h-5 3xl:w-8 3xl:h-8"
          color={"var(--text-900)"}
        />
      ),
    },
  ]; 


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