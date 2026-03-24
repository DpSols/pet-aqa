import allure

from src.api.client import PetstoreClient
from src.api.models.pet import Pet


class PetSteps:

    def __init__(self, client: PetstoreClient) -> None:

        self._client = client

    @allure.step("Create pet and verify")
    def create_pet_and_verify(self, pet_data: dict) -> Pet:

        pet = Pet(**pet_data)
        created = self._client.add_pet(pet)
        assert created.id is not None, "Created pet should have an ID"
        assert created.name == pet.name, f"Expected name {pet.name}, got {created.name}"
        return created

    @allure.step("Update pet and verify")
    def update_pet_and_verify(self, pet: Pet) -> Pet:

        assert pet.id is not None, "Pet must have ID to update"
        updated = self._client.update_pet(pet)
        assert updated.id == pet.id, f"Pet ID should remain {pet.id}"
        return updated

    @allure.step("Delete pet and verify")
    def delete_pet_and_verify(self, pet_id: int) -> None:

        self._client.delete_pet(pet_id)
        try:
            self._client.get_pet(pet_id)
            raise AssertionError(f"Pet {pet_id} should be deleted but was found")
        except Exception as e:
            if "404" not in str(e):
                raise
