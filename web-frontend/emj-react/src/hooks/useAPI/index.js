import { useState, useCallback } from "react";
import { api } from "../../services/api";

export function useApi() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const request = useCallback(async (config) => {
    try {
      setLoading(true);
      setError(null);

      const response = await api({
        ...config,
      });

      return response;
    } catch (err) {
      setError(err);
      throw err;
      
    } finally {
      setLoading(false);
    }
  }, []);

  return { request, loading, error };
}
