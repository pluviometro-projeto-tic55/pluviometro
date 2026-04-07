import {
  AreaChart,
  Area,
  CartesianGrid,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

export default function Chart({ data, xKey = "time", config }) {
  // Se não houver config, evita que o componente quebre
  if (!config) return null;

  const gradientId = `chartColor-${config.key}`;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={config.color} stopOpacity={0.3} />
            <stop offset="95%" stopColor={config.color} stopOpacity={0} />
          </linearGradient>
        </defs>

        <CartesianGrid
          strokeDasharray="3 3"
          vertical={false}
          stroke="var(--chart-grid)"
        />

        <XAxis
          dataKey={xKey}
          axisLine={false}
          tickLine={false}
          tick={{ fill: "var(--chart-axis)", fontSize: 11 }}
        />

        <YAxis
          axisLine={false}
          tickLine={false}
          tick={{ fill: "var(--chart-axis)", fontSize: 11 }}
          tickFormatter={(value) => `${value} ${config.unit}`}
          width="auto"
        />

        <Tooltip
          contentStyle={{
            backgroundColor: "rgba(255, 255, 255, 0.95)",
            borderRadius: "8px",
            border: "none",
            boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
            color: "#1e293b",
          }}
          formatter={(value) => [
            `${value.toFixed()} ${config.unit}`,
            config.label,
          ]}
        />

        <Area
          type="monotone"
          dataKey={config.key}
          stroke={config.color}
          strokeWidth={3}
          fillOpacity={1}
          fill={`url(#${gradientId})`}
          animationDuration={500}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}