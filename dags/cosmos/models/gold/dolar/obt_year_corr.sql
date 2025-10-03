{{
    config(
        materialized='table',
        enabled=true,
        tags=['dolar'],
    )
}}

SELECT
    year,
    CORR(close_ibov, close_dolar) AS corr
FROM {{ ref('tb_dolar_ibov') }}
GROUP BY 1

UNION ALL

SELECT
    2999 AS year,
    CORR(close_ibov, close_dolar) AS corr
FROM {{ ref('tb_dolar_ibov') }}
GROUP BY 1
