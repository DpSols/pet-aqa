from typing import Any, Generic, Type, TypeVar

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import inspect, select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.api.models.pet import Category

T = TypeVar("T", bound=BaseModel)


class PostgresRepository(Generic[T]):
    """Generic PostgreSQL repository using SQLAlchemy 2.0 ORM."""

    def __init__(
        self,
        session_factory: sessionmaker[Session],
        orm_class: Type[DeclarativeBase],
        model_class: Type[T],
    ) -> None:
        """Initialize the repository.

        Args:
            session_factory: SQLAlchemy sessionmaker for creating sessions
            orm_class: SQLAlchemy ORM model class (DeclarativeBase subclass)
            model_class: Pydantic model class for data validation
        """
        self._session_factory = session_factory
        self._orm_class = orm_class
        self._model_class = model_class
        self._log = logger.bind(
            layer="db", table=orm_class.__tablename__, model=model_class.__name__
        )

    def _to_orm(self, entity: T) -> DeclarativeBase:
        """Convert Pydantic model to ORM model.

        Filters data to only include columns that exist in the ORM class,
        and handles special field mappings.

        Args:
            entity: Pydantic model instance

        Returns:
            ORM model instance
        """
        data = entity.model_dump(exclude_none=False)

        # Get valid column names from ORM class
        orm_mapper = inspect(self._orm_class)
        valid_cols = {c.key for c in orm_mapper.column_attrs}

        # Filter to only valid columns
        filtered = {k: v for k, v in data.items() if k in valid_cols}

        # Special handling for category: if it's a dict (Pydantic nested model), extract the name
        if "category" in filtered:
            category_val = filtered["category"]
            if isinstance(category_val, dict):
                filtered["category"] = category_val.get("name")
            elif hasattr(category_val, "name"):
                # Handle Category object (has 'name' attribute)
                filtered["category"] = category_val.name
            # else keep as-is (could be string or None)

        return self._orm_class(**filtered)

    def _from_orm(self, orm_obj: DeclarativeBase) -> T:
        """Convert ORM model to Pydantic model.

        Args:
            orm_obj: ORM model instance

        Returns:
            Pydantic model instance
        """
        # Get ORM object as dict
        orm_data = {}
        orm_mapper = inspect(self._orm_class)

        for column in orm_mapper.column_attrs:
            orm_data[column.key] = getattr(orm_obj, column.key)

        # Map ORM data to Pydantic model, handling field mismatches
        pydantic_data = {}

        for field_name, field_info in self._model_class.model_fields.items():
            if field_name in orm_data:
                value = orm_data[field_name]

                # Special handling for category: convert string back to Category model
                if field_name == "category" and value is not None:
                    # Category is stored as string in DB, reconstruct as Category object
                    pydantic_data[field_name] = Category(id=0, name=value)
                elif field_name == "category" and value is None:
                    pydantic_data[field_name] = None
                else:
                    pydantic_data[field_name] = value

        return self._model_class.model_validate(pydantic_data)

    def save(self, entity: T) -> T:
        """Save (upsert) an entity to the database.

        Args:
            entity: Pydantic model instance to save

        Returns:
            Persisted Pydantic model instance

        Raises:
            RuntimeError: If the upsert operation fails
        """
        orm_obj = self._to_orm(entity)

        with self._session_factory() as session:
            try:
                # merge handles upsert semantics (insert or update)
                merged_obj = session.merge(orm_obj)
                session.flush()
                session.refresh(merged_obj)
                result = self._from_orm(merged_obj)
                session.commit()
                self._log.debug(f"Saved entity with id={getattr(entity, 'id', None)}")
                return result
            except Exception as e:
                session.rollback()
                raise RuntimeError(f"Upsert failed for {self._model_class.__name__}: {e}") from e

    def find_by_id(self, id: str | int) -> T | None:
        """Find an entity by ID.

        Args:
            id: Primary key value

        Returns:
            Pydantic model instance if found, None otherwise
        """
        with self._session_factory() as session:
            orm_obj = session.get(self._orm_class, id)

            if orm_obj is None:
                return None

            result = self._from_orm(orm_obj)
            self._log.debug(f"Found entity with id={id}")
            return result

    def find_all(self, filters: dict[str, Any] | None = None) -> list[T]:
        """Find all entities, optionally filtered.

        Args:
            filters: Dictionary of {column_name: value} for filtering

        Returns:
            List of Pydantic model instances
        """
        with self._session_factory() as session:
            stmt = select(self._orm_class)

            if filters:
                orm_mapper = inspect(self._orm_class)
                valid_cols = {c.key for c in orm_mapper.column_attrs}

                for col_name, value in filters.items():
                    if col_name in valid_cols:
                        stmt = stmt.where(getattr(self._orm_class, col_name) == value)

            orm_objs = session.scalars(stmt).all()
            result = [self._from_orm(obj) for obj in orm_objs]
            self._log.debug(f"Found {len(result)} entities with filters={filters}")
            return result

    def delete(self, id: str | int) -> bool:
        """Delete an entity by ID.

        Args:
            id: Primary key value

        Returns:
            True if entity was found and deleted, False otherwise
        """
        with self._session_factory() as session:
            orm_obj = session.get(self._orm_class, id)

            if orm_obj is None:
                return False

            session.delete(orm_obj)
            session.commit()
            self._log.debug(f"Deleted entity with id={id}")
            return True
