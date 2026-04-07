import Modal, { ModalBody, ModalFooter, ModalHeader } from "../UI/Modal";
import Button from "../UI/Button";
import Table from "../UI/Table";
import VariationBadge from "../UI/VariationBadge";
import { Dot } from "lucide-react";
import PropTypes from "prop-types";
import { errorPercent } from "../../utils/errorPercent";

function ComparisonModal({isOpen, onClose, weather, externalData}) {
    const columns = [
        { label: "Parâmetro", key: "summary" },
        { label: "Sensor Local", key: "local" },
        { label: "API Externa", key: "owm" },
        {
          label: "Margem de Erro",
          key: "error",
          render: (value) => <VariationBadge value={value} />,
        },
      ];

    const dataTable = [
        {
          summary: "Temperatura",
          local: `${Math.round(weather?.temperature)} °C`,
          owm: `${Math.round(externalData?.external_temperature)} °C`,
          error: errorPercent(
            weather?.temperature,
            externalData?.external_temperature,
          ),
        },
        {
          summary: "Umidade",
          local: `${Math.round(weather?.humidity)}%`,
          owm: `${Math.round(externalData?.external_humidity)}%`,
          error: errorPercent(
            weather?.humidity,
            externalData?.external_humidity,
          ),
        },
        {
          summary: "Pressão",
          local: `${Math.round(weather?.pressure)} hPa`,
          owm: `${Math.round(externalData?.external_pressure)} hPa`,
          error: errorPercent(
            weather?.pressure,
            externalData?.external_pressure,
          ),
        },
        {
          summary: "Vento",
          local: `${Math.round(weather?.wind_speed)} km/h`,
          owm: `${Math.round(externalData?.external_wind_speed)} km/h`,
          error: errorPercent(
            weather?.wind_speed,
            externalData?.external_wind_speed,
          ),
        },
        {
          summary: "Chuva",
          local: `${Math.round(weather?.rain_chance)}%`,
          owm: `${Math.round(externalData?.external_rain_chance)}%`,
          error: errorPercent(
            weather?.rain_chance,
            externalData?.external_rain_chance,
          ),
        },
      ];

    return (
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        blurIntensity={8}
        aria-labelledby="modal-comparacao-titulo"
        aria-describedby="modal-comparacao-descricao">
        <ModalHeader id="modal-comparacao-titulo">
          Comparação de dados
        </ModalHeader>

        <ModalBody id="modal-comparacao-descricao">
          <div className="flex flex-col gap-4">
            <span className="text-(--text-800) text-sm">
              Comparação de dados dos sensores locais em tempo real com os dados
              da API Externa.
            </span>

            <Table columns={columns} data={dataTable} />

            <div className="flex items-start bg-(--info-bg) border border-(--info-border) rounded-xl px-4! py-2! gap-2">
              <Dot stroke="#2563EB" className="shrink-0" />
              <span className="text-(--info-text) text-xs">
                Os valores locais apresentados correspondem às medições
                coletadas pelos sensores instalados nesta área de cobertura.
              </span>
            </div>
          </div>
        </ModalBody>

        <ModalFooter>
          <Button variant="primary" onClick={onClose}>
            Ok
          </Button>
        </ModalFooter>
      </Modal>
    );
}

export default ComparisonModal;

ComparisonModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  weather: PropTypes.array.isRequired,
  externalData: PropTypes.array.isRequired,
};
