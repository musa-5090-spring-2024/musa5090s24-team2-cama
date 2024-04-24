import os
import pathlib
import time  # for timeout testing
import google
import functions_framework
from dotenv import load_dotenv
from google.cloud import bigquery


load_dotenv(".env")
DATA_DIR = pathlib.Path(__file__).parent  

PROJECT_ID = os.getenv("PROJECT_ID")
BUCKET_NAME = os.getenv('PREP_DATA_LAKE_BUCKET')
dataset_name = os.getenv('SOURCE_DATASET')
core_dataset_name = os.getenv('CORE_DATASET')
prepared_blobname = 'pwd_parcels/data.jsonl'
table_name = 'pwd_parcels'
table_uri = f'gs://{BUCKET_NAME}/{prepared_blobname}'

## what is the actual field for property_id
### there is no parcel_number
create_table_query = f'''
CREATE OR REPLACE EXTERNAL TABLE `{dataset_name}.{table_name}` (
  `objectid` STRING,
  `parcelid` STRING,
  `tencode` STRING,
  `address` STRING,
  `owner1` STRING,
  `owner2` STRING,
  `bldg_code` STRING,
  `bldg_desc` STRING,
  `brt_id` STRING,
  `num_brt` STRING,
  `num_accounts` STRING,
  `gross_area` STRING,
  `pin` STRING,
  `shape__area` STRING,
  `shape__length` STRING,
  `geog` STRING,
)
OPTIONS (
  description = 'Philadelphia Water Department (PWD) Parcels - Source',
  format = 'JSON',
  uris = ['{table_uri}']
);

'''

create_core_table_query = f'''
CREATE OR REPLACE TABLE {core_dataset_name}.{table_name} 
CLUSTER BY (geog)
AS (
  SELECT *
  FROM {dataset_name}.{table_name}
);

ALTER TABLE {core_dataset_name}.{table_name}
ADD COLUMN property_id STRING;

UPDATE {core_dataset_name}.{table_name}
SET `property_id` = `parcelid`
WHERE TRUE;
'''


def load_phl_pwd_parcels():

    print("Loading PHL OPA Properties data...")

    bigquery_client = bigquery.Client(project=PROJECT_ID)
    start = time.time()
    bigquery_client.query_and_wait(create_table_query)
    end = time.time()
    print(f"Time taken for external table load:\n\t{end-start} seconds.") 

    start = time.time()
    bigquery_client.query_and_wait(create_core_table_query)
    end = time.time()
    print(f"Time taken for internal table load:\n\t{end-start} seconds.")  
    
    return f"Loaded {table_uri} into {dataset_name}.{table_name}\n\tand internal/native table {core_dataset_name}.{table_name}"


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


@functions_framework.http
def load_phl_pwd_parcels_main(request):
    # ensure datasets tables are created in exist
    check_datasets([dataset_name, core_dataset_name])

    # check if file exists before downloading        
    return load_phl_pwd_parcels()


if __name__ == "__main__":
    load_phl_pwd_parcels_main("Hello World")
    
