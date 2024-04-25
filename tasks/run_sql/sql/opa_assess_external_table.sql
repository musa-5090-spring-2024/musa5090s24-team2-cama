CREATE OR REPLACE EXTERNAL TABLE `source.opa_assessments` (
    `parcel_number` STRING,
    `year` INT64,
    `market_value` FLOAT64,
    `taxable_land` FLOAT64,
    `taxable_building` FLOAT64,
    `exempt_land` FLOAT64,
    `exempt_building` FLOAT64,
    `objectid` INT64
)
OPTIONS (
    description = 'Philadelphia OPA Assessments - Source',
    format = 'CSV',
    uris = ['gs://musa509s24_team02_prepared_data/opa_assessments/assessments.csv'],
    skip_leading_rows = 1
);
