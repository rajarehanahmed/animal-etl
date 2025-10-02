from datetime import datetime, timezone
from logging import getLogger
from typing import Any

logger = getLogger(__name__)


def transform_animal(animal: dict[str, Any]) -> dict[str, Any]:
    born_at = transform_timestamp(animal["born_at"]) if animal.get("born_at") else None
    friends = transform_friends(animal["friends"])

    return {
        "id": animal["id"],
        "name": animal["name"],
        "friends": friends,
        **({"born_at": born_at} if born_at else {}),
    }


def transform_friends(friends_str: str) -> list[str]:
    if not friends_str or friends_str.strip() == "":
        return []
    return [friend.strip() for friend in friends_str.split(",") if friend.strip()]


def transform_timestamp(timestamp: int) -> str | None:
    try:
        # timestamp is in milliseconds, so convert to seconds before processing
        time_stamp = timestamp / 1000.0

        dt = datetime.fromtimestamp(time_stamp, tz=timezone.utc)
        return dt.isoformat()
    except Exception as e:
        logger.error(f"Error transforming timestamp {timestamp}: {e}")
        return None


def batch_animals(animals: list[dict[str, Any]], batch_size: int = 100) -> list[list[dict[str, Any]]]:
    return [animals[i : i + batch_size] for i in range(0, len(animals), batch_size)]  # noqa
