{{
    config(
        materialized='table',
        enabled=true,
        tags=['dolar'],
    )
}}

SELECT
    {{ extract_date_parts('date_day') }},
    STDDEV(close_ibov) AS volatility_ibov,
    STDDEV(close_dolar) AS volatility_dolar
FROM {{ ref('tb_dolar_ibov') }}
GROUP BY 1, 2, 3
