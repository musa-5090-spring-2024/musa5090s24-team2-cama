import os
import pathlib
import requests
from google.cloud import storage
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
import googleapiclient.discovery  # type: ignore


load_dotenv()
DATA_DIR = pathlib.Path(__file__).parent  # / 'raw_data'


def create_key(email: str) -> None:
    """Creates a key for a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    service = googleapiclient.discovery.build("iam", "v1", credentials=credentials)

    key = (
        service.projects()
        .serviceAccounts()
        .keys()
        .create(name="projects/-/serviceAccounts/" + email, body={})
        .execute()
    )

    # The privateKeyData field contains the base64-encoded service account key
    # in JSON format.
    # TODO(Developer): Save the below key {json_key_file} to a secure location.
    #  You cannot download it again later.
    # import base64
    # json_key_file = base64.b64decode(key['privateKeyData']).decode('utf-8')

    if not key["disabled"]:
        print("Created json key")


if not(os.path.exists("keys/service-account-key.json")):
    create_key(os.getenv('AUTH_EMAIL'))


def extract_phl_opa_properties():

    print("Extracting PHL OPA Properties data...")

    # Download the OPA Properties data as a CSV
    url = 'https://opendata-downloads.s3.amazonaws.com/opa_properties_public.csv'
    filename = DATA_DIR / 'phl_opa_properties.csv'

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f'Downloaded {filename}')

    # Upload the downloaded file to cloud storage
    BUCKET_NAME = os.getenv('DATA_LAKE_BUCKET')
    blobname = 'raw/phl_opa_properties/phl_opa_properties.csv'

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)

    print(f'Uploaded {blobname} to {BUCKET_NAME}')

    return "Downloaded and uploaded gs://{BUCKET_NAME}/{blobname} successfully"


if __name__ == "__main__":
    extract_phl_opa_properties()