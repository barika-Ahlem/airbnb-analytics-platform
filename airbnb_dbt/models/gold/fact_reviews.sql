{{ config(materialized='table') }}

SELECT
    listing_id,
    review_date,
    reviewer_name,
    review_text,
    sentiment
FROM {{ ref('silver_reviews') }}
WHERE review_text IS NOT NULL
ORDER BY review_date DESC