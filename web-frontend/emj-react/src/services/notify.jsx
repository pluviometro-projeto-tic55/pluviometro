import toast from "react-hot-toast";
import { Toast } from "../components/UI/Toast";

export const notify = {
  success: (msg) =>
    toast.custom((t) => <Toast type="success" message={msg} t={t} />),

  error: (msg) =>
    toast.custom((t) => <Toast type="error" message={msg} t={t} />),

  warning: (msg) =>
    toast.custom((t) => <Toast type="warning" message={msg} t={t} />),
};
