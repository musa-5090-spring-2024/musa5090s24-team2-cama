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
prepared_blobname = 'opa_properties/data.jsonl'
table_name = 'phl_opa_properties'
table_uri = f'gs://{BUCKET_NAME}/{prepared_blobname}'

create_table_query = f'''
CREATE OR REPLACE EXTERNAL TABLE `{dataset_name}.{table_name}` (
  `objectid` STRING,
  `assessment_date` STRING,
  `basements` STRING,
  `beginning_point` STRING,
  `book_and_page` STRING,
  `building_code` STRING,
  `building_code_description` STRING,
  `category_code` STRING,
  `category_code_description` STRING,
  `census_tract` STRING,
  `central_air` STRING,
  `cross_reference` STRING,
  `date_exterior_condition` STRING,
  `depth` STRING,
  `exempt_building` STRING,
  `exempt_land` STRING,
  `exterior_condition` STRING,
  `fireplaces` STRING,
  `frontage` STRING,
  `fuel` STRING,
  `garage_spaces` STRING,
  `garage_type` STRING,
  `general_construction` STRING,
  `geographic_ward` STRING,
  `homestead_exemption` STRING,
  `house_extension` STRING,
  `house_number` STRING,
  `interior_condition` STRING,
  `location` STRING,
  `mailing_address_1` STRING,
  `mailing_address_2` STRING,
  `mailing_care_of` STRING,
  `mailing_city_state` STRING,
  `mailing_street` STRING,
  `mailing_zip` STRING,
  `market_value` STRING,
  `market_value_date` STRING,
  `number_of_bathrooms` STRING,
  `number_of_bedrooms` STRING,
  `number_of_rooms` STRING,
  `number_stories` STRING,
  `off_street_open` STRING,
  `other_building` STRING,
  `owner_1` STRING,
  `owner_2` STRING,
  `parcel_number` STRING,
  `parcel_shape` STRING,
  `quality_grade` STRING,
  `recording_date` STRING,
  `registry_number` STRING,
  `sale_date` STRING,
  `sale_price` STRING,
  `separate_utilities` STRING,
  `sewer` STRING,
  `site_type` STRING,
  `state_code` STRING,
  `street_code` STRING,
  `street_designation` STRING,
  `street_direction` STRING,
  `street_name` STRING,
  `suffix` STRING,
  `taxable_building` STRING,
  `taxable_land` STRING,
  `topography` STRING,
  `total_area` STRING,
  `total_livable_area` STRING,
  `type_heater` STRING,
  `unfinished` STRING,
  `unit` STRING,
  `utility` STRING,
  `view_type` STRING,
  `year_built` STRING,
  `year_built_estimate` STRING,
  `zip_code` STRING,
  `zoning` STRING,
  `pin` STRING,
  `building_code_new` STRING,
  `building_code_description_new` STRING,
  `geog` GEOGRAPHY,
)
OPTIONS (
  description = 'Philadelphia OPA Properties - Source',
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
SET `property_id` = `parcel_number`
WHERE TRUE;
'''


def load_phl_opa_properties():

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
def load_phl_opa_prop_main(request):
    # ensure datasets tables are created in exist
    check_datasets([dataset_name, core_dataset_name])

    # check if file exists before downloading        
    return load_phl_opa_properties()


if __name__ == "__main__":
    load_phl_opa_prop_main("Hello World")
    
