import { renderHook } from "@testing-library/react";
import { useSocketEvent } from "./index";
import socket from "../../services/socket";
import { vi } from "vitest";

vi.mock("../../services/socket", () => ({
  default: {
    on: vi.fn(),
    off: vi.fn(),
  },
}));

describe("useSocketEvent", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("não deve registrar listener se eventName for falsy", () => {
    const handler = vi.fn();

    renderHook(() => useSocketEvent(null, handler));

    expect(socket.on).not.toHaveBeenCalled();
  });

  it("deve registrar listener corretamente", () => {
    const handler = vi.fn();

    renderHook(() => useSocketEvent("event_test", handler));

    expect(socket.on).toHaveBeenCalledWith("event_test", handler);
  });

  it("deve remover listener no unmount", () => {
    const handler = vi.fn();

    const { unmount } = renderHook(() => useSocketEvent("event_test", handler));

    unmount();

    expect(socket.off).toHaveBeenCalledWith("event_test", handler);
  });

  it("deve atualizar listener quando eventName mudar", () => {
    const handler = vi.fn();

    const { rerender } = renderHook(
      ({ event }) => useSocketEvent(event, handler),
      { initialProps: { event: "event_1" } },
    );

    expect(socket.on).toHaveBeenCalledWith("event_1", handler);

    rerender({ event: "event_2" });

    expect(socket.off).toHaveBeenCalledWith("event_1", handler);
    expect(socket.on).toHaveBeenCalledWith("event_2", handler);
  });
});
