import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import { ThemeProvider } from "./context/ThemeContext.jsx";
import 'maplibre-gl/dist/maplibre-gl.css';
import "react-loading-skeleton/dist/skeleton.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>,
);
