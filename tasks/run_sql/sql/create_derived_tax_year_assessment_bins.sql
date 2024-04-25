CREATE OR REPLACE TABLE derived.tax_year_assessment_bins AS
SELECT
    year AS tax_year,
    FLOOR(market_value / 10000) * 10000 AS lower_bound,
    FLOOR(market_value / 10000) * 10000 + 10000 AS upper_bound,
    COUNT(*) AS property_count
FROM
    core.opa_assessments
GROUP BY
    year, lower_bound, upper_bound
ORDER BY lower_bound;
