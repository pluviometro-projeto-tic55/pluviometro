import { useEffect, useState } from "react";
import { notify } from "../../services/notify";
import { useApi } from "../useAPI";

export function useDetailsData(stationId) {
  const [data, setData] = useState(null);
  const { request, loading, error } = useApi();

  useEffect(() => {
    if (!stationId) return;

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
  }, [stationId, request]);

  return { data, loading, error };
}
