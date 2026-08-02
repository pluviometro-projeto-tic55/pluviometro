import { ArrowUp, ArrowDown } from "lucide-react";
import BaseCard from "../UI/BaseCard";
import { getCloudinessInfo } from "../../utils/getCloudinessInfo";
import Skeleton from "react-loading-skeleton";
import PropTypes from "prop-types";

export default function WeatherCard({
  day,
  date,
  maxTemp,
  minTemp,
  feelsLike,
  windSpeed,
  rainMm,
  cloudiness,
  loading,
}) {
  
  if (loading) {
    return (
      <BaseCard>
        <Skeleton height={14} />
        <Skeleton height={14} />
        <Skeleton height={14} />
      </BaseCard>
    );
  }
  const cloudinessInfo = getCloudinessInfo(cloudiness);

  return (
    <BaseCard>
      {/* Header */}
      <div className="flex items-center justify-between mb-3! 3xl:mb-6!">
        <div className="flex flex-col items-start gap-2">
          <h3 className="text-base 3xl:text-2xl 4xl:text-3xl font-bold text-(--text-900)">
            {day}
          </h3>
          <span className="text-xs 3xl:text-lg 4xl:text-xl text-(--text-600)">
            {date}
          </span>
        </div>

        <div className="flex flex-col items-end gap-1">
          <cloudinessInfo.icon
            color={cloudinessInfo.color}
            className="shrink-0 w-6 h-6 3xl:w-8 3xl:h-8 4xl:w-12 4xl:h-12"
          />
          <span className="text-xs 3xl:text-lg 4xl:text-xl text-(--text-600) leading-tight">
            {cloudinessInfo.label}
          </span>
        </div>
      </div>

      {/* Temperaturas */}
      <div className="flex items-center justify-between bg-(--color-filters-bg) rounded-lg h-9 mb-3! px-4! 3xl:h-12 3xl:mb-6! 4xl:h-16">
        <div className="flex justify-center items-center gap-1 text-(--text-red)">
          <ArrowUp className="h-4 w-4 3xl:w-6 3xl:h-6 4xl:w-10 4xl:h-10" />
          <span className="text-base 3xl:text-2xl 4xl:text-3xl font-bold">
            {maxTemp}°
          </span>
        </div>

        <div className="h-6 w-px bg-[#D9D9D9] 3xl:h-8" />

        <div className="flex items-center justify-center gap-1 text-(--text-blue)">
          <ArrowDown className="h-4 w-4 3xl:w-6 3xl:h-6 4xl:w-10 4xl:h-10" />
          <span className="text-base 3xl:text-2xl 4xl:text-3xl font-bold">
            {minTemp}°
          </span>
        </div>
      </div>

      {/* Infos adicionais */}
      <div className="space-y-1 text-xs 3xl:text-base 4xl:text-xl text-(--text-600)">
        <div className="flex justify-between">
          <span>Sensação térmica</span>
          <span>{feelsLike}°</span>
        </div>

        <div className="flex justify-between">
          <span>Vento</span>
          <span>{windSpeed} km/h</span>
        </div>

        <div className="flex justify-between">
          <span>Chuva</span>
          <span>{rainMm} mm</span>
        </div>
      </div>
    </BaseCard>
  );
}

WeatherCard.propTypes = {
  day: PropTypes.string,
  date: PropTypes.string,
  maxTemp: PropTypes.number,
  minTemp: PropTypes.number,
  feelsLike: PropTypes.number,
  windSpeed: PropTypes.number,
  rainMm: PropTypes.number,
  cloudiness: PropTypes.number,
  loading: PropTypes.bool,
};