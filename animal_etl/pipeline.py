import logging
import sys
from typing import Any

from animal_etl.api_client import APIClient
from animal_etl.transformers import batch_animals, transform_animal

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
                # it could get slow if there is too much data, we could optimize this by sending multiple api calls
                # asynchronously, but as the data size is not that much and the server
                # is also slow (accordinng to the doc), we can keep it simple for now
                animal_detail = self.api_client.get(endpoint=f"{endpoint}/{animal_summary['id']}")
                logger.info(f"Animal ID {animal_detail['id']}: {animal_detail['name']}")
                all_animals.append(animal_detail)

            if page >= 10:
                break
            page += 1

        logger.info(f"Fetched {len(all_animals)} animals from {page} pages")
        return all_animals

    def transform_animals(self, animals: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [transform_animal(animal) for animal in animals]

    def load_animals(self, animals: list[dict[str, Any]], batch_size: int = 100) -> None:
        endpoint = "/animals/v1/home"
        batches = batch_animals(animals, batch_size)

        for i, batch in enumerate(batches, 1):
            self.api_client.post(endpoint=endpoint, data=batch)
            logger.info(f"Loaded batch {i}/{len(batches)}")

    def run(self) -> None:
        logger.info("Starting ETL pipeline")

        logger.info("Extracting animals from API")
        animals = self.fetch_animals()

        logger.info("Transforming animals")
        transformed_animals = self.transform_animals(animals)
        logger.info(transformed_animals)

        logger.info("Loading animals to API")
        self.load_animals(transformed_animals)


if __name__ == "__main__":
    pipeline = AnimalETLPipeline()
    pipeline.run()
