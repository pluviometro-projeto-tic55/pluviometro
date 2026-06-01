import { useState } from "react";

import Navbar from "../../components/UI/Navbar";
import Footer from "../../components/UI/Footer";
import DailySummary from "../../components/DailySummary";
import WeatherDetails from "../../components/WeatherDetails";
import ForecastChart from "../../components/ForecastChart";
import HistoryChart from "../../components/HistoryChart";
import StationManagement from "../../components/StationManagement";
import BaseCard from "../../components/UI/BaseCard";

import { chartHistoryVariables } from "../../config/charts";
import { forecastVariables } from "../../config/forecastVariables";
import { useForecastData } from "../../hooks/useForecastData";
import { useWeatherUpdates } from "../../hooks/useWeatherUpdates";
import { useDetailsData } from "../../hooks/useDetailsData";
import { transformForecastData } from "../../utils/transformForecast";
import { useStation } from "../../context/StationContext";
import ErrorMessage from "../../components/ErrorMessage/ErrorMessage";

function Advanced() {
  const { stationsLoading, selectedStation, stationId } = useStation();
  const [weatherFromSocket, setWeatherFromSocket] = useState(null);

  const { data: rawForecast, loading: forecastLoading, error: forecastError } = useForecastData(stationId);

  useWeatherUpdates(stationId, setWeatherFromSocket);

  // Agora transformForecastData retorna um objeto { "data": [...] }
  const chartData = transformForecastData(rawForecast || {});

  const { data, loading, error } = useDetailsData(stationId);

  const weatherData = weatherFromSocket ?? data;
  const isLoading = stationsLoading || !selectedStation || loading || forecastLoading;

  if (error || forecastError) {
    return (
      <div className="flex min-h-screen flex-col">
        <Navbar />
        <ErrorMessage onRetry={() => window.location.reload()} />
        <Footer />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />

      <main role="main" className="flex flex-col gap-4 px-5! py-4! md:px-10! lg:px-16! 3xl:gap-6">
        <div className="row-page h-full">
          <DailySummary weather={weatherData} forecast={rawForecast} loading={isLoading} />
          <WeatherDetails weather={weatherData} loading={isLoading} />
        </div>

        {/* Verifica se chartData é um objeto com chaves (dias) */}
        {chartData && typeof chartData === 'object' && Object.keys(chartData).length > 0 ? (
          <ForecastChart
            title="Previsão da Semana"
            variables={forecastVariables}
            data={chartData}
          />
        ) : (
          <BaseCard>
            <h3 className="chart-title">Previsão da Semana</h3>
            <div className="p-8 min-h-28 text-(--text-800) flex items-center justify-center">
              <p>
                {forecastLoading 
                  ? "Carregando previsão..." 
                  : !rawForecast 
                    ? "Erro ao carregar dados da previsão." 
                    : "Dados da previsão indisponíveis para este período."}
              </p>
            </div>
          </BaseCard>
        )}
          
        <HistoryChart
          title="Histórico"
          rcId={stationId}
          variables={chartHistoryVariables}
        />

        <section className="w-full">
          <StationManagement />
        </section>

        <Footer />
      </main>
    </div>
  );
}

export default Advanced;