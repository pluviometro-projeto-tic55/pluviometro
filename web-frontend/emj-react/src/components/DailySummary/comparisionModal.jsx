import Modal, { ModalBody, ModalFooter, ModalHeader } from "../UI/Modal";
import Button from "../UI/Button";
import Table from "../UI/Table";
import VariationBadge from "../UI/VariationBadge";
import { Dot } from "lucide-react";
import PropTypes from "prop-types";

function ComparisonModal({isOpen, onClose, weather, externalData}) {
    const columns = [
        { label: "Parâmetro", key: "summary" },
        { label: "Sensor Local", key: "local" },
        { label: "API Externa", key: "owm" },
        {
          label: "Variação Local",
          key: "error",
          render: (value) => <VariationBadge value={value} />,
        },
      ];

    const dataTable = [
        {
          summary: "Temperatura",
          local: `${Math.round(weather?.temperature ?? 0)} °C`,
          owm: `${Math.round(externalData?.external_temperature ?? 0)} °C`,
          error: parseFloat(((weather?.temperature ?? 0) - (externalData?.external_temperature ?? 0)).toFixed(1)),
        },
        {
          summary: "Umidade",
          local: `${Math.round(weather?.humidity ?? 0)}%`,
          owm: `${Math.round(externalData?.external_humidity ?? 0)}%`,
          error: parseFloat(((weather?.humidity ?? 0) - (externalData?.external_humidity ?? 0)).toFixed(0)),
        },
        {
          summary: "Pressão",
          local: `${Math.round(weather?.pressure ?? 0)} hPa`,
          owm: `${Math.round(externalData?.external_pressure ?? 0)} hPa`,
          error: parseFloat(((weather?.pressure ?? 0) - (externalData?.external_pressure ?? 0)).toFixed(0)),
        },
        {
          summary: "Vento",
          local: `${Math.round(weather?.wind_speed ?? 0)} km/h`,
          owm: `${Math.round(externalData?.external_wind_speed ?? 0)} km/h`,
          error: parseFloat(((weather?.wind_speed ?? 0) - (externalData?.external_wind_speed ?? 0)).toFixed(1)),
        },
        {
          summary: "Chuva",
          local: `${Math.round(weather?.rain_mm ?? 0)} mm`,
          owm: `${Math.round(externalData?.external_rain_mm ?? 0)} mm`,
          error: null,
        },
        {
          summary: "Iluminância",
          local: weather?.luminosity != null ? `${Math.round(weather.luminosity)} Lux` : "-",
          owm: `0 Lux`,
          error: weather?.luminosity != null ? parseFloat((weather.luminosity - 0).toFixed(1)) : null,
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
  weather: PropTypes.object,
  externalData: PropTypes.object,
};