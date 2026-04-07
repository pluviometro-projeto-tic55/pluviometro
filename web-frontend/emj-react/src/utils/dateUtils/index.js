export function getFormattedDate(dateString) {
  let date;

  if (dateString) {
    // Detecta formato ISO: YYYY-MM-DD 
    if (dateString.includes("-")) {
      const [year, month, day] = dateString.split("-").map(Number);
      date = new Date(year, month - 1, day);
    }
  } else {
    date = new Date();
  }

  let dayOfWeek = date
    .toLocaleDateString("pt-BR", { weekday: "long" })
    .replace("-feira", "")
    .trim();

  dayOfWeek = dayOfWeek.charAt(0).toUpperCase() + dayOfWeek.slice(1);

  let fullDayOfWeek = date
    .toLocaleDateString("pt-BR", { weekday: "long" })
    .trim();

  fullDayOfWeek = fullDayOfWeek.charAt(0).toUpperCase() + fullDayOfWeek.slice(1);

  const day = date.getDate().toString().padStart(2, "0");
  const monthNumber = (date.getMonth() + 1).toString().padStart(2, "0");

  const monthName =
    date
      .toLocaleDateString("pt-BR", { month: "long" })
      .charAt(0)
      .toUpperCase() +
    date.toLocaleDateString("pt-BR", { month: "long" }).slice(1);

  const year = date.getFullYear();

  return {
    fullDayOfWeek,
    dayOfWeek,
    shortDate: `${day}/${monthNumber}`,
    formattedDate: `${day} de ${monthName}, ${year}`,
  };
}

export function formatDayMonth(dateStr) {
  const [year, month, day] = dateStr.split("-").map(Number);
  const date = new Date(year, month - 1, day);

  const formatted = date.toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "short",
  });

  return formatted.replace(".", "").replace(/^\w/, c => c.toUpperCase());
}
