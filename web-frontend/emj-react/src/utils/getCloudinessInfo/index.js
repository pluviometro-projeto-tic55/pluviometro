import { Cloud, CloudSun, Sun } from "lucide-react";

/**
 * Retorna informações visuais com base no valor de nebulosidade
 * @param {number} cloudiness
 */
export function getCloudinessInfo(cloudiness = 0) {
  if (cloudiness >= 0.75) {
    return {
      label: "Nublado",
      icon: Cloud,
      color: "#94A3B8",
    };
  }

  if (cloudiness >= 0.4) {
    return {
      label: "Parcialmente nublado",
      icon: CloudSun,
      color: "#FBBF24",
    };
  }

  return {
    label: "Ensolarado",
    icon: Sun,
    color: "#FACC15",
  };
}
