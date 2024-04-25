import os
import pathlib
import google
from dotenv import load_dotenv
from google.cloud import bigquery


load_dotenv(".env")
DATA_DIR = pathlib.Path(__file__).parent  

PROJECT_ID = os.getenv("PROJECT_ID")
dataset_name = os.getenv('SOURCE_DATASET')
core_dataset_name = os.getenv('CORE_DATASET')


def check_datasets(sets):
    client = bigquery.Client(PROJECT_ID)

    for set in sets:
        set_id = f"{PROJECT_ID}.{set}"
        dataset = bigquery.Dataset(set_id)
        dataset.location = os.getenv('DATASET_LOCATION')

        try:
            client.create_dataset(dataset, timeout=30)
        except google.api_core.exceptions.Conflict:
            print(f"Dataset {set} already exists.", end='\n\n')


if __name__ == "__main__":
    check_datasets([dataset_name, core_dataset_name])
    
