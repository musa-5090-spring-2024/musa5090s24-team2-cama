import os
import pathlib
import requests
import time # for timeout testing
from google.cloud import storage
from dotenv import load_dotenv
from google.oauth2 import service_account
import googleapiclient.discovery  # type: ignore
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


load_dotenv()
DATA_DIR = pathlib.Path(__file__).parent  # / 'raw_data'

'''
def create_key(email: str) -> None:
    """Creates a key for a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    service = googleapiclient.discovery.build(
        "iam", "v1", credentials=credentials
                                              )

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
'''
'''
def create_api_key(project_id: str, suffix: str) -> Key:
    """
    Creates and restrict an API key. Add the suffix for uniqueness.

    TODO(Developer):
    1. Before running this sample,
      set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    2. Make sure you have the necessary permission to create API keys.

    Args:
        project_id: Google Cloud project id.

    Returns:
        response: Returns the created API Key.
    """
    # Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f"My first API key - {suffix}"

    # Initialize request and set arguments.
    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    # Make the request and wait for the operation to complete.
    response = client.create_key(request=request).result()

    print(f"Successfully created an API key: {response.name}")
    # For authenticating with the API key, use the value in "response.key_string".
    # To restrict the usage of this API key, use the value in "response.name".
    return response
'''


def check_google_auth():
    if not (os.path.exists(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))):
        path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        built_path = ""
        for level in path.rsplit("/", 1)[0].split("/"):
            if not os.path.exists(os.path.join(built_path, level)):
                built_path = os.path.join(built_path, level)
                os.makedirs(built_path)
        open(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), "w", encoding='utf-8'
            ).close()
        # create_key(os.getenv('AUTH_EMAIL'))


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
        print(f"Time taken for download:\n\t{end-start} seconds.") # took 514 seconds in last trial
        
    # Upload the downloaded file to cloud storage
    BUCKET_NAME = os.getenv('RAW_DATA_LAKE_BUCKET')
    blobname = 'phl_opa_properties/phl_opa_properties.csv'

    storage_client = storage.Client(project=os.getenv("PROJECT_ID"))
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blobname)
    start = time.time()
    blob.upload_from_filename(filename, timeout=(60*60))
    end = time.time()
    print(f"Time taken for upload:\n\t{end-start} seconds.") # took 47 minutes to successfully upload

    print(f'Uploaded {blobname} to {BUCKET_NAME}')

    return "Uploaded to gs://{BUCKET_NAME}/{blobname} successfully"


if __name__ == "__main__":
    # check_google_auth()

    # check if file exists before downloading        
    extract_phl_opa_properties(
        True if not (os.path.exists(
            DATA_DIR / 'phl_opa_properties.csv'
            )
            ) else False)

    # create_api_key("musa509s24-team2","")
