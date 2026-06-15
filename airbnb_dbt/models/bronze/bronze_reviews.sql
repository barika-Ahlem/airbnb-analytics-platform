{{ config(materialized='table') }}

SELECT
    listing_id,
    date,
    reviewer_name,
    comments,
    sentiment
FROM read_csv_auto('{{ env_var("DBT_DATA_PATH", "../data") }}/reviews.csv',
    header=True,
    quote='"'
)