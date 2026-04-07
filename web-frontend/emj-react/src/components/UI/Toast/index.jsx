import { CheckCircle, XCircle, AlertTriangle, X } from "lucide-react";
import toast from "react-hot-toast";

const ICONS = {
  success: CheckCircle,
  error: XCircle,
  warning: AlertTriangle,
};

const STYLES = {
  success: "text-emerald-500",
  error: "text-red-500",
  warning: "text-amber-500",
};

export function Toast({ type = "success", message, t }) {
  const Icon = ICONS[type];
  const style = STYLES[type];

  return (
    <div
      className={`
        relative flex items-center gap-3
        px-4! py-3! pr-10!
        rounded-xl
        min-w-70 max-w-sm
        backdrop-blur-md
        transition-all duration-300
        bg-white/80 text-gray-800 border border-gray-200
      `}
    >
      <Icon size={20} className={`shrink-0 ${style}`} />

      <span className="text-sm font-medium leading-snug">{message}</span>

      <button
        onClick={() => toast.dismiss(t.id)}
        className="
          absolute top-2 right-2
          p-1! rounded-md
          text-gray-400
          hover:text-gray-700 hover:bg-black/5
          transition
        "
        aria-label="Fechar notificação"
      >
        <X size={14} />
      </button>
    </div>
  );
}
