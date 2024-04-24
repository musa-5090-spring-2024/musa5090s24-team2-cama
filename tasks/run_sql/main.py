
import os
import pathlib
import functions_framework
from dotenv import load_dotenv
from google.cloud import bigquery
from check_bq import check_datasets

from dotenv import load_dotenv
load_dotenv()

import os
import pathlib
import functions_framework
from google.cloud import bigquery

DIR_NAME = pathlib.Path(__file__).parent
SQL_DIR_NAME = DIR_NAME / 'sql'


@functions_framework.http
def run_sql(request):
    
    # Check the dataset(s) specified in the request
    #  or core and source if not specified
    try:
        datasets = request.args.get("dataset")
        print(datasets)
        check_datasets(request.args.get("dataset"))
    except Exception:
        check_datasets(["core", "source"])

    # Read the SQL file specified in the request
    sql_path = SQL_DIR_NAME / str(request.args.get('sql'))
    print(sql_path)
    # Read the SQL file specified in the request
    sql_path = SQL_DIR_NAME / request.args.get('sql')


    # Check that the file exists
    if (not sql_path.exists()) or (not sql_path.is_file()):
        # Return a 404 (not found) response if not
        return f'File {sql_path} not found', 404

    # Read the SQL file
    with open(sql_path, 'r', encoding='utf-8') as sql_file:
        sql_query = sql_file.read()
        
    # Run the SQL query
    bigquery_client = bigquery.Client(project=os.getenv("PROJECT_ID"))
    bigquery_client.query_and_wait(sql_query)

    print(f'Ran the SQL file {sql_path}')
    return f'Ran the SQL file {sql_path}'

