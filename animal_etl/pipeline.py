import logging
import sys
from typing import Any

from animal_etl.api_client import APIClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("animal_etl.log")],
)

logger = logging.getLogger(__name__)


class AnimalETLPipeline:
    def __init__(self, base_url: str = "http://localhost:3123"):
        self.api_client = APIClient(base_url)

    def fetch_animals(self) -> list[dict[str, Any]]:
        endpoint = "/animals/v1/animals"
        all_animals = []
        page = 1

        while True:
            response = self.api_client.get(endpoint=endpoint, params={"page": page})
            animals_on_page = response["items"]
            total_pages = response["total_pages"]
            logger.info(f"Page {page}/{total_pages}, Page Size: {len(animals_on_page)}")

            # Get detailed info for each animal
            for animal_summary in animals_on_page:
                animal_detail = self.api_client.get(endpoint=f"{endpoint}/{animal_summary['id']}")
                logger.info(f"Animal ID {animal_detail['id']}: {animal_detail['name']}")
                all_animals.append(animal_detail)

            if page >= total_pages:
                break
            page += 1

        logger.info(f"Fetched {len(all_animals)} animals from {page} pages")
        return all_animals

    def run(self) -> None:
        logger.info("Starting ETL pipeline")

        animals = self.fetch_animals()


if __name__ == "__main__":
    pipeline = AnimalETLPipeline()
    pipeline.run()
