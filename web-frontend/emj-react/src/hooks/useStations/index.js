import { useState, useEffect } from "react";
import { notify } from "../../services/notify";
import { useApi } from "../useAPI";

export function useStations() {
  const { request, loading, error } = useApi();
  const [stations, setStations] = useState([]);

  useEffect(() => {
    request({
      method: "get",
      url: "/api/stations",
    })
      .then((response) => {
        const options = response.data
          .map((station) => ({
            id: station.rcId,
            label: station.local,
            lat: Number(station.latitude),
            lng: Number(station.longitude),
            value: station.rcId,
          }))
          .filter(Boolean);

        setStations(options);
      })
      .catch(() => {
        notify.error("Erro ao conectar com o servidor.");
      });
  }, [request]);

  return { stations, loading, error };
}
