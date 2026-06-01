export default function VariationBadge({ value }) {
  if (value == null) {
    return <span>-</span>;
  }

  // Mantive sua lógica original de verificação de cor
  const isLowVariation = value <= 10;

  const style = {
    backgroundColor: isLowVariation
      ? "var(--variation-low-bg)"
      : "var(--variation-medium-bg)",
    color: isLowVariation
      ? "var(--variation-low-text)"
      : "var(--variation-medium-text)",
  };

  return (
    <span
      className="p-1! rounded text-sm font-bold min-w-11 text-center"
      style={style}
    >
      {value > 0 ? `+${value}` : value}
    </span>
  );
}
