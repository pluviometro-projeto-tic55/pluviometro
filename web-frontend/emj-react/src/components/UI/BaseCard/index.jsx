export default function BaseCard({ children, style }) {
  return (
    <div className="bg-(--color-surface) border border-(--color-border) rounded-2xl p-6! shadow-sm" style={style}>
      {children}
    </div>
  );
}
