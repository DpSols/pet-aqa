import warnings

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from config.settings import Settings
from infrastructure.kafka.consumer import KafkaConsumer
from infrastructure.kafka.producer import KafkaProducer
from infrastructure.postgresql.connection_pool import create_sa_engine, create_session_factory
from infrastructure.postgresql.models import Base


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
def db_engine(settings: Settings) -> Engine:
    """Create SQLAlchemy engine for the test session."""
    engine = create_sa_engine(settings.postgres.dsn)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine: Engine) -> sessionmaker[Session]:
    """Create session factory for the test session."""
    return create_session_factory(db_engine)


@pytest.fixture(scope="session")
def apply_migrations(db_engine: Engine) -> None:
    """Apply database migrations using SQLAlchemy metadata."""
    try:
        Base.metadata.create_all(db_engine)
    except Exception as e:
        warnings.warn(f"Database migrations failed (will skip DB-dependent tests): {e}")


@pytest.fixture(scope="session")
def kafka_producer(settings: Settings) -> KafkaProducer:
    producer = KafkaProducer(settings.kafka)
    yield producer
    producer.flush()


@pytest.fixture(scope="session")
def kafka_consumer(settings: Settings) -> KafkaConsumer:
    consumer = KafkaConsumer(settings.kafka)
    yield consumer
    consumer.close()
