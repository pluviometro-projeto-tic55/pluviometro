import React, { useEffect, useRef, useMemo } from "react";
import Map, { Marker, NavigationControl } from "react-map-gl/maplibre";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import "./style.css";

export default function StationMap({
  stations = [],
  selectedStation,
  onMarkerClick,
}) {
  const mapRef = useRef(null);

  /* Primeira estação válida */
  const firstStation = useMemo(() => {
    return stations.find(
      (s) =>
        typeof s.lat === "number" &&
        typeof s.lng === "number" &&
        !isNaN(s.lat) &&
        !isNaN(s.lng)
    );
  }, [stations]);

  /* Centraliza quando o mapa carrega */
  const handleMapLoad = () => {
    if (!mapRef.current || !firstStation) return;

    mapRef.current.flyTo({
      center: [firstStation.lng, firstStation.lat],
      zoom: 13,
      speed: 1.2,
      essential: true,
    });
  };

  /* Centraliza quando seleciona a estação */
  useEffect(() => {
    if (!mapRef.current || !selectedStation) return;

    mapRef.current.flyTo({
      center: [selectedStation.lng, selectedStation.lat],
      zoom: 14,
      speed: 1.2,
      essential: true,
    });
  }, [selectedStation]);

  useEffect(() => {
    const timer = setTimeout(() => {
      mapRef.current?.getMap()?.resize();
    }, 300);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="map-container">
      <Map
        ref={mapRef}
        mapLib={maplibregl}
        mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
        style={{ width: "100%", height: "100%" }}
        onLoad={handleMapLoad}
      >
        <NavigationControl position="top-right" />

        {stations
          .filter(
            (s) =>
              typeof s.lat === "number" &&
              typeof s.lng === "number" &&
              !isNaN(s.lat) &&
              !isNaN(s.lng)
          )
          .map((station) => (
            <Marker
              key={station.id}
              latitude={station.lat}
              longitude={station.lng}
              anchor="bottom"
            >
              <div
                className="marker-wrapper"
                onClick={() => onMarkerClick(station)}
              >
                {/* Tooltip */}
                <div className="marker-tooltip">
                  <strong>{station.label}</strong>

                  <div>Lat: {station.lat.toFixed(4)}</div>
                  <div>Long: {station.lng.toFixed(4)}</div>
                </div>

                {/* Animação */}
                <div className="marker-pulse" />

                {/* Marker */}
                <div
                  className={`custom-marker ${
                    selectedStation?.id === station.id ? "blue" : "gray"
                  }`}
                >
                  <div className="marker-inner-dot" />
                </div>
              </div>
            </Marker>
          ))}
      </Map>
    </div>
  );
}
