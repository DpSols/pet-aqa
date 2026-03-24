import uuid

import allure
import pytest

from src.steps.api_steps import PetSteps
from src.steps.infra_steps import InfraSteps


@allure.feature("Petstore API")
@allure.story("Pet CRUD Lifecycle")
@pytest.mark.api
class TestPetLifecycle:

    @allure.title("Create, read, update, delete a pet with DB persistence and Kafka")
    def test_create_read_update_delete_pet(
        self,
        pet_steps: PetSteps,
        infra_steps: InfraSteps,
    ) -> None:
        pet_data = {
            "id": int(uuid.uuid4().int % (2**31)),
            "name": "TestDog",
            "status": "available",
            "category": {"id": 1, "name": "Dogs"},
        }
        pet = pet_steps.create_pet_and_verify(pet_data)
        assert pet.name == "TestDog", "Pet name should match"

        persisted_pet = infra_steps.persist_pet(pet)
        assert persisted_pet.id == pet.id, "Persisted pet ID should match"

        found_pet = infra_steps.assert_pet_in_db(pet.id)
        assert found_pet.name == pet.name, "Found pet should match persisted pet"

        infra_steps.publish_pet_event("pet-events", pet)

        pet.status = "sold"
        updated_pet = pet_steps.update_pet_and_verify(pet)
        assert updated_pet.status == "sold", "Pet status should be updated to sold"

        pet_steps.delete_pet_and_verify(pet.id)
