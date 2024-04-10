import os
import pathlib
import requests
import time # for timeout testing
import functions_framework
from google.cloud import storage
from dotenv import load_dotenv
# from google.oauth2 import service_account
# import googleapiclient.discovery  # type: ignore
# from google.cloud import api_keys_v2
# from google.cloud.api_keys_v2 import Key


load_dotenv(".env")
DATA_DIR = pathlib.Path(__file__).parent  


def download_phl_opa_properties(url: str, fname: str):
    response = requests.get(url)
    response.raise_for_status()

    with open(fname, 'wb') as f:
        f.write(response.content)

    print(f'Downloaded {fname}')


def extract_phl_opa_properties(download=False):

    print("Extracting PHL OPA Properties data...")

    # Download the OPA Properties data as a CSV
    url = 'https://opendata-downloads.s3.amazonaws.com/' + \
        'opa_properties_public.csv'
    filename = DATA_DIR / 'phl_opa_properties.csv'

    if download:
        start = time.time()
        download_phl_opa_properties(url, filename)
        end = time.time()
        print(f"Time taken for download:\n\t{end-start} seconds.")  
        # took 514 seconds in last trial
        
    # Upload the downloaded file to cloud storage
    BUCKET_NAME = os.getenv('RAW_DATA_LAKE_BUCKET')
    blobname = 'opa_properties/phl_opa_properties.csv'

    storage_client = storage.Client(project=os.getenv("PROJECT_ID"))
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blobname)
    print("Starting file upload.")
    start = time.time()
    blob.upload_from_filename(filename, timeout=(60*3))
    end = time.time()
    print(f"Time taken for upload:\n\t{end-start} seconds.")  
    # took 47 minutes to successfully upload

    print(f'Uploaded {blobname} to {BUCKET_NAME}')

    return f"Uploaded to gs://{BUCKET_NAME}/{blobname} successfully"


@functions_framework.http
def extract_phl_opa_prop_main(request):
    # check if file exists before downloading        
    return extract_phl_opa_properties(
        True if not (os.path.exists(
            DATA_DIR / 'phl_opa_properties.csv'
            )
            ) else False)


if __name__ == "__main__":
    print(extract_phl_opa_prop_main("google.com"))
