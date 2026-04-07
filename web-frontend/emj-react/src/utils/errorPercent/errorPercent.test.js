import { describe, it, expect } from "vitest";
import { errorPercent } from "../errorPercent";

describe("errorPercent", () => {
  it("deve calcular corretamente o percentual de erro", () => {
    const result = errorPercent(100, 120);
    expect(result).toBe(20);
  });

  it("deve retornar valor absoluto arredondado", () => {
    const result = errorPercent(100, 80);
    expect(result).toBe(20);
  });

  it("deve retornar null se local for 0", () => {
    expect(errorPercent(0, 100)).toBeNull();
  });

  it("deve retornar null se valores forem null", () => {
    expect(errorPercent(null, 100)).toBeNull();
    expect(errorPercent(100, null)).toBeNull();
  });
});
