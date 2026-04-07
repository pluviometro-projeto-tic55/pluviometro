import { useEffect, useState, useRef } from "react";
import { ChevronDown } from "lucide-react";
import "./style.css";

export default function Dropdown({
  icon: Icon,
  options = [],
  value,
  onChange,
  className = "",
}) {
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState(value || options[0] || null);
  const ref = useRef(null);

  // Inicializa selecionado
  useEffect(() => {
    if (!value && options.length > 0) {
      setSelected(options[0]);
    }
  }, [options]);

  useEffect(() => {
    if (value) setSelected(value);
  }, [value]);

  // Fecha dropdown clicando fora
  useEffect(() => {
    function handleClickOutside(e) {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  function handleSelect(option) {
    setSelected(option);
    onChange?.(option);
    setOpen(false);
  }

  // Ações de teclado
  const handleKeyDownTrigger = (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      setOpen(!open);
    }
  };

  const handleKeyDownItem = (e, option) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleSelect(option);
    }
  };

  return (
    <div ref={ref} className={`dropdown ${className}`}>
      {/* Botão */}
      <button
        className="dropdown-trigger"
        onClick={() => setOpen(!open)}
        onKeyDown={handleKeyDownTrigger}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-label={`Selecionar estação: ${selected?.label || "nenhuma"}`}
      >
        <div className="dropdown-left">
          {Icon && <Icon size={20} className="dropdown-trigger-icon" />}
          <span
            className="dropdown-label"
            title={selected ? selected.label : ""}
          >
            {selected?.label}
          </span>
        </div>

        <ChevronDown
          size={16}
          className={`dropdown-arrow ${open ? "open" : ""}`}
          aria-hidden="true"
        />
      </button>

      {/* Menu de opções */}
      <div
        className={`dropdown-menu ${open ? "open" : ""}`}
        role="listbox"
        aria-activedescendant={selected?.value}
        tabIndex={-1}
      >
        {options.map((option) => (
          <button
            key={option.value}
            className="dropdown-item"
            role="option"
            aria-selected={selected?.value === option.value}
            onClick={() => handleSelect(option)}
            onKeyDown={(e) => handleKeyDownItem(e, option)}
            tabIndex={0}
            id={option.value}
          >
            <span className="dropdown-item-label" title={option.label}>
              {option.label}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
