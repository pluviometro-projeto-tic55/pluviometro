import { useState, useRef, useEffect } from "react";
import { Calendar } from "lucide-react";
import "./style.css";

const MONTHS = [
  "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
];

export default function DateRangePicker({ onChange }) {
  const TODAY = new Date();
  const START_YEAR = 2026;
  const CURRENT_YEAR = TODAY.getFullYear();
  const CURRENT_MONTH = TODAY.getMonth();
  const CURRENT_DAY = TODAY.getDate();

  const [isOpen, setIsOpen] = useState(false);
  const [month, setMonth] = useState(CURRENT_MONTH);
  const [year, setYear] = useState(CURRENT_YEAR);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const pickerRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (pickerRef.current && !pickerRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const years = Array.from(
    { length: CURRENT_YEAR - START_YEAR + 1 },
    (_, i) => START_YEAR + i
  );

  const totalDaysInMonth = new Date(year, month + 1, 0).getDate();
  const daysInMonth =
    year === CURRENT_YEAR && month === CURRENT_MONTH
      ? CURRENT_DAY
      : totalDaysInMonth;

  const firstWeekDay = new Date(year, month, 1).getDay();

  // Garante que não é possível selecionar um mês inválido ao trocar de ano
  const handleYearChange = (newYear) => {
    setYear(newYear);
    if (newYear === CURRENT_YEAR && month > CURRENT_MONTH) {
      setMonth(CURRENT_MONTH);
    }
  };

  const handleSelectDay = (day) => {
    const selected = new Date(year, month, day);

    if (!startDate || endDate) {
      setStartDate(selected);
      setEndDate(null);
    } else if (selected < startDate) {
      setStartDate(selected);
    } else {
      setEndDate(selected);
    }
  };

  const handleClear = () => {
    setStartDate(null);
    setEndDate(null);
    onChange?.({ startDate: null, endDate: null });
  };

  const handleConfirm = () => {
    if (startDate) {
      const selectedRange = { 
        startDate: startDate, 
        endDate: endDate || startDate 
      };
      onChange?.(selectedRange); 
      setIsOpen(false); 
    }
  };

  const formatLabel = () => {
    if (!startDate) return "Selecione o período";
    const startStr = `${startDate.getDate()} ${MONTHS[startDate.getMonth()].slice(0,3)}`;
    if (!endDate) return startStr;
    const endStr = `${endDate.getDate()} ${MONTHS[endDate.getMonth()].slice(0,3)}`;
    return `${startStr} - ${endStr}`;
  };

  const isSameDay = (date, day) =>
    date &&
    date.getDate() === day &&
    date.getMonth() === month &&
    date.getFullYear() === year;

  const isInRange = (day) => {
    if (!startDate || !endDate) return false;
    const d = new Date(year, month, day);
    return d > startDate && d < endDate;
  };

  return (
    <div className="date-picker-wrapper" ref={pickerRef}>
      <button className="date-input w-full" onClick={() => setIsOpen(!isOpen)}>
        {formatLabel()}
        <Calendar size={18} />
      </button>

      {isOpen && (
        <div className="calendar">
          <div className="calendar-header">
            <select value={month} onChange={(e) => setMonth(+e.target.value)}>
              {MONTHS.map((m, i) => (
                <option
                  key={m}
                  value={i}
                  disabled={year === CURRENT_YEAR && i > CURRENT_MONTH}>
                  {m}
                </option>
              ))}
            </select>

            <select
              value={year}
              onChange={(e) => handleYearChange(+e.target.value)}>
              {years.map((y) => (
                <option key={y} value={y}>
                  {y}
                </option>
              ))}
            </select>
          </div>

          <div className="week-days">
            {["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SÁB"].map((d) => (
              <span key={d}>{d}</span>
            ))}
          </div>

          <div className="days-grid">
            {Array.from({ length: firstWeekDay }).map((_, i) => (
              <span key={`e-${i}`} className="empty-slot" />
            ))}

            {Array.from({ length: daysInMonth }).map((_, i) => {
              const day = i + 1;
              return (
                <button
                  key={day}
                  type="button"
                  className={`day
                    ${isSameDay(startDate, day) ? "start" : ""}
                    ${isSameDay(endDate, day) ? "end" : ""}
                    ${isInRange(day) ? "range" : ""}`}
                  onClick={() => handleSelectDay(day)}>
                  {day}
                </button>
              );
            })}
          </div>

          <div className="calendar-footer">
            <button className="clear-btn" onClick={handleClear}>
              Limpar
            </button>
            <button
              className="ok-btn"
              onClick={handleConfirm}
              disabled={!startDate}>
              OK
            </button>
          </div>
        </div>
      )}
    </div>
  );
}