import logging
import sys

from .api_client import APIClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("animal_etl.log")],
)

logger = logging.getLogger(__name__)


class AnimalETLPipeline:
    def __init__(self, base_url: str = "http://localhost:3123"):
        self.api_client = APIClient(base_url)

    def run(self) -> None:
        logger.info("Starting ETL pipeline")


if __name__ == "__main__":
    pipeline = AnimalETLPipeline()
    pipeline.run()
