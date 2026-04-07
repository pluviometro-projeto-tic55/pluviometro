import { renderHook, waitFor } from "@testing-library/react";
import { useStations } from "./index";
import { useApi } from "../useAPI";
import { notify } from "../../services/notify";

vi.mock("../useAPI");
vi.mock("../../services/notify", () => ({
  notify: {
    error: vi.fn(),
  },
}));

describe("useStations", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("deve transformar dados corretamente", async () => {
    const apiData = [
      {
        rcId: 1,
        local: "Recife",
        latitude: "10",
        longitude: "20",
      },
    ];

    const mockRequest = vi.fn().mockResolvedValue({
      data: apiData,
    });

    useApi.mockReturnValue({
      request: mockRequest,
      loading: false,
      error: null,
    });

    const { result } = renderHook(() => useStations());

    await waitFor(() => {
      expect(result.current.stations.length).toBe(1);
    });

    expect(result.current.stations[0]).toEqual({
      id: 1,
      label: "Recife",
      lat: 10,
      lng: 20,
      value: 1,
    });
  });

  it("deve chamar notify.error se falhar", async () => {
    const mockRequest = vi.fn().mockRejectedValue(new Error("erro"));

    useApi.mockReturnValue({
      request: mockRequest,
      loading: false,
      error: null,
    });

    renderHook(() => useStations());

    await waitFor(() => {
      expect(notify.error).toHaveBeenCalledWith(
        "Erro ao conectar com o servidor.",
      );
    });
  });
});
