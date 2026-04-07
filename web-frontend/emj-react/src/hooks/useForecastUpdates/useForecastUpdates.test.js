import { renderHook } from "@testing-library/react";
import { useForecastUpdates } from "./index";
import { useSocketEvent } from "../useSocketEvent";
import { vi } from "vitest";

vi.mock("../useSocketEvent", () => ({
  useSocketEvent: vi.fn(),
}));

describe("useForecastUpdates", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("deve montar corretamente o nome do evento de forecast", () => {
    const setForecastData = vi.fn();

    renderHook(() => useForecastUpdates(10, setForecastData));

    expect(useSocketEvent).toHaveBeenCalledWith(
      "update_forecast_10",
      setForecastData,
    );
  });

  it("deve passar null se stationId for falsy", () => {
    const setForecastData = vi.fn();

    renderHook(() => useForecastUpdates(null, setForecastData));

    expect(useSocketEvent).toHaveBeenCalledWith(null, setForecastData);
  });
});
