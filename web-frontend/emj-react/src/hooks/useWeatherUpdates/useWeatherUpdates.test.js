import { renderHook } from "@testing-library/react";
import { useWeatherUpdates } from "./index";
import { useSocketEvent } from "../useSocketEvent";
import { vi } from "vitest";

vi.mock("../useSocketEvent", () => ({
  useSocketEvent: vi.fn(),
}));

describe("useWeatherUpdates", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("deve montar corretamente o nome do evento", () => {
    const setWeatherData = vi.fn();

    renderHook(() => useWeatherUpdates(5, setWeatherData));

    expect(useSocketEvent).toHaveBeenCalledWith(
      "update_weather_5",
      setWeatherData,
    );
  });

  it("deve passar null se stationId for falsy", () => {
    const setWeatherData = vi.fn();

    renderHook(() => useWeatherUpdates(null, setWeatherData));

    expect(useSocketEvent).toHaveBeenCalledWith(null, setWeatherData);
  });
});
