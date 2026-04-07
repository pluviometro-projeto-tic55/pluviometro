import { renderHook, act } from "@testing-library/react";
import { useApi } from "../useAPI";
import { api } from "../../services/api";

vi.mock("../../services/api", () => ({
  api: vi.fn(),
}));

describe("useApi", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("deve iniciar com loading false e error null", () => {
    const { result } = renderHook(() => useApi());

    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it("deve realizar request com sucesso", async () => {
    const mockResponse = { data: "ok" };
    api.mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useApi());

    let response;

    await act(async () => {
      response = await result.current.request({ url: "/test" });
    });

    expect(api).toHaveBeenCalledWith({ url: "/test" });
    expect(response).toEqual(mockResponse);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it("deve tratar erro corretamente", async () => {
    const mockError = new Error("Erro API");
    api.mockRejectedValue(mockError);

    const { result } = renderHook(() => useApi());

    await act(async () => {
      await expect(result.current.request({ url: "/error" })).rejects.toThrow(
        "Erro API",
      );
    });

    expect(result.current.error).toBe(mockError);
    expect(result.current.loading).toBe(false);
  });
});
