{{ config(materialized='table') }}

SELECT
    listing_id,
    listing_url,
    listing_name,
    room_type,
    minimum_nights,
    host_id,
    price,
    created_at,
    updated_at
FROM {{ ref('silver_listings') }}