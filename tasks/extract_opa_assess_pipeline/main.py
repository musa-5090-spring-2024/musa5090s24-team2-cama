import requests
import pathlib
from google.cloud import storage
from dotenv import load_dotenv
import os
import functions_framework
import pandas as pd

load_dotenv(".env")
DATA_DIR = pathlib.Path(__file__).parent

functions_framework.http
def extract_opa_assess_main(request):
    url = 'https://opendata-downloads.s3.amazonaws.com/assessments.csv'
    df = pd.read_csv(url)
    raw_data_folder = DATA_DIR / 'raw_data'
    if not os.path.exists(raw_data_folder):
        os.mkdir(raw_data_folder)
    filename = DATA_DIR / 'raw_data/opa_assessments.csv'
    df.to_csv(filename,index=False)
    print('Writing File Complete')
    # Upload the downloaded file to cloud storage
    BUCKET_NAME = os.getenv('PREP_DATA_LAKE_BUCKET')
    blobname = 'opa_assessments/assessments.csv'
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blobname)
    print("Starting file upload.")
    blob.upload_from_filename(filename, timeout=(60*3)) 
    print(f'Uploaded {blobname} to {BUCKET_NAME}')
    return f"Uploaded to gs://{BUCKET_NAME}/{blobname} successfully"