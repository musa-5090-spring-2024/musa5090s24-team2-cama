import pandas as pd
import geopandas as gpd
import functions_framework
import os
import pathlib
import time  # for timeout testing
import csv
import pyproj
import json
from shapely import wkt
from google.cloud import storage, bigquery
from dotenv import load_dotenvls

PROJECT_ID = "musa509s24-team2"
BUCKET_NAME = "musa5090s24_team02_temp_data"
dataset_name = "source"
core_dataset_name = "core"
prepared_blobname = 'property_tile_info.geojson'
table_name = 'pwd_parcels'
table_uri = f'gs://{BUCKET_NAME}/{prepared_blobname}'

client = bigquery.Client(project=PROJECT_ID)