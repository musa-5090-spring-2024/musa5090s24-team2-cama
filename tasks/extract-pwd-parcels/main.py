import os
import pathlib
import requests
import time  # for timeout testing
import functions_framework
from google.cloud import storage
from dotenv import load_dotenv
# from google.oauth2 import service_account
# import googleapiclient.discovery  # type: ignore
# from google.cloud import api_keys_v2
# from google.cloud.api_keys_v2 import Key


load_dotenv(".env")
DATA_DIR = pathlib.Path(__file__).parent  


def download_phl_pwd_parcels(url: str, fname: str):
    response = requests.get(url)
    response.raise_for_status()

    with open(fname, 'wb') as f:
        f.write(response.content)

    print(f'Downloaded {fname}')


def extract_phl_pwd_parcels(download=False):

    print("Extracting PWD Parcel data...")

    # Download the OPA Properties data as a CSV
    url = 'https://opendata.arcgis.com/datasets/' + \
        '84baed491de44f539889f2af178ad85c_0.geojson'
    filename = DATA_DIR / 'phl_pwd_parcels.geojson'

    if download:
        start = time.time()
        download_phl_pwd_parcels(url, filename)
        end = time.time()
        print(f"Time taken for download:\n\t{end-start} seconds.")  
        # took 514 seconds in last trial
        
    # Upload the downloaded file to cloud storage
    BUCKET_NAME = os.getenv('RAW_DATA_LAKE_BUCKET')
    blobname = 'pwd_parcels/phl_pwd_parcels.geojson'

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
def extract_pwd_parcel_main(request):
    # check if file exists before downloading        
    return extract_phl_pwd_parcels(
        True if not (os.path.exists(
            DATA_DIR / 'phl_pwd_parcels.geojson'
            )
            ) else False)


if __name__ == "__main__":
    print(extract_pwd_parcel_main("google.com"))
