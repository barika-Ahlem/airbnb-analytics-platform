{{ config(materialized='table') }}

SELECT *
FROM read_csv_auto('{{ env_var("DBT_DATA_PATH", "../data") }}/listings.csv',
    header=True,
    quote='"'
)