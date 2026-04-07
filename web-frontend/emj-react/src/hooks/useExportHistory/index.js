import { useApi } from "../useAPI";

export function useExportHistoryCSV() {
  const { request, loading, error } = useApi();

  const exportCSV = async ({ stationId, variable, startDate, endDate }) => {
    if (!stationId || !variable || !startDate) return;

    const response = await request({
      method: "get",
      url: `/api/stations/${stationId}/history/export`,
      params: {
        rc_id: stationId,
        variable,
        start_date: startDate,
        end_date: endDate || startDate,
      },
      responseType: "blob",
    });

    const disposition = response.headers["content-disposition"];
    let filename = "export.csv";

    if (disposition) {
      const match = disposition.match(/filename="?([^"]+)"?/);
      if (match?.[1]) {
        filename = match[1];
      }
    }

    const blob = new Blob([response.data], {
      type: "text/csv;charset=utf-8;",
    });

    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = filename;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  return { exportCSV, loading, error };
}
