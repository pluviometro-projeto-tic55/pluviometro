from unittest.mock import patch

BASE_URL = "/data/details"

#Retorna detalhes da estação com sucesso
def test_get_station_details_success(client):
    fake_response = {
        "rcID": 1,
        "temperature": 25,
        "humidity": 70
    }

    with patch(
        "src.routes.get_station_data_by_id",
        return_value=fake_response
    ) as mock_service:

        response = client.get(f"{BASE_URL}/1")

        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == fake_response

        mock_service.assert_called_once_with(1)

#Retorna 404 para estação inexistente
def test_get_station_details_not_found(client):
    with patch(
        "src.routes.get_station_data_by_id",
        return_value=None
    ) as mock_service:

        response = client.get(f"{BASE_URL}/999")

        assert response.status_code == 404
        assert response.is_json
        assert "error" in response.get_json()

        mock_service.assert_called_once_with(999)

#Chama corretamente o serviço get_station_data_by_id
def test_route_calls_service_with_correct_id(client):
    with patch(
        "src.routes.get_station_data_by_id",
        return_value={"ok": True}
    ) as mock_service:

        client.get(f"{BASE_URL}/5")

        mock_service.assert_called_once_with(5)

#Retorna resposta no formato JSON
def test_get_station_details_returns_json(client):
    with patch(
        "src.routes.get_station_data_by_id",
        return_value={"key": "value"}
    ):
        response = client.get(f"{BASE_URL}/1")

        assert response.is_json
        assert response.content_type == "application/json"
