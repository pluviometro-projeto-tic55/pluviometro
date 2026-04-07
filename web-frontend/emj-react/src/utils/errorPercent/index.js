export function errorPercent(local, external) {
  if (local == null || external == null) return null;

  if (local === 0 && external === 0) return 0;

  const denominator = (Math.abs(local) + Math.abs(external)) / 2;
  if (denominator === 0) return 0;

  return Math.round((Math.abs(external - local) / denominator) * 100);
}