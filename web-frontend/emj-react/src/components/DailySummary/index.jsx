import { useMemo, useState } from "react";
import BaseCard from "../../components/UI/BaseCard";
import { getFormattedDate } from "../../utils/dateUtils";
import { getCloudinessInfo } from "../../utils/getCloudinessInfo";
import Button from "../UI/Button";
import {
  AlarmClock,
  ArrowDown,
  ArrowUp,
  GitCompare,
  ThermometerSun,
} from "lucide-react";
import Skeleton from "react-loading-skeleton";
import PropTypes from "prop-types";
import { useExternalCurrentData } from "../../hooks/useExternalCurrentData/useExternalCurrentData";
import { useStation } from "../../context/StationContext";
import ComparisonModal from "./comparisionModal";

function DailySummary({ weather, forecast, loading }) {
  console.log("last_update:", weather?.last_update); //Modificação
  const { stationId } = useStation();
  const { data: externalData } = useExternalCurrentData(stationId);

  const { fullDayOfWeek, formattedDate } = getFormattedDate();

  const cloudinessInfo = getCloudinessInfo(weather?.cloudiness);

  const [isModalOpen, setIsModalOpen] = useState(false);

  const todayTemps = useMemo(() => {
    if (!forecast?.daily_summary?.length) return null;

    const todayData = forecast.daily_summary[0];

    return {
      tempMin: Math.round(todayData.min_temp),
      tempMax: Math.round(todayData.max_temp),
      felsLike: Math.round(todayData.heat_index),
    };
  }, [forecast]);

  const rawStatus = weather?.status;
  const rawStatus = weather?.status;

const normalizedStatus = String(rawStatus)
  .trim()
  .toLowerCase();

const isOnline = [
  true,
  1,
  '1',
  'on',
  'online',
  'active',
  'ativo',
  'connected'
].includes(
  typeof rawStatus === 'string'
    ? normalizedStatus
    : rawStatus
);

  const statusColor = isOnline ? "bg-emerald-500" : "bg-red-500";
  const statusGlow = isOnline ? "shadow-[0_0_6px_rgba(16,185,129,0.5)]" : "shadow-[0_0_6px_rgba(239,68,68,0.5)]";
  
  const getUpdateLabel = (minutes) => {
    if (!minutes || minutes < 1) return "Atualizado agora";
    
    // Menos de 1 hora
    if (minutes < 60) {
      return `Atualizado há ${minutes} min`;
    }

    const hours = Math.floor(minutes / 60);

    // Exato horas (1 a 12 horas)
    if (hours <= 12) {
      return `Atualizado há ${hours} ${hours === 1 ? 'hora' : 'horas'}`;
    }

    // Entre 12 e 24 horas
    if (hours < 24) {
      return "Atualizado há mais de 12 horas";
    }

    // Mais de 24 horas
    return "Atualizado há mais de 24 horas";
  };
  
  return (
    <BaseCard>
      <div className="h-full flex md:flex-row justify-between gap-6 flex-col md:gap-5">
        {/* BLOCO ESQUERDO */}
        <div className="flex flex-3 lg:pl-4! flex-col items-center justify-center md:items-start">
          {loading || !weather ? (
            <>
              <Skeleton width={120} height={14} />
              <Skeleton width={200} height={14} />
              <Skeleton width={140} height={14} />
            </>
          ) : (
            <>
              <div className="flex items-center mb-2!">
                <AlarmClock className="mr-2! text-(--text-600) w-3.5 h-3.5 3xl:w-4 3xl:h-4" />

                {/* info de ultima atulização */}
                <p className="text-(--text-600) text-xs 3xl:text-base 4xl:text-xl mr-3!">
                  {getUpdateLabel(weather?.last_update)}
                </p>

                {/* indicador de status */}
                <div
                  className={`w-2.5 h-2.5 rounded-full ${statusColor} ${statusGlow} transition-colors duration-300`}
                  title={isOnline ? "Estação Online" : "Estação Offline"}
                />
              </div>

              <div className="flex items-center gap-5">
                <h1 className="text-(--text-900) font-bold leading-none text-[84px] 3xl:text-9xl 4xl:text-[160px]">
                  {Math.round(weather?.temperature ?? 0)}°
                </h1>

                <div className="flex flex-col items-start text-base 3xl:text-xl 4xl:text-3xl text-(--text-600)">
                  <cloudinessInfo.icon
                    color={cloudinessInfo.color}
                    className="weather-icon w-8 h-8 3xl:w-12 3xl:h-12 4xl:w-16  4xl:h-16"
                  />
                  <span>{cloudinessInfo.label}</span>
                </div>
              </div>

              <div className="mt-3! flex gap-5">
                <div className="flex items-center gap-1">
                  <ArrowUp
                    className="w-6 h-6 3xl:w-8 3xl:h-8 4xl:w-10 4xl:h-10"
                    color="var(--text-red)"
                  />
                  <p className="text-(--text-600) text-sm 3xl:text-lg 4xl:text-2xl">
                    Máx: {todayTemps?.tempMax ?? "-"}°
                  </p>
                </div>
                <div className="flex items-center gap-1">
                  <ArrowDown
                    className="w-6 h-6 3xl:w-8 3xl:h-8 4xl:w-10 4xl:h-10"
                    color="var(--text-blue)"
                  />
                  <p className="text-(--text-600) text-sm 3xl:text-lg 4xl:text-2xl">
                    Min: {todayTemps?.tempMin ?? "-"}°
                  </p>
                </div>
              </div>
            </>
          )}
        </div>

        {/* BLOCO DIREITO */}
        <div className="flex flex-2 flex-col p-4! 3xl:p-8! 4xl:p-9! justify-between rounded-2xl text-white bg-primary-secondary-gradient">
          {loading || !weather ? (
            <>
              <div>
                <Skeleton width={180} height={14} />
                <Skeleton width={180} height={14} />
              </div>
              <Skeleton height={14} />
              <Skeleton height={14} />
            </>
          ) : (
            <>
              <div>
                <h2 className="text-xl 3xl:text-3xl 4xl:text-4xl font-bold">
                  {fullDayOfWeek}
                </h2>
                <p className="mt-2! text-sm 3xl:text-xl 4xl:text-2xl">
                  {formattedDate}
                </p>
              </div>

              <div className="flex gap-4 items-center text-white text-sm my-4!">
                <div className="flex gap-2 items-center 4xl:gap-4">
                  <ThermometerSun className="shrink-0 w-4.5 h-4.5 3xl:w-10 3xl:h-10 4xl:h-12 4xl:w-12" />
                  <p className="text-sm 3xl:text-xl 4xl:text-2xl">
                    Sensação Térmica
                  </p>
                </div>
                <p className="font-bold text-sm 3xl:text-xl 4xl:text-2xl">
                  {todayTemps?.felsLike ?? "-"}°
                </p>
              </div>

              <Button
                variant="ghost"
                onClick={() => setIsModalOpen(true)}
                aria-label="Abrir comparação de dados da API Externa">
                <GitCompare className="shrink-0 mr-1 w-4.5 h-4.5 3xl:w-6 3xl:h-6" />
                Comparação API Externa
              </Button>

              <ComparisonModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                weather={weather}
                externalData={externalData}
              />
            </>
          )}
        </div>
      </div>
    </BaseCard>
  );
}

export default DailySummary;
DailySummary.propTypes = {
  weather: PropTypes.shape({
    temperature: PropTypes.number,
    wind_speed: PropTypes.number,
    rain_chance: PropTypes.number,
    humidity: PropTypes.number,
    pressure:  PropTypes.number,
    cloudiness: PropTypes.number,
    last_update: PropTypes.number,
    status: PropTypes.string,
  }),

  forecast: PropTypes.shape({
    daily_summary: PropTypes.arrayOf(
      PropTypes.shape({
        min_temp: PropTypes.number,
        max_temp: PropTypes.number,
        heat_index: PropTypes.number,
      }),
    ),
  }),

  loading: PropTypes.bool,
};
