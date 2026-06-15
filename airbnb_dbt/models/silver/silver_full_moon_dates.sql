{{ config(materialized='table') }}

SELECT
    CAST(full_moon_date AS DATE) AS date_day
FROM {{ ref('seed_full_moon_dates') }}