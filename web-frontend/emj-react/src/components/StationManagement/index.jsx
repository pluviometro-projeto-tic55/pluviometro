import React, { useState, useEffect, useMemo, useCallback } from "react";
import { useStations } from "../../hooks/useStations";
import StationMap from "../StationMap";
import Modal, {
  ModalHeader,
  ModalBody,
  ModalFooter,
} from "../UI/Modal";
import { api } from "../../services/api";
import "./style.css";
import { MapPin, Mail, Phone, Globe, Mountain, Waves, Activity, Hash } from "lucide-react";


export default function StationManagement() {
  const { stations, loading, error } = useStations();

  const [selectedStation, setSelectedStation] = useState(null);
  const [modalStation, setModalStation] = useState(null);

  /* Login */
  const [user, setUser] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const [isLoadingLogin, setIsLoadingLogin] = useState(false);
  const [isLogged, setIsLogged] = useState(false);

  /* Dados da estação */
  const [stationDetails, setStationDetails] = useState(null);

  useEffect(() => {
    if (stations?.length && !selectedStation) {
      setSelectedStation(stations[0]);
    }
  }, [stations, selectedStation]);

  const orderedStations = useMemo(() => {
    if (!stations || !selectedStation) return stations || [];

    return [
      selectedStation,
      ...stations.filter((s) => s.id !== selectedStation.id),
    ];
  }, [stations, selectedStation]);

  const handleSelectStation = useCallback((station) => {
    setSelectedStation(station);
  }, []);

  const handleOpenModal = useCallback((station) => {
    setModalStation(station);
    setUser("");
    setPassword("");
    setLoginError("");
    setIsLogged(false);
  }, []);

  const handleCloseModal = useCallback(() => {
    setModalStation(null);
    setUser("");
    setPassword("");
    setLoginError("");
    setIsLoadingLogin(false);
    setIsLogged(false);
    setStationDetails(null);
  }, []);

  const handleLogin = async () => {
    setLoginError("");
    setIsLoadingLogin(true);

    try {
      const response = await api.post("api/auth/login", {
        email: user,
        password: password,
      });

      const { token } = response.data;

      localStorage.setItem("token", token);

      setIsLogged(true);

      await fetchStationDetails(token);

    } catch (error) {
      setLoginError("E-mail ou senha inválidos.");
    } finally {
      setIsLoadingLogin(false);
    }
  };

  const fetchStationDetails = async (token) => {
    try {
      const response = await api.get("/api/stations/details", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setStationDetails(response.data);
    } catch (error) {
      console.error("Erro ao buscar detalhes:", error);
    }
  };

  if (loading) {
    return <div className="loading-state">Carregando...</div>;
  }

  if (error) {
    return (
      <div className="error-state">
        Erro ao carregar estações: {error.message}
      </div>
    );
  }

  return (
    <div className="management-wrapper">
      <header className="management-header">
        <h1>Gestão de Estações Meteorológicas - Porto Alegre</h1>
      </header>

      <section className="station-content">
        <aside className="sidebar">
          <h3 className="sidebar-title">Estações Disponíveis</h3>

          <div className="list-scroll">
            {orderedStations?.map((station) => (
              <div
                key={station.id}
                className={`station-card ${
                  selectedStation?.id === station.id ? "active-card" : ""
                }`}
                onClick={() => handleSelectStation(station)}>
                <h4>{station.label}</h4>

                <div className="card-coords">
                  Lat: {station.lat?.toFixed(4)} | Long:{" "}
                  {station.lng?.toFixed(4)}
                </div>

                <button
                  className="btn-ver-mais"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleOpenModal(station);
                  }}>
                  Ver mais
                </button>
              </div>
            ))}
          </div>
        </aside>

        <div className="map-area">
          <StationMap
            stations={stations}
            selectedStation={selectedStation}
            onMarkerClick={handleSelectStation}
          />
        </div>
      </section>

      <Modal isOpen={!!modalStation} onClose={handleCloseModal}>
        <ModalHeader>
          {modalStation && (
            <div>
              <div>Acesso à Estação</div>
              <div>{modalStation.label}</div>
            </div>
          )}
        </ModalHeader>

        <ModalBody>
          {!isLogged && (
            <div className="station-modal-body text-(--text-800)">
              <p>Insira suas credenciais para acessar.</p>

              {loginError && <p className="text-red-600">{loginError}</p>}

              <label>E-mail</label>
              <input
                type="text"
                value={user}
                onChange={(e) => setUser(e.target.value)}
              />

              <label>Senha</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          )}

          {isLogged && stationDetails && (
            <>
              <h3 className="text-sm py-2! font-semibold text-(--text-800) uppercase tracking-wide">
                Dados da Estação
              </h3>

              <div className="max-h-[60vh] overflow-y-auto pr-2">
                <div className="grid md:grid-cols-2 gap-8">
                  {/* COLUNA ESQUERDA */}
                  <div className="p-6! space-y-6!">
                    <div className="flex items-start gap-4">
                      <Hash className="w-5 h-5 text-(--text-600) mt-1!" />
                      <div>
                        <p className="text-xs text-(--text-600)">Nome</p>
                        <p className="text-sm font-medium text-(--text-800)">
                          {stationDetails[0]?.name}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-start gap-4">
                      <Globe className="w-5 h-5 text-(--text-600) mt-1!" />
                      <div>
                        <p className="text-xs text-(--text-600)">Local</p>
                        <p className="text-sm font-medium text-(--text-800)">
                          {stationDetails[0]?.local}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-start gap-4">
                      <Mail className="w-5 h-5 text-(--text-600) mt-1!" />
                      <div>
                        <p className="text-xs text-(--text-600)">E-mail</p>
                        <p className="text-sm font-medium text-(--text-800)">
                          {stationDetails[0]?.email}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-start gap-4">
                      <Phone className="w-5 h-5 text-(--text-600) mt-1!" />
                      <div>
                        <p className="text-xs text-(--text-600)">Contato</p>
                        <p className="text-sm font-medium text-(--text-800)">
                          {stationDetails[0]?.contact}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* COLUNA DIREITA */}
                  <div className="p-6! space-y-6!">
                    {/* Status */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <Activity className="w-5 h-5 text-(--text-600)" />
                        <p className="text-sm text-(--text-600)">Status</p>
                      </div>

                      <span
                        className={`px-3! py-1! text-xs font-semibold rounded-full flex items-center gap-2
                        ${
                          status === "online"
                            ? "bg-emerald-100 text-emerald-700"
                            : "bg-red-100 text-red-700"
                        }`}>
                        <span className="w-2 h-2 rounded-full bg-current"></span>
                        {stationDetails[0]?.status}
                      </span>
                    </div>

                    {/* Coordenadas */}
                    <div className=" pt-5! grid grid-cols-2 gap-6">
                      <div className="flex gap-3">
                        <MapPin className="w-4 h-4 text-(--text-600) mt-1!" />
                        <div>
                          <p className="text-xs text-(--text-600)">Latitude</p>
                          <p className="text-sm font-medium text-(--text-800)">
                            {stationDetails[0]?.latitude}
                          </p>
                        </div>
                      </div>

                      <div className="flex gap-3">
                        <MapPin className="w-4 h-4 text-(--text-600) mt-1!" />
                        <div>
                          <p className="text-xs text-(--text-600)">Longitude</p>
                          <p className="text-sm font-medium text-(--text-800)">
                            {stationDetails[0]?.longitude}
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Altura */}
                    <div className="pt-5 grid grid-cols-2 gap-6">
                      <div className="flex gap-3">
                        <Mountain className="w-4 h-4 text-(--text-600) mt-1" />
                        <div>
                          <p className="text-xs text-(--text-600)">Altura</p>
                          <p className="text-sm font-medium text-(--text-800)">
                            {stationDetails[0]?.height}
                          </p>
                        </div>
                      </div>

                      <div className="flex gap-3">
                        <Waves className="w-4 h-4 text-(--text-600) mt-1" />
                        <div>
                          <p className="text-xs text-(--text-600)">
                            Nível do mar
                          </p>
                          <p className="text-sm font-medium text-(--text-800)">
                            {stationDetails[0]?.height_sea_level}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}
        </ModalBody>

        <ModalFooter>
          {!isLogged && (
            <>
              <button className="btn-cancelar" onClick={handleCloseModal}>
                Cancelar
              </button>

              <button
                className="btn-entrar"
                onClick={handleLogin}
                disabled={!user || !password || isLoadingLogin}>
                {isLoadingLogin ? "Entrando..." : "Entrar"}
              </button>
            </>
          )}

          {isLogged && (
            <button className="btn-entrar" onClick={handleCloseModal}>
              Fechar
            </button>
          )}
        </ModalFooter>
      </Modal>
    </div>
  );
}