{{ config(materialized='table') }}

SELECT
    CAST(id AS INTEGER)         AS host_id,
    COALESCE(name, 'Anonymous') AS host_name,
    CAST(is_superhost AS BOOLEAN) AS is_superhost,
    CAST(created_at AS TIMESTAMP) AS created_at,
    CAST(updated_at AS TIMESTAMP) AS updated_at
FROM {{ ref('bronze_hosts') }}