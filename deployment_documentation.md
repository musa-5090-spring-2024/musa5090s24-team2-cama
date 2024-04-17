# Things to Remember

* create/update `.gcloudignore` file
	- ensure generated files (env/, pycache, .csv|.jsonl|... data, etc.) are included
	- including .gcloudignore itself
* Note the options in `gcloud functions deploy`
	- **The ones used normally are in the example below**
	- things like *timeout* or *entry_point* change for each function as necessary
* remember `\` in CLI on Linux/Mac is ``` (or backtick) on Windows

# gcloud CLI commands

### **Deploy**

#### *extract_phl_opa_properties*:
- Linux/Mac
```shell
gcloud functions deploy extract_phl_opa_properties \
--gen2 \
--region=us-central1 \
--runtime=python312 \
--source=. \
--entry-point=extract_phl_opa_prop_main \
--service-account='data-pipeline-robot-2024@musa509s24-team2.iam.gserviceaccount.com' \
--timeout=60s \
--memory=1024Mi \
--no-allow-unauthenticated \
--trigger-http
```

- Windows
```shell
gcloud functions deploy extract_phl_opa_properties 
--gen2 `
--region=us-central1 `
--runtime=python312 `
--source=. `
--entry-point=extract_phl_opa_prop_main `
--service-account="data-pipeline-robot-2024@musa509s24-team2.iam.gserviceaccount.com" `
--timeout=60s `
--memory=1024Mi `
--no-allow-unauthenticated `
--trigger-http
```

	- one-line version
```shell
gcloud functions deploy extract_phl_opa_properties --gen2 --region=us-central1 --runtime=python312 --source=.  --entry-point=extract_phl_opa_prop_main  --service-account="data-pipeline-robot-2024@musa509s24-team2.iam.gserviceaccount.com"  --timeout=60s  --memory=1024Mi  --no-allow-unauthenticated --trigger-http
```

#### *prepare_phl_opa_properties*:

#### *load_phl_opa_properties*:

#### *run_sql*:

## CORS configuration

`gcloud storage buckets update gs://musa5090s24_team02_public/ --cors-file=public_cors_config.json`

<ins>**Ensure the path to public_cors_config.json is correct.**
* it is currently located at the root folder of the repository*</ins>

### View current configuration

run `gcloud storage buckets describe gs://<bucket_name>` in any gcloud accessible CLI

for example, use the following for the public bucket...

`gcloud storage buckets describe gs://musa5090s24_team02_public`


### JSON File contents

`
[
    {
      "origin": ["*"],
      "method": ["GET","POST","PUT","OPTIONS","HEAD","DELETE"],
      "responseHeader": ["*"],
      "maxAgeSeconds": 3600
    }
]

`

## Workflow Details

#### <ins>YAML</ins>
`
#
# This workflow passes the region where the workflow is deployed
# to the Wikipedia API and returns a list of related Wikipedia articles.
# A region is retrieved from the GOOGLE_CLOUD_LOCATION system variable
# unless you input your own search term; for example, {"searchTerm": "asia"}.
main:
    params: [input]
    steps:
    - extractPHLPropertyData:
        call: http.post
        args:
            url: https://us-central1-musa509s24-team2.cloudfunctions.net/extract_phl_opa_properties
            auth:
                type: OIDC
    - preparePHLPropertyData:
        call: http.post
        args:
            url: https://prepare-phl-opa-properties-u7ppop2rpa-uc.a.run.app # https://us-central1-musa509s24-team2.cloudfunctions.net/_phl_opa_properties
            auth:
                type: OIDC
    - loadPHLPropertyData:
        call: http.post
        args:
            url: https://us-central1-musa509s24-team2.cloudfunctions.net/load_phl_opa_properties
            auth:
                type: OIDC
`