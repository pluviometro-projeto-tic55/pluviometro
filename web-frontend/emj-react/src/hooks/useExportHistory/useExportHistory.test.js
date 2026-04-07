import { renderHook, act } from "@testing-library/react";
import { useExportHistoryCSV } from "./index";
import { useApi } from "../useAPI";
import { vi } from "vitest";

vi.mock("../useAPI");

describe("useExportHistoryCSV", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    document.body.innerHTML = "";
  });

    it("deve chamar API com parâmetros corretos", async () => {
        const mockResponse = {
            data: "csv content",
            headers: {
                "content-disposition": 'attachment; filename="file.csv"',
            },
        };

        const mockRequest = vi.fn().mockResolvedValue(mockResponse);

        useApi.mockReturnValue({
            request: mockRequest,
            loading: false,
            error: null,
        });

        vi.spyOn(URL, "createObjectURL").mockReturnValue("blob:url");
        vi.spyOn(URL, "revokeObjectURL").mockImplementation(() => {});
        vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(() => {});

        const { result } = renderHook(() => useExportHistoryCSV());

        await act(async () => {
        await result.current.exportCSV({
            stationId: 1,
            variable: "temp",
            startDate: "2024-01-01",
            endDate: "2024-01-02",
        });
        });

        expect(mockRequest).toHaveBeenCalledWith({
        method: "get",
        url: "/api/stations/1/history/export",
        params: {
            rc_id: 1,
            variable: "temp",
            start_date: "2024-01-01",
            end_date: "2024-01-02",
        },
        responseType: "blob",
        });

        expect(URL.createObjectURL).toHaveBeenCalled();
        expect(HTMLAnchorElement.prototype.click).toHaveBeenCalled();
        expect(URL.revokeObjectURL).toHaveBeenCalled();
    });

    it("deve usar nome padrão se não houver content-disposition", async () => {
        const mockResponse = {
            data: "csv content",
            headers: {},
        };

        const mockRequest = vi.fn().mockResolvedValue(mockResponse);

        useApi.mockReturnValue({
            request: mockRequest,
            loading: false,
            error: null,
        });

        vi.spyOn(URL, "createObjectURL").mockReturnValue("blob:url");
        vi.spyOn(URL, "revokeObjectURL").mockImplementation(() => {});
        vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(() => {});

        let createdAnchor = null;

        const originalCreateElement = document.createElement;

        vi.spyOn(document, "createElement").mockImplementation((tagName) => {
            const element = originalCreateElement.call(document, tagName);

            if (tagName === "a") {
            createdAnchor = element;
            }

            return element;
        });

        const { result } = renderHook(() => useExportHistoryCSV());

        await act(async () => {
            await result.current.exportCSV({
            stationId: 1,
            variable: "temp",
            startDate: "2024-01-01",
            });
        });

        expect(createdAnchor).not.toBeNull();
        expect(createdAnchor.download).toBe("export.csv");
    });

});
