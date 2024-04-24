CREATE OR REPLACE TABLE `core.phl_opa_properties`
CLUSTER BY (geog)
AS (
    SELECT *
        REPLACE
        (
            CAST(LEFT(assessment_date, 10) AS DATE) AS assessment_date,
            CAST(category_code AS NUMERIC) AS category_code,
            CASE WHEN census_tract = '' THEN NULL ELSE CAST(census_tract AS INT64) END AS census_tract,
            CASE WHEN exempt_building = '' THEN NULL ELSE CAST(exempt_building AS NUMERIC) END AS exempt_building,
            CASE WHEN depth = '' THEN NULL ELSE CAST(depth AS NUMERIC) END AS depth,
            CASE WHEN fireplaces = '' THEN NULL ELSE CAST(fireplaces AS INT64) END AS fireplaces,
            CASE WHEN frontage = '' THEN NULL ELSE CAST(frontage AS NUMERIC) END AS frontage,
            CASE WHEN garage_spaces = '' THEN NULL ELSE CAST(garage_spaces AS INT64) END AS garage_spaces,
            CASE WHEN geographic_ward = '' THEN NULL ELSE CAST(geographic_ward AS NUMERIC) END AS geographic_ward,
            CASE WHEN homestead_exemption = '' THEN NULL ELSE CAST(homestead_exemption AS INT64) END AS homestead_exemption,
            CASE WHEN house_extension = '' THEN NULL ELSE CAST(house_extension AS INT64) END AS house_extension,
            CASE WHEN house_number = '' THEN NULL ELSE CAST(house_number AS INT64) END AS house_number,
            CASE WHEN interior_condition = '' THEN NULL ELSE CAST(interior_condition AS INT64) END AS interior_condition,
            CASE WHEN market_value = '' THEN NULL ELSE CAST(market_value AS NUMERIC) END AS market_value,
            CASE WHEN number_of_bathrooms = '' THEN NULL ELSE CAST(number_of_bathrooms AS INT64) END AS number_of_bathrooms,
            CASE WHEN number_of_bedrooms = '' THEN NULL ELSE CAST(number_of_bedrooms AS INT64) END AS number_of_bedrooms,
            CASE WHEN number_of_rooms = '' THEN NULL ELSE CAST(number_of_rooms AS INT64) END AS number_of_rooms,
            CASE WHEN number_stories = '' THEN NULL ELSE CAST(number_stories AS INT64) END AS number_stories,
            CASE WHEN off_street_open = '' THEN NULL ELSE CAST(off_street_open AS INT64) END AS off_street_open,
            CASE WHEN parcel_number = '' THEN NULL ELSE CAST(parcel_number AS INT64) END AS parcel_number,
            CAST(LEFT(sale_date, 10) AS DATE) AS sale_date,
            CAST(LEFT(recording_date, 10) AS DATE) AS recording_date,
            CASE WHEN sale_price = '' THEN NULL ELSE CAST(sale_price AS NUMERIC) END AS sale_price,
            CASE WHEN taxable_building = '' THEN NULL ELSE CAST(taxable_building AS NUMERIC) END AS taxable_building,
            CASE WHEN taxable_land = '' THEN NULL ELSE CAST(taxable_land AS NUMERIC) END AS taxable_land,
            CASE WHEN total_area = '' THEN NULL ELSE CAST(total_area AS NUMERIC) END AS total_area,
            CASE WHEN total_livable_area = '' THEN NULL ELSE CAST(total_livable_area AS NUMERIC) END AS total_livable_area,
            CASE WHEN year_built = '' THEN NULL ELSE CAST(year_built AS INT64) END AS year_built,
            CASE WHEN zip_code = '' THEN NULL ELSE CAST(zip_code AS INT64) END AS zip_code,
            CASE WHEN pin = '' THEN NULL ELSE CAST(pin AS NUMERIC) END AS pin
        )
    FROM `source.phl_opa_properties`
);

ALTER TABLE `core.phl_opa_properties`
ADD COLUMN property_id NUMERIC;

UPDATE `core.phl_opa_properties`
SET `property_id` = `parcel_number`
WHERE TRUE
