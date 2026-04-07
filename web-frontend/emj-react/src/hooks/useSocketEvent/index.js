import { useEffect } from "react";
import socket from "../../services/socket";

export function useSocketEvent(eventName, handler) {
  useEffect(() => {
    if (!eventName) return;

    socket.on(eventName, handler);

    return () => {
      socket.off(eventName, handler);
    };
  }, [eventName, handler]);
}
