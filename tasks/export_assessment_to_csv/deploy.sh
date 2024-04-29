functions-framework --debug `
  --target export_assessment_data_csv

gcloud functions deploy export_assessment_data_csv `
--gen2 `
--region=us-central1 `
--runtime=python312 `
--project=musa509s24-team2 `
--source=. `
--entry-point=export_assessment_data_csv `
--service-account=data-pipeline-robot-2024@musa509s24-team2.iam.gserviceaccount.com	 `
--memory=4Gi `
--timeout=480s `
--set-env-vars='PUBLIC_BUCKET=musa5090s24_team02_public,DERIVED_DATASET=derived' `
--trigger-http `
--no-allow-unauthenticated

gcloud functions call export_assessment_data_csv --project=musa509s24-team2 --region=us-central1