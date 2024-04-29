import os
import csv
import pathlib
import functions_framework
from dotenv import load_dotenv
from google.cloud import bigquery
from google.cloud import storage


load_dotenv(".env")
DATA_DIR = pathlib.Path(__file__).parent


public_bucket_name = os.getenv('PUBLIC_BUCKET')

derived_dataset_name = os.getenv('DERIVED_DATASET')
table_name = 'tax_year_assessment_bins'

query = f'''
SELECT * FROM {derived_dataset_name}.{table_name}
'''


@functions_framework.http
def export_assessment_data_csv(request):
    print("Loading assessment data...")

    prepared_filename = DATA_DIR / 'tax_year_assessment_bins.csv'
    prepared_location = 'tax_year_assessment_bins/tax_year_assessment_bins.csv'

    bigquery_client = bigquery.Client()
    result = bigquery_client.query_and_wait(query)
      
    with open(prepared_filename, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[field.name for field in result.schema])
        writer.writeheader()
        for row in result:
            writer.writerow(row)
      
    print(f'Processed data into {prepared_filename}')

    # Upload the prepared data to cloud storage
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(public_bucket_name)

    prepared_blobname = (prepared_location)
    blob = bucket.blob(prepared_blobname)
    blob.upload_from_filename(prepared_filename)
    print(f'Uploaded {prepared_filename} to {public_bucket_name}')

    return 'Success'
