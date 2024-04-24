CREATE OR REPLACE EXTERNAL TABLE `source.pwd_parcels` (
  `objectid` STRING,
  `parcelid` STRING,
  `tencode` STRING,
  `address` STRING,
  `owner1` STRING,
  `owner2` STRING,
  `bldg_code` STRING,
  `bldg_desc` STRING,
  `brt_id` STRING,
  `num_brt` STRING,
  `num_accounts` STRING,
  `gross_area` STRING,
  `pin` STRING,
  `shape__area` STRING,
  `shape__length` STRING,
  `geog` STRING,
)
OPTIONS (
  description = 'Philadelphia Water Department (PWD) Parcels - Source',
  format = 'JSON',
  uris = ['gs://musa509s24_team02_prepared_data/pwd_parcels/data.jsonl']
);

CREATE OR REPLACE TABLE core.pwd_parcels
CLUSTER BY (geog)
AS (
  SELECT *
  FROM source.pwd_parcels
);

ALTER TABLE core.pwd_parcels
ADD COLUMN property_id STRING;

UPDATE core.pwd_parcels
SET `property_id` = `brt_id`
WHERE TRUE;