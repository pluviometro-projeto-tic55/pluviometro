import React, { useEffect, useState } from "react";
import { X } from "lucide-react";
import "./style.css";
import Button from "../Button";

export const ModalHeader = ({ children }) => (
  <div className="modal-header-inner">{children}</div>
);
export const ModalBody = ({ children }) => (
  <div className="modal-body-inner">{children}</div>
);
export const ModalFooter = ({ children }) => (
  <div className="modal-footer-inner">{children}</div>
);

const Modal = ({ isOpen, onClose, children, blurIntensity = 6 }) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setVisible(true);
      document.body.style.overflow = "hidden";
    } else {
      const t = setTimeout(() => setVisible(false), 300);
      document.body.style.overflow = "unset";
      return () => clearTimeout(t);
    }
  }, [isOpen]);

  useEffect(() => {
    if (!visible) return;
    const handleKey = (e) => {
      if (e.key === "Escape" || e.key === "Esc") {
        onClose();
      }
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [visible, onClose]);

  if (!visible) return null;

  const header = React.Children.toArray(children).find(
    (c) => c && c.type === ModalHeader
  );
  const body = React.Children.toArray(children).find(
    (c) => c && c.type === ModalBody
  );
  const footer = React.Children.toArray(children).find(
    (c) => c && c.type === ModalFooter
  );

  return (
    <div
      className={`modal-overlay ${isOpen ? "open" : "closing"}`}
      onClick={onClose}>
      <div
        className="modal-backdrop"
        style={{
          backdropFilter: `blur(${isOpen ? blurIntensity : 0}px)`,
          WebkitBackdropFilter: `blur(${isOpen ? blurIntensity : 0}px)`,
          opacity: isOpen ? 1 : 0,
        }}
      />

      <div
        className={`modal-content ${isOpen ? "modal-in" : "modal-out"}`}
        onClick={(e) => e.stopPropagation()}
        role="dialog">
        <div className="modal-header">
          {header}

          <Button variant="close" size="sm" onClick={onClose}>
            <X size={20} stroke="var(--text-600)" />
          </Button>
        </div>

        {body}

        {footer || null}
      </div>
    </div>
  );
};

export default Modal;
