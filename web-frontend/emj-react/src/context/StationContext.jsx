import { createContext, useContext, useEffect, useState } from "react";
import { useStations } from "../hooks/useStations";

const StationContext = createContext();

export function StationProvider({ children }) {
  const { stations, loading } = useStations();
  const [selectedStation, setSelectedStation] = useState(null);

  useEffect(() => {
    if (!selectedStation && stations.length > 0) {
      setSelectedStation(stations[0]);
    }
  }, [stations, selectedStation]);

  const stationId = selectedStation?.value;

  return (
    <StationContext.Provider
      value={{
        stations,
        stationsLoading: loading,
        selectedStation,
        setSelectedStation,
        stationId,
      }}>
      {children}
    </StationContext.Provider>
  );
}

export function useStation() {
  return useContext(StationContext);
}
