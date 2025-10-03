{{
    config(
        materialized='table',
        enabled=true,
        tags=['dolar'],
    )
}}

SELECT 
       date_day, 
       close_ibov,
       LAG(close_ibov) OVER (ORDER BY date_day) AS prev_close_ibov,
       close_ibov - LAG(close_ibov) OVER (ORDER BY date_day) AS oscillation_ibov,
       close_dolar,
       LAG(close_dolar) OVER (ORDER BY date_day) AS prev_close_dolar,
       close_dolar - LAG(close_dolar) OVER (ORDER BY date_day) AS oscillation_dolar
FROM {{ ref('tb_dolar_ibov') }}
