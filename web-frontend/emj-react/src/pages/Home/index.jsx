import { useState, useMemo } from "react";

import Navbar from "../../components/UI/Navbar";
import Footer from "../../components/UI/Footer/index.jsx";

import DailySummary from "../../components/DailySummary";
import WeatherDetails from "../../components/WeatherDetails";
import WeatherCard from "../../components/WeatherCard";

import { useWeatherUpdates } from "../../hooks/useWeatherUpdates";
import { useForecastData } from "../../hooks/useForecastData";

import { useDetailsData } from "../../hooks/useDetailsData";
import { useExternalCurrentData } from "../../hooks/useExternalCurrentData/useExternalCurrentData";
import { useStation } from "../../context/StationContext.jsx";
import { transformWeatherData } from "../../utils/transformWeather";
import ErrorMessage from "../../components/ErrorMessage/ErrorMessage.jsx";

export default function Home() {
  const { stationsLoading, selectedStation, stationId } = useStation();

  const [weatherFromSocket, setWeatherFromSocket] = useState(null);
  useWeatherUpdates(stationId, setWeatherFromSocket);

  const { 
    data: rawForecast, 
    loading: forecastLoading, 
    error: forecastError 
  } = useForecastData(stationId);

  const weekData = useMemo(() => {
    if (!rawForecast?.daily_summary) return [];
    return transformWeatherData(rawForecast.daily_summary);
  }, [rawForecast]);

  const { data, loading, error } = useDetailsData(stationId);
  const { data: externalData } = useExternalCurrentData(stationId);

  const weatherData = useMemo(() => {
    const baseWeather = weatherFromSocket ?? data;
    if (!baseWeather) return null;

    return {
      ...baseWeather,
      external_rain_mm: externalData?.external_rain_mm ?? 0,
    };
  }, [weatherFromSocket, data, externalData]);

  const isLoading = stationsLoading || !selectedStation || loading || forecastLoading;

  if (error || forecastError) {
    return (
      <div className="flex min-h-screen flex-col">
        <Navbar className="h-[10dvh]" />
        <ErrorMessage onRetry={() => window.location.reload()} />
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-full flex flex-col">
      <Navbar className="h-[10dvh]" />

      <main
        role="main"
        className="h-[90dvh] grid grid-rows-[1fr_1fr_auto] gap-4 px-5! py-4! md:px-10! lg:px-16!">
        <h1 className="sr-only">Previsão do Tempo</h1>

        <div className="row-page h-full">
          <DailySummary
            weather={weatherData}
            forecast={rawForecast}
            loading={isLoading}
          />
          <WeatherDetails weather={weatherData} loading={isLoading} />
        </div>

        <section className="flex flex-col h-full">
          <h2 className="mb-3! text-base 3xl:text-2xl font-bold text-(--text-900)">
            Previsão para 4 dias
          </h2>

          <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 flex-1">
            {weekData && weekData.length > 0
              ? weekData
                  .slice(0, 4)
                  .map((day) => (
                    <WeatherCard key={day.date} {...day}/>
                  ))
              : Array.from({ length: 4 }).map((_, index) => (
                  <WeatherCard key={`loading-${index}`} loading />
                ))}
          </div>
        </section>

        <Footer />
      </main>
    </div>
  );
}