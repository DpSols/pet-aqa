from loguru import logger
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def create_sa_engine(dsn: str, pool_size: int = 2, max_overflow: int = 8) -> Engine:
    """Create a SQLAlchemy engine with psycopg3 driver.

    Args:
        dsn: PostgreSQL connection string (postgresql://user:pass@host:port/db)
        pool_size: Minimum number of connections to keep in the pool
        max_overflow: Maximum overflow connections beyond pool_size

    Returns:
        SQLAlchemy Engine instance
    """
    # Convert postgresql:// to postgresql+psycopg:// for psycopg3 driver
    sa_url = dsn.replace("postgresql://", "postgresql+psycopg://", 1)

    _logger = logger.bind(layer="postgresql", component="engine")
    _logger.info(f"Creating SQLAlchemy engine: pool_size={pool_size}, max_overflow={max_overflow}")

    return create_engine(
        sa_url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        echo=False,
        pool_pre_ping=True,  # Test connections before using them
    )


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create a SQLAlchemy session factory.

    Args:
        engine: SQLAlchemy Engine instance

    Returns:
        Session factory (sessionmaker)
    """
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)
