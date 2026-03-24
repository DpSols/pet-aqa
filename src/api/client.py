from requests import Session
from loguru import logger

from src.api import ApiError
from src.api.endpoints import PET, STORE_ORDER, find_by_status, pet_by_id
from src.api.models.pet import Pet
from src.api.models.order import Order, ApiResponse


class PetstoreClient:
    def __init__(self, session: Session, base_url: str) -> None:
        self._session = session
        self._base_url = base_url
        self._logger = logger.bind(layer="api", component="petstore_client")
        self._logger.info(f"PetstoreClient initialized with base_url={base_url}")

    def add_pet(self, pet: Pet) -> Pet:
        url = f"{self._base_url}{PET}"
        data = pet.model_dump(mode="json", by_alias=True, exclude_none=True)

        self._logger.debug(f"POST {url} with data={data}")
        response = self._session.post(url, json=data)

        if not response.ok:
            raise ApiError(response.status_code, response.text)

        created_pet = Pet.model_validate(response.json())
        self._logger.debug(f"Pet created with id={created_pet.id}")
        return created_pet

    def get_pet(self, pet_id: int) -> Pet:
        url = f"{self._base_url}{pet_by_id(pet_id)}"
        self._logger.debug(f"GET {url}")
        response = self._session.get(url)

        if not response.ok:
            raise ApiError(response.status_code, response.text)

        pet = Pet.model_validate(response.json())
        self._logger.debug(f"Pet retrieved: id={pet.id}")
        return pet

    def update_pet(self, pet: Pet) -> Pet:
        url = f"{self._base_url}{PET}"
        data = pet.model_dump(mode="json", by_alias=True, exclude_none=True)

        self._logger.debug(f"PUT {url} with data={data}")
        response = self._session.put(url, json=data)

        if not response.ok:
            raise ApiError(response.status_code, response.text)

        updated_pet = Pet.model_validate(response.json())
        self._logger.debug(f"Pet updated: id={updated_pet.id}")
        return updated_pet

    def delete_pet(self, pet_id: int) -> ApiResponse:
        url = f"{self._base_url}{pet_by_id(pet_id)}"
        self._logger.debug(f"DELETE {url}")
        response = self._session.delete(url)

        if not response.ok:
            raise ApiError(response.status_code, response.text)

        api_response = ApiResponse.model_validate(response.json())
        self._logger.debug(f"Pet deleted: id={pet_id}")
        return api_response

    def find_pets_by_status(self, status: str) -> list[Pet]:
        url = f"{self._base_url}{find_by_status(status)}"
        params = {"status": status}

        self._logger.debug(f"GET {url} with params={params}")
        response = self._session.get(url, params=params)

        if not response.ok:
            raise ApiError(response.status_code, response.text)

        pets = [Pet.model_validate(item) for item in response.json()]
        self._logger.debug(f"Found {len(pets)} pets with status={status}")
        return pets

    def place_order(self, order: Order) -> Order:
        url = f"{self._base_url}{STORE_ORDER}"
        data = order.model_dump(mode="json", by_alias=True, exclude_none=True)

        self._logger.debug(f"POST {url} with data={data}")
        response = self._session.post(url, json=data)

        if not response.ok:
            raise ApiError(response.status_code, response.text)

        placed_order = Order.model_validate(response.json())
        self._logger.debug(f"Order placed: id={placed_order.id}, pet_id={placed_order.pet_id}")
        return placed_order
