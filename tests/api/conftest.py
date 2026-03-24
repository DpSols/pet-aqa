import pytest
import requests
from sqlalchemy.orm import Session, sessionmaker

from config.settings import Settings
from infrastructure.postgresql.models import PetModel
from infrastructure.postgresql.repository import PostgresRepository
from src.api.client import PetstoreClient
from src.api.models.pet import Pet
from src.steps.api_steps import PetSteps
from src.steps.infra_steps import InfraSteps


@pytest.fixture(scope="session", autouse=True)
def _run_migrations(apply_migrations) -> None:
    """Ensure migrations run for API tests."""
    pass


@pytest.fixture(scope="module")
def http_session(settings: Settings) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "Content-Type": "application/json",
        }
    )
    yield session
    session.close()


@pytest.fixture(scope="module")
def petstore_client(http_session: requests.Session, settings: Settings) -> PetstoreClient:
    return PetstoreClient(session=http_session, base_url=settings.api.base_url)


@pytest.fixture(scope="module")
def pet_repo(db_session_factory: sessionmaker[Session]) -> PostgresRepository[Pet]:
    return PostgresRepository(
        session_factory=db_session_factory, orm_class=PetModel, model_class=Pet
    )


@pytest.fixture(scope="function")
def pet_steps(petstore_client: PetstoreClient) -> PetSteps:
    return PetSteps(client=petstore_client)


@pytest.fixture(scope="function")
def infra_steps(
    pet_repo: PostgresRepository[Pet],
    kafka_producer,
) -> InfraSteps:
    return InfraSteps(repo=pet_repo, producer=kafka_producer)
