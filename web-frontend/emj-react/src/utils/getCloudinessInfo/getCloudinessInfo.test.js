import { describe, it, expect } from "vitest";
import { getCloudinessInfo } from "../getCloudinessInfo";
import { Cloud, CloudSun, Sun } from "lucide-react";

describe("getCloudinessInfo", () => {
  it("deve retornar Nublado quando >= 0.75", () => {
    const result = getCloudinessInfo(0.8);

    expect(result.label).toBe("Nublado");
    expect(result.icon).toBe(Cloud);
    expect(result.color).toBe("#94A3B8");
  });

  it("deve retornar Parcialmente nublado quando >= 0.4", () => {
    const result = getCloudinessInfo(0.5);

    expect(result.label).toBe("Parcialmente nublado");
    expect(result.icon).toBe(CloudSun);
    expect(result.color).toBe("#FBBF24");
  });

  it("deve retornar Ensolarado quando < 0.4", () => {
    const result = getCloudinessInfo(0.2);

    expect(result.label).toBe("Ensolarado");
    expect(result.icon).toBe(Sun);
    expect(result.color).toBe("#FACC15");
  });

  it("deve usar valor padrão 0", () => {
    const result = getCloudinessInfo();
    expect(result.label).toBe("Ensolarado");
  });
});
