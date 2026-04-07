import { renderHook, waitFor } from "@testing-library/react";
import { useDetailsData } from "./index";
import { useApi } from "../useAPI";
import { notify } from "../../services/notify";
import { vi } from "vitest";

vi.mock("../useAPI");
vi.mock("../../services/notify", () => ({
  notify: {
    error: vi.fn(),
  },
}));

describe("useDetailsData", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("não deve chamar request se stationId for null", () => {
    const mockRequest = vi.fn();

    useApi.mockReturnValue({
      request: mockRequest,
      loading: false,
      error: null,
    });

    renderHook(() => useDetailsData(null));

    expect(mockRequest).not.toHaveBeenCalled();
  });

  it("deve buscar dados corretamente", async () => {
    const mockData = { name: "Station 1" };

    const mockRequest = vi.fn().mockResolvedValue({
      data: mockData,
    });

    useApi.mockReturnValue({
      request: mockRequest,
      loading: false,
      error: null,
    });

    const { result } = renderHook(() => useDetailsData(1));

    await waitFor(() => {
      expect(result.current.data).toEqual(mockData);
    });

    expect(mockRequest).toHaveBeenCalledWith({
      method: "get",
      url: "/api/stations/1/current",
    });
  });

  it("deve chamar notify.error se falhar", async () => {
    const mockRequest = vi.fn().mockRejectedValue(new Error("erro"));

    useApi.mockReturnValue({
      request: mockRequest,
      loading: false,
      error: null,
    });

    renderHook(() => useDetailsData(1));

    await waitFor(() => {
      expect(notify.error).toHaveBeenCalledWith(
        "Erro ao conectar com o servidor. Tente novamente mais tarde.",
      );
    });
  });
});
