import { useState, useEffect } from "react";
import { Menu, X, MapPin } from "lucide-react";
import { useLocation, useNavigate } from "react-router-dom";
import Dropdown from "../Dropdown";
import Button from "../Button";
import ThemeSwitcher from "../../ThemeSwitcher";
import logoJoao from "../../../assets/logo.png";
import "./style.css";
import { useStation } from "../../../context/StationContext";

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  //Detecta se é desktop
  const [isDesktop, setIsDesktop] = useState(
    window.matchMedia("(min-width: 768px)").matches
  );

  const { stations, selectedStation, setSelectedStation } = useStation();

  const location = useLocation();
  const navigate = useNavigate();

  const toggleRoute = () => {
    if (location.pathname === "/advanced") {
      navigate("/");
    } else {
      navigate("/advanced");
    }
    setMenuOpen(false);
  };

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(min-width: 768px)");

    const handleChange = (e) => {
      setIsDesktop(e.matches);
      if (e.matches) {
        setMenuOpen(false); 
      }
    };

    mediaQuery.addEventListener("change", handleChange);

    return () => {
      mediaQuery.removeEventListener("change", handleChange);
    };
  }, []);

  return (
    <>
      <header
        className={`navbar ${scrolled ? "scrolled" : ""}`}
        role="navigation"
      >
        <div className="navbar-left">
          <img
            src={logoJoao}
            alt="Colégio João XXIII"
            className="navbar-logo"
          />
        </div>

        <div className="navbar-actions">
          <div style={{ width: "230px" }}>
            <Dropdown
              icon={MapPin}
              options={stations}
              value={selectedStation}
              onChange={setSelectedStation}
            />
          </div>

          {/* Botão desktop */}
          {isDesktop && (
            <Button variant="primary" onClick={toggleRoute}>
              {location.pathname === "/advanced"
                ? "Previsão Resumida"
                : "Previsão Completa"}
            </Button>
          )}

          <ThemeSwitcher />
        </div>

  
        <button
          className="menu-toggle"
          aria-label={menuOpen ? "Fechar menu" : "Abrir menu"}
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((prev) => !prev)}
        >
          {menuOpen ? <X size={26} /> : <Menu size={26} />}
        </button>
      </header>

      {/* Mobile Menu  */}
      <div className={`mobile-menu ${menuOpen ? "open" : ""}`}>
        <div className="w-full">
          <Dropdown
            icon={MapPin}
            options={stations}
            value={selectedStation}
            onChange={setSelectedStation}
          />
        </div>

        <ThemeSwitcher />
      </div>
    </>
  );
}