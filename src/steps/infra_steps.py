import allure

from core.protocols import MessageProducer, StorageRepository
from src.api.models.pet import Pet


class InfraSteps:

    def __init__(self, repo: StorageRepository[Pet], producer: MessageProducer) -> None:

        self._repo = repo
        self._producer = producer

    @allure.step("Persist pet to database")
    def persist_pet(self, pet: Pet) -> Pet:

        persisted = self._repo.save(pet)
        assert persisted.id == pet.id, "Persisted pet ID mismatch"
        return persisted

    @allure.step("Publish pet event to Kafka: {topic}")
    def publish_pet_event(self, topic: str, pet: Pet) -> None:

        pet_dict = pet.model_dump(mode="json")
        self._producer.produce(
            topic=topic,
            key=str(pet.id),
            value=pet_dict,
        )
        self._producer.flush()

    @allure.step("Assert pet in database: {pet_id}")
    def assert_pet_in_db(self, pet_id: int) -> Pet:

        pet = self._repo.find_by_id(pet_id)
        assert pet is not None, f"Pet {pet_id} not found in database"
        return pet
