{{
    config(
        materialized='table',
        enabled=true,
        tags=['dolar'],
    )
}}

SELECT
    {{ extract_date_parts('date_day') }},
    AVG(close_ibov) AS avg_ibov,
    AVG(close_dolar) AS avg_dolar
FROM {{ ref('tb_dolar_ibov') }}
GROUP BY 1, 2, 3
