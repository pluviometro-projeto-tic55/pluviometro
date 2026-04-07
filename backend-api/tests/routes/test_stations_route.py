from unittest.mock import patch

BASE_URL = "/stations"

#Retorna 200 e lista de estações
def test_list_stations_success(client):
    fake_stations = [
        {"rcId": 1, "name": "Estação 1", "local": "Local 1"},
        {"rcId": 2, "name": "Estação 2", "local": "Local 2"},
    ]

    with patch(
        "src.routes.get_all_stations",
        return_value=fake_stations
    ) as mock_service:

        response = client.get(BASE_URL)

        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == fake_stations

        mock_service.assert_called_once()

#Retorna 404 quando não há estações
def test_list_stations_not_found(client):
    with patch(
        "src.routes.get_all_stations",
        return_value=None
    ) as mock_service:

        response = client.get(BASE_URL)

        assert response.status_code == 404
        assert response.is_json

        body = response.get_json()
        assert "message" in body

        mock_service.assert_called_once()

#Chama corretamente o serviço get_all_stations
def test_list_stations_calls_get_all_stations(client):
    with patch(
        "src.routes.get_all_stations",
        return_value=[]
    ) as mock_service:

        client.get(BASE_URL)

        mock_service.assert_called_once()



#Retorna 500 quando o service lança exceção
def test_list_stations_internal_error(client):
    with patch(
        "src.routes.get_all_stations",
        side_effect=Exception("DB error")
    ) as mock_service:

        response = client.get(BASE_URL)

        assert response.status_code == 500
        assert response.is_json

        body = response.get_json()
        assert "error" in body

        mock_service.assert_called_once()

#Garante resposta em JSON
def test_list_stations_returns_json(client):
    with patch(
        "src.routes.get_all_stations",
        return_value=[]
    ):
        response = client.get(BASE_URL)

        assert response.content_type == "application/json"
