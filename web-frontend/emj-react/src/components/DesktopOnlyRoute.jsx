import { Navigate } from "react-router-dom";
import { useEffect, useState } from "react";

export default function DesktopOnlyRoute({ children }) {
  const [isDesktop, setIsDesktop] = useState(window.innerWidth >= 768);

  useEffect(() => {
    const handleResize = () => {
      setIsDesktop(window.innerWidth >= 768);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  if (!isDesktop) {
    return <Navigate to="/" replace />;
  }

  return children;
}