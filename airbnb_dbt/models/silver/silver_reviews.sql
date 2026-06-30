{{ config(materialized='table') }}

SELECT
    listing_id,
    CAST(date AS DATE)  AS review_date,
    reviewer_name,
    comments            AS review_text,
    sentiment
FROM {{ ref('bronze_reviews') }}
WHERE comments IS NOT NULL
  AND TRIM(comments) != ''