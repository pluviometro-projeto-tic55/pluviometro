import { useEffect, useState } from "react";
import { notify } from "../../services/notify";
import { useApi } from "../useAPI";

export function useDetailsData(stationId) {
  const [data, setData] = useState(null);
  const { request, loading, error } = useApi();

  useEffect(() => {
    if (!stationId) {
      setData(null);
      return;
    }

    const fetchData = () => {
      request({
        method: "get",
        url: `/api/stations/${stationId}/current`,
      })
        .then((response) => {
          setData(response.data);
        })
        .catch(() => {
          notify.error(
            "Erro ao conectar com o servidor. Tente novamente mais tarde.",
          );
        });
    };

    fetchData();

    // Atualiza automaticamente a cada 3 minutos.
    const interval = setInterval(fetchData, 180000);

    return () => clearInterval(interval);
  }, [stationId, request]);

  return { data, loading, error };
}
