import { useState } from "react";
import Chart from "../UI/Chart";
import BaseCard from "../UI/BaseCard";
import Button from "../UI/Button";
import DateRangePicker from "../UI/DateRangePicker";
import { Funnel, Download } from "lucide-react";
import "./style.css";
import { useHourlyHistory } from "../../hooks/useHourlyHistory";
import { useExportHistoryCSV } from "../../hooks/useExportHistory";
import { notify } from "../../services/notify";

export default function HistoryChart({ title, rcId, variables }) {
  const variableKeys = Object.keys(variables);
  const [selectedVar, setSelectedVar] = useState(variableKeys[0]);
  const [dateRange, setDateRange] = useState({
    startDate: null,
    endDate: null,
  });

  const startDate = dateRange.startDate
    ? new Date(dateRange.startDate).toISOString().split("T")[0]
    : null;

  const endDate = dateRange.endDate
    ? new Date(dateRange.endDate).toISOString().split("T")[0]
    : startDate;

  const currentVariableConfig = variables[selectedVar];

  const { data, loading } = useHourlyHistory({
    stationId: rcId,
    variable: currentVariableConfig.key,
    startDate,
    endDate,
  });

  const handleDateChange = (range) => {
    setDateRange(range || { startDate: null, endDate: null });
  };

  const chartData = data.map((item) => ({
    day: `${item.day} ${String(item.avgHour).padStart(2, "0")}h`,
    [currentVariableConfig.key]: item[currentVariableConfig.key],
  }));

  const { exportCSV, loading: exporting } = useExportHistoryCSV();

  const handleExportCSV = () => {
    if (!startDate) return;

    exportCSV({
      stationId: rcId,
      variable: currentVariableConfig.key,
      startDate,
      endDate,
    });
  };

  return (
    <BaseCard>
      <div className="chart-header-content">
        {/* Título e botão CSV */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}>
          <h3 className="chart-title">{title}</h3>

          <Button
            variant="export"
            onClick={handleExportCSV}
            disabled={exporting || !startDate}
            aria-label={`Exportar CSV da variável ${selectedVar} para o período selecionado`}>
            <Download size={18} />
            {exporting ? "Exportando..." : "Exportar CSV"}
          </Button>
        </div>

        {/* Controles */}
        <div className="controls-bar-row">
          <div className="date-picker-fixed-width">
            <DateRangePicker
              onChange={handleDateChange}
              aria-label="Selecionar período de datas para exibir o gráfico"
            />
          </div>

          <div className="chart-filters-content">
            <div className="chart-filters-label">
              <Funnel size={18} />
              <span>FILTROS :</span>
            </div>

            <div className="chart-filters-btn">
              {variableKeys.map((label) => (
                <Button
                  key={label}
                  variant={`secondary ${selectedVar === label ? "active" : ""}`}
                  onClick={() => {
                    if (!dateRange.startDate || !dateRange.endDate) {
                      notify.warning(
                        "É necessário ter uma data inicial e final selecionada.",
                      );
                      return;
                    }
                    setSelectedVar(label);
                  }}
                  aria-pressed={selectedVar === label}
                  aria-label={`Filtrar por variável ${label}`}>
                  {label}
                </Button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Gráfico */}
      <div
        className="chart-display-container"
        role="region"
        aria-label={`Gráfico de ${selectedVar} para o período selecionado`}>
        {loading ? (
          <div className="no-data-placeholder">
            <p>Carregando dados...</p>
          </div>
        ) : chartData.length > 0 ? (
          <Chart
            key={`${selectedVar}-${dateRange.startDate}`}
            data={chartData}
            xKey="day"
            config={{ ...currentVariableConfig, label: selectedVar }}
          />
        ) : (
          <div className="no-data-placeholder">
            <p>Selecione um período para visualizar os dados</p>
          </div>
        )}
      </div>
    </BaseCard>
  );
}
