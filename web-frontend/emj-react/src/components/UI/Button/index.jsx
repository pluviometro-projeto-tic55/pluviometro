import clsx from "clsx";
import "./style.css";

export default function Button({
  children,
  variant = "primary",
  size = "md",
  fullWidth = false,
  disabled = false,
  className = "",
  "aria-label": ariaLabel, 
  "aria-pressed": ariaPressed, 
  ...props
}) {
  const classes = clsx(
    "btn",
    variant,
    size,
    fullWidth && "fullWidth",
    disabled && "disabled",
    className
  );

  return (
    <button
      className={classes}
      disabled={disabled}
      aria-label={ariaLabel}
      aria-pressed={ariaPressed}
      {...props} 
    >
      {children}
    </button>
  );
}
