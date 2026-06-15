{{ config(materialized='table') }}

SELECT
    fr.listing_id,
    fr.review_date,
    fr.reviewer_name,
    fr.review_text,
    fr.sentiment,
    CASE
        WHEN fm.date_day IS NULL THEN 'not full moon'
        ELSE 'full moon'
    END AS is_full_moon
FROM {{ ref('fact_reviews') }} fr
LEFT JOIN {{ ref('silver_full_moon_dates') }} fm
    ON fr.review_date = fm.date_day + INTERVAL '1 day'