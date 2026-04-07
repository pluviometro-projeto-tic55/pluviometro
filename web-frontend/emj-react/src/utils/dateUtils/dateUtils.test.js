import { describe, it, expect, vi, beforeAll, afterAll } from "vitest";
import { getFormattedDate } from ".";

describe("getFormattedDate", () => {
  it("deve formatar corretamente uma data ISO", () => {
    const result = getFormattedDate("2026-01-28");

    expect(result.shortDate).toBe("28/01");
    expect(result.formattedDate).toContain("28 de");
    expect(result.dayOfWeek).toBeDefined();
    expect(result.fullDayOfWeek).toBeDefined();
  });

  it("deve usar a data atual quando não recebe parâmetro", () => {
    const mockDate = new Date(2026, 0, 28);
    vi.useFakeTimers();
    vi.setSystemTime(mockDate);

    const result = getFormattedDate();

    expect(result.shortDate).toBe("28/01");

    vi.useRealTimers();
  });
});
