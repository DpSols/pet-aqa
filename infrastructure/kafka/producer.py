from typing import Any

from confluent_kafka import Producer
from loguru import logger

from config.settings import KafkaSettings
from infrastructure.kafka import KafkaDeliveryError
from infrastructure.kafka.serializers import serialize_json


class KafkaProducer:
    def __init__(self, settings: KafkaSettings) -> None:
        self._settings = settings
        self._logger = logger.bind(layer="kafka", component="producer")
        self._producer = Producer({"bootstrap.servers": settings.bootstrap_servers})
        self._logger.info(f"KafkaProducer initialized with {settings.bootstrap_servers}")

    def produce(self, topic: str, key: str | bytes, value: str | bytes | dict[str, Any]) -> None:
        if isinstance(value, dict):
            value = serialize_json(value)
        elif isinstance(value, str):
            value = value.encode("utf-8")

        if isinstance(key, str):
            key = key.encode("utf-8")

        self._logger.debug(f"Producing to {topic} with key={key}")
        self._producer.produce(topic, key=key, value=value, on_delivery=self._on_delivery)

    def flush(self, timeout: float = 10.0) -> None:
        self._logger.debug(f"Flushing Kafka producer (timeout={timeout}s)")
        remaining = self._producer.flush(timeout)
        if remaining > 0:
            self._logger.warning(f"{remaining} messages were not delivered within {timeout}s")

    @staticmethod
    def _on_delivery(err: Any, msg: Any) -> None:
        if err:
            raise KafkaDeliveryError(f"Message delivery failed: {err}")
