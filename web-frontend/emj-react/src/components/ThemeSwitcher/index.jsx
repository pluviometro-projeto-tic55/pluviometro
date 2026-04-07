import { useContext } from "react";
import { ThemeContext } from "../../context/ThemeContext";
import { Sun, Moon } from "lucide-react";
import "./style.css";

export default function ThemeSwitcher() {
  const { theme, toggleTheme } = useContext(ThemeContext);
  const isDark = theme === "dark";

  return (
    <button
      className={`theme-switcher ${isDark ? "dark" : "light"}`}
      onClick={toggleTheme}
      aria-label={isDark ? "Ativar tema claro" : "Ativar tema escuro"}
      aria-pressed={isDark} // indica que o tema escuro está ativo
    >
      <span className="theme-label">
        {isDark ? (
          <Sun size={18} color={"#fff"} />
        ) : (
          <Moon size={18} color={"#fff"} />
        )}
      </span>

      <span className="theme-handle">
        {isDark ? (
          <Moon size={18} color={"#fff"} />
        ) : (
          <Sun size={18} color={"#fff"} />
        )}
      </span>
    </button>
  );
}
