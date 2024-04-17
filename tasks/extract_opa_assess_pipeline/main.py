import requests
import pathlib
from google.cloud import storage
from dotenv import load_dotenv
import os

load_dotenv(".env")
DATA_DIR = pathlib.Path(__file__).parent

def extract_opa_assess_pipeline():
    url = 'https://opendata-downloads.s3.amazonaws.com/assessments.csv'
    r = requests.get(url)
    raw_data_folder = DATA_DIR / 'raw_data'
    if not os.path.exists(raw_data_folder):
        os.mkdir(raw_data_folder)
    filename = DATA_DIR / 'raw_data/opa_assessments.csv'
    with open(filename, "wb") as f:
        for line in r.iter_lines():
            f.write(line+'\n'.encode())
    print('Writing File Complete')
    # Upload the downloaded file to cloud storage
    BUCKET_NAME = os.getenv('PREP_DATA_LAKE_BUCKET')
    blobname = 'opa_assessments/assessments.csv'
    print(os.getcwd())
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blobname)
    print("Starting file upload.")
    blob.upload_from_filename(filename, timeout=(60*3)) 
    print(f'Uploaded {blobname} to {BUCKET_NAME}')
    return f"Uploaded to gs://{BUCKET_NAME}/{blobname} successfully"

extract_opa_assess_pipeline()
