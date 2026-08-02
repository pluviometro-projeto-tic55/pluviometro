import { useEffect, useRef, useState } from "react";
import { notify } from "../../services/notify";
import { useApi } from "../useAPI";

export function useExternalCurrentData(stationId) {
  const [data, setData] = useState(null);
  const [lastSuccessAt, setLastSuccessAt] = useState(null);
  const [isExternalOnline, setIsExternalOnline] = useState(false);
  const { request, loading, error } = useApi();
  const hasShownErrorRef = useRef(false);

  useEffect(() => {
    if (!stationId) {
      setData(null);
      setLastSuccessAt(null);
      setIsExternalOnline(false);
      hasShownErrorRef.current = false;
      return;
    }

    const fetchData = () => {
      request({
        method: "get",
        url: `/api/stations/${stationId}/external/current`,
      })
        .then((response) => {
          setData(response.data);
          setLastSuccessAt(Date.now());
          setIsExternalOnline(true);
          hasShownErrorRef.current = false;
        })
        .catch((err) => {
          setIsExternalOnline(false);

          if (!hasShownErrorRef.current) {
            if (err?.response?.status === 503) {
              notify.warning("Dados externos temporariamente indisponíveis.");
            } else {
              notify.error(
                "Erro ao buscar dados externos. Tente novamente mais tarde.",
              );
            }

            hasShownErrorRef.current = true;
          }
        });
    };

    // chama uma vez ao abrir
    fetchData();

    // chama a cada 3 minutos
    const interval = setInterval(fetchData, 180000);

    // limpa quando sair da tela
    return () => clearInterval(interval);
  }, [stationId, request]);

  return { data, loading, error, lastSuccessAt, isExternalOnline };
}
