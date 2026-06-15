{{ config(materialized='table') }}

SELECT
    id,
    name,
    is_superhost,
    created_at,
    updated_at
FROM read_csv_auto('{{ env_var("DBT_DATA_PATH", "../data") }}/hosts.csv',
    header=True,
    quote='"'
)