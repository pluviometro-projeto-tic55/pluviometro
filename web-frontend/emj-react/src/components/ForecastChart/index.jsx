import { useState } from "react";
import Chart from "../UI/Chart";
import BaseCard from "../UI/BaseCard";
import Button from "../UI/Button";
import "./style.css";
import { Funnel } from "lucide-react";
import { getFormattedDate } from "../../utils/dateUtils";

export default function ForecastChart({ data, variables, title }) {
  const variableKeys = Object.keys(variables);
  const dataKeys = Object.keys(data);

  const [selectedVar, setSelectedVar] = useState(variableKeys[0]);
  const [selectedData, setSelectedData] = useState(dataKeys[0]);

  const config = variables[selectedVar];
  const chartData = selectedData ? data[selectedData] : [];

  return (
    <BaseCard>
      <div className="chart-header-content">
        {/* Título */}
        <h3 className="chart-title">{title}</h3>

        {/* Botões de dias */}
        <div
          className="chart-days-btn"
          role="group"
          aria-label="Selecionar dia para exibir dados horários">
          {dataKeys.map((item) => {
            const { dayOfWeek, shortDate } = getFormattedDate(item);

            return (
              <Button
                key={item}
                variant={`tertiary ${selectedData === item ? "active" : ""}`}
                onClick={() => setSelectedData(item)}
                aria-pressed={selectedData === item}
                aria-label={`Selecionar dia ${dayOfWeek}, ${shortDate}`}>
                <span>{dayOfWeek}</span>
                <span className="day-date">{shortDate}</span>
              </Button>
            );
          })}
        </div>

        {/* Botões de variáveis */}
        <div className="chart-filters-content">
          <div className="chart-filters-label">
            <Funnel size={18} />
            <span>FILTROS :</span>
          </div>

          <div
            className="chart-filters-btn"
            role="group"
            aria-label="Selecionar variável para exibir no gráfico">
            {variableKeys.map((label) => (
              <Button
                key={label}
                variant={`secondary ${selectedVar === label ? "active" : ""}`}
                onClick={() => setSelectedVar(label)}
                aria-pressed={selectedVar === label}
                aria-label={`Selecionar variável ${label}`}>
                {label}
              </Button>
            ))}
          </div>
        </div>
      </div>

      {/* Gráfico */}
      <div
        role="region"
        aria-label={`Gráfico horário da variável ${selectedVar} para o dia ${getFormattedDate(selectedData).dayOfWeek}`}>
        <Chart
          data={chartData}
          config={{
            ...config,
            label: selectedVar,
          }}
        />
      </div>
    </BaseCard>
  );
}
