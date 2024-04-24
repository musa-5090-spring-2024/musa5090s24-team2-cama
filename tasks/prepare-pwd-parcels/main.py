import os
import pathlib
import time  # for timeout testing
import csv
import pyproj
import json
import functions_framework
from shapely import wkt
from google.cloud import storage
from dotenv import load_dotenv
# from google.oauth2 import service_account
# import googleapiclient.discovery  # type: ignore
# from google.cloud import api_keys_v2
# from google.cloud.api_keys_v2 import Key
# from google.cloud import bigquery


load_dotenv(".env")
OVERWRITE_DOWNLOAD = True
OVERWRITE_PROCESSED = True
DATA_DIR = pathlib.Path(__file__).parent 
RAW_DATA_DIR = DATA_DIR / 'raw_data'
PREPARED_DATA_DIR = DATA_DIR / 'prepared_data'

raw_filename = RAW_DATA_DIR / 'phl_pwd_parcels.geojson'
prepared_filename = PREPARED_DATA_DIR / 'phl_pwd_parcels.jsonl'

BUCKET_NAME = os.getenv('PREP_DATA_LAKE_BUCKET')
storage_client = storage.Client(project=os.getenv("PROJECT_ID"))
bucket = storage_client.bucket(BUCKET_NAME)


def check_dirs(dirs):
    for dir in dirs:
        if not (os.path.isdir(dir)):
            os.makedirs(dir, mode=0o777)


def enforce_download():
    if OVERWRITE_DOWNLOAD:
        return True
    else:
        return True if not (os.path.exists(
            raw_filename
            )
            ) else False
    

def enforce_processing():
    if OVERWRITE_PROCESSED:
        return True
    else:
        return True if not (os.path.exists(
            prepared_filename
            )
            ) else False


def download_raw_data():
    # Download the data from the bucket
    raw_blobname = "pwd_parcels/phl_pwd_parcels.geojson"
    blob = storage_client.bucket(
        os.getenv('RAW_DATA_LAKE_BUCKET')).blob(raw_blobname)
    start = time.time()
    blob.download_to_filename(raw_filename)
    end = time.time()
    print(f"Time taken for download:\n\t{end-start} seconds.")
    # took 987 seconds in last trial
    print(f'Downloaded to {raw_filename}')


def process_raw_data(fname=prepared_filename):
    print("Beginning projection processing of data...")
    # Load the data from the GEOJSON file
    with open(raw_filename, 'r', encoding="utf8") as f:
        with open(raw_filename, 'r') as f:
            data = json.load(f)

    # Write the data to a JSONL file
    with open(prepared_filename, 'w') as f:
        for feature in data['features']:
            row = feature['properties']
            row['geog'] = (
                json.dumps(feature['geometry'])
                if feature['geometry'] and feature['geometry']['coordinates']
                else None
            )
            f.write(json.dumps(row) + '\n')

    print(f'Processed data into {prepared_filename}')


def prepare_phl_pwd_parcel(download=False, process=False):

    # Download the OPA Properties data from bucket (if necessary)
    if download:
        print("Downloading raw PWD Parcels data...")
        download_raw_data()
    
    if process:
        start = time.time()
        process_raw_data()
        end = time.time()
        print(f"Time taken for processing:\n\t{end-start} seconds.")
        
    print("Uploading processed PWD Parcels data...")    
    # Upload the prepared data to the bucket
    prepared_blobname = "pwd_parcels/data.jsonl"
    blob = bucket.blob(prepared_blobname)
    
    start = time.time()
    blob.upload_from_filename(prepared_filename, timeout=60*3)
    end = time.time()
    print(f"Time taken for upload:\n\t{end-start} seconds.")
    # took 764 seconds to successfully upload

    return f"Uploaded to gs://{BUCKET_NAME}/{prepared_blobname} successfully"


@functions_framework.http
def prepare_phl_pwd_parcel_main(request):
    '''
    makes directories on local machines if necessary,
    downloads, processes, and uploads processed data to prepared data bucket
    Estimate Runtime (ERt): ~30 minutes for everything 
    (though it currently checks if files exist 
    before downloading or processing);
    ERt with files: ~ 10 minutes
    '''
    # check if directories exists before referencing paths
    check_dirs([RAW_DATA_DIR, PREPARED_DATA_DIR]) 

    # check if file exists before downloading        
    return prepare_phl_pwd_parcel(
        enforce_download(), enforce_processing())
    

if __name__ == "__main__":
    print(prepare_phl_pwd_parcel_main("request"))