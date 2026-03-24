from confluent_kafka import Consumer, KafkaError
from loguru import logger

from config.settings import KafkaSettings
from core.protocols import ConsumedMessage


class KafkaConsumer:
    def __init__(self, settings: KafkaSettings) -> None:
        self._settings = settings
        self._logger = logger.bind(layer="kafka", component="consumer")

        config = {
            "bootstrap.servers": settings.bootstrap_servers,
            "group.id": settings.consumer_group,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True,
        }
        self._consumer = Consumer(config)
        self._logger.info(f"KafkaConsumer initialized (group={settings.consumer_group})")

    def subscribe(self, topics: list[str]) -> None:
        self._logger.debug(f"Subscribing to topics: {topics}")
        self._consumer.subscribe(topics)

    def consume(
        self,
        timeout: float = 1.0,
        max_records: int = 1,
    ) -> list[ConsumedMessage]:
        messages = self._consumer.consume(num_messages=max_records, timeout=timeout)
        consumed: list[ConsumedMessage] = []

        for msg in messages:
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    self._logger.debug(f"End of partition reached: {msg.topic()}")
                else:
                    self._logger.warning(f"Consumer error: {msg.error()}")
                continue

            consumed.append(
                ConsumedMessage(
                    topic=msg.topic(),
                    partition=msg.partition(),
                    offset=msg.offset(),
                    key=msg.key(),
                    value=msg.value(),
                )
            )

        self._logger.debug(f"Consumed {len(consumed)} messages")
        return consumed

    def close(self) -> None:
        self._logger.debug("Closing Kafka consumer")
        self._consumer.close()
