from unittest.mock import Mock

import allure
import pytest

from src.api.client import PetstoreClient
from src.api.models.pet import Pet


@allure.feature("Petstore API")
@allure.story("API Client")
@pytest.mark.api
class TestPetstoreClient:

    @pytest.fixture
    def mock_session(self) -> Mock:
        return Mock()

    @pytest.fixture
    def client(self, mock_session: Mock) -> PetstoreClient:
        return PetstoreClient(session=mock_session, base_url="https://api.example.com")

    @allure.title("Can create a pet")
    def test_add_pet(self, client: PetstoreClient, mock_session: Mock) -> None:
        pet_data = {"id": 123, "name": "Fido", "status": "available"}
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = pet_data
        mock_session.post.return_value = mock_response

        pet_input = Pet(**pet_data)
        result = client.add_pet(pet_input)

        assert result.id == 123
        assert result.name == "Fido"
        assert result.status == "available"
        mock_session.post.assert_called_once()

    @allure.title("Can retrieve a pet")
    def test_get_pet(self, client: PetstoreClient, mock_session: Mock) -> None:
        pet_data = {"id": 123, "name": "Fido", "status": "available"}
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = pet_data
        mock_session.get.return_value = mock_response

        result = client.get_pet(123)

        assert result.id == 123
        assert result.name == "Fido"
        mock_session.get.assert_called_once()

    @allure.title("Raises error on API failure")
    def test_api_error_handling(self, client: PetstoreClient, mock_session: Mock) -> None:
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_session.get.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            client.get_pet(999)

        assert "404" in str(exc_info.value)

    @allure.title("Can update a pet")
    def test_update_pet(self, client: PetstoreClient, mock_session: Mock) -> None:
        pet_data = {"id": 123, "name": "Fido", "status": "sold"}
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = pet_data
        mock_session.put.return_value = mock_response

        pet_input = Pet(**pet_data)
        result = client.update_pet(pet_input)

        assert result.status == "sold"
        mock_session.put.assert_called_once()

    @allure.title("Can delete a pet")
    def test_delete_pet(self, client: PetstoreClient, mock_session: Mock) -> None:
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"code": 200, "message": "ok"}
        mock_session.delete.return_value = mock_response

        result = client.delete_pet(123)

        assert result.code == 200
        mock_session.delete.assert_called_once()
