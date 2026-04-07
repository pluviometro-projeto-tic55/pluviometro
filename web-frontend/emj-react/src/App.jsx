import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./style.css";
import Home from "./pages/Home";
import Advanced from "./pages/Advanced";
import DesktopOnlyRoute from "./components/DesktopOnlyRoute";
import { Toaster } from "react-hot-toast";
import { SkeletonTheme } from "react-loading-skeleton";
import { StationProvider } from "./context/StationContext";

function App() {
  return (
    <SkeletonTheme
      baseColor="var(--skeleton-base)"
      highlightColor="var(--skeleton-highlight)">
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
        }}
      />

      <BrowserRouter>
        <StationProvider>
          <Routes>
            {/* Home - disponível para todos */}
            <Route path="/" element={<Home />} />

            {/* Advanced - disponível apenas em desktop */}
            <Route
              path="/advanced"
              element={
                <DesktopOnlyRoute>
                  <Advanced />
                </DesktopOnlyRoute>
              }
            />

            {/* Fallback */}
            <Route path="*" element={<h1>Página Não Encontrada</h1>} />
          </Routes>
        </StationProvider>
      </BrowserRouter>
    </SkeletonTheme>
  );
}

export default App;