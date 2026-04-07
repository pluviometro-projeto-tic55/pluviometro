import { useEffect, useState } from "react";
import { notify } from "../../services/notify";
import { useApi } from "../useAPI";

export function useHourlyHistory({ stationId, variable, startDate, endDate }) {
  const [data, setData] = useState([]);
  const { request, loading, error } = useApi();

  useEffect(() => {
    if (!stationId || !variable || !startDate) return;

    request({
      method: "get",
      url: `/api/stations/${stationId}/history`,
      params: {
        rc_id: stationId,
        variable,
        start_date: startDate,
        end_date: endDate || startDate,
      },
    })
      .then((response) => {
        setData(response.data); 
      })
      .catch(() => {
        notify.error(
          "Erro ao conectar com o servidor. Tente novamente mais tarde.",
        );
      });
  }, [stationId, variable, startDate, endDate, request]);

  return { data, loading, error };
}
