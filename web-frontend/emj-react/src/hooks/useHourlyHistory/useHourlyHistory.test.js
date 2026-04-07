import { renderHook, waitFor } from "@testing-library/react";
import { useHourlyHistory } from "./index";
import { useApi } from "../useAPI";
import { notify } from "../../services/notify";
import { vi } from "vitest";

vi.mock("../useAPI");
vi.mock("../../services/notify", () => ({
  notify: {
    error: vi.fn(),
  },
}));

describe("useHourlyHistory", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("não deve chamar API se parâmetros obrigatórios faltarem", () => {
    const mockRequest = vi.fn();

    useApi.mockReturnValue({
      request: mockRequest,
      loading: false,
      error: null,
    });

    renderHook(() =>
      useHourlyHistory({
        stationId: null,
        variable: "temp",
        startDate: "2024-01-01",
      }),
    );

    expect(mockRequest).not.toHaveBeenCalled();
  });

  it("deve chamar API com parâmetros corretos", async () => {
    const mockData = [{ hour: "10:00", value: 25 }];

    const mockRequest = vi.fn().mockResolvedValue({
      data: mockData,
    });

    useApi.mockReturnValue({
      request: mockRequest,
      loading: false,
      error: null,
    });

    const { result } = renderHook(() =>
      useHourlyHistory({
        stationId: 1,
        variable: "temp",
        startDate: "2024-01-01",
        endDate: "2024-01-02",
      }),
    );

    await waitFor(() => {
      expect(result.current.data).toEqual(mockData);
    });

    expect(mockRequest).toHaveBeenCalledWith({
      method: "get",
      url: "/api/stations/1/history",
      params: {
        rc_id: 1,
        variable: "temp",
        start_date: "2024-01-01",
        end_date: "2024-01-02",
      },
    });
  });

  it("deve usar startDate como endDate se não for informado", async () => {
    const mockData = [];

    const mockRequest = vi.fn().mockResolvedValue({
      data: mockData,
    });

    useApi.mockReturnValue({
      request: mockRequest,
      loading: false,
      error: null,
    });

    renderHook(() =>
      useHourlyHistory({
        stationId: 1,
        variable: "temp",
        startDate: "2024-01-01",
      }),
    );

    await waitFor(() => {
      expect(mockRequest).toHaveBeenCalledWith({
        method: "get",
        url: "/api/stations/1/history",
        params: {
          rc_id: 1,
          variable: "temp",
          start_date: "2024-01-01",
          end_date: "2024-01-01",
        },
      });
    });
  });

  it("deve chamar notify.error se a API falhar", async () => {
    const mockRequest = vi.fn().mockRejectedValue(new Error("erro"));

    useApi.mockReturnValue({
      request: mockRequest,
      loading: false,
      error: null,
    });

    renderHook(() =>
      useHourlyHistory({
        stationId: 1,
        variable: "temp",
        startDate: "2024-01-01",
      }),
    );

    await waitFor(() => {
      expect(notify.error).toHaveBeenCalledWith(
        "Erro ao conectar com o servidor. Tente novamente mais tarde.",
      );
    });
  });
});
