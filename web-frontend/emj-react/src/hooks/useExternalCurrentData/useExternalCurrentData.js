import { useEffect, useState } from "react";
import { notify } from "../../services/notify";
import { useApi } from "../useAPI";

export function useExternalCurrentData(stationId) {
  const [data, setData] = useState(null);
  const { request, loading, error } = useApi();

  useEffect(() => {
  if (!stationId) return;

  const fetchData = () => {
    request({
      method: "get",
      url: `/api/stations/${stationId}/external/current`,
    })
      .then((response) => {
        setData(response.data);
      })
      .catch((err) => {
        if (err?.response?.status === 503) {
          notify.warning("Dados externos temporariamente indisponíveis.");
        } else {
          notify.error(
            "Erro ao buscar dados externos. Tente novamente mais tarde.",
          );
        }
      });
  };

  // chama uma vez ao abrir
  fetchData();

  //chama a cada 5 minutos
  const interval = setInterval(fetchData, 300000);

  // limpa quando sair da tela
  return () => clearInterval(interval);

}, [stationId]);
  return { data, loading, error };
}
