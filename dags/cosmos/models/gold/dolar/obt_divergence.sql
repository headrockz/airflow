{{
    config(
        materialized='table',
        enabled=true,
        tags=['dolar'],
    )
}}

SELECT 
  date_day
  ,oscillation_ibov
  ,oscillation_dolar
  ,CASE 
    WHEN oscillation_ibov * oscillation_dolar < 0 THEN TRUE
    WHEN oscillation_ibov * oscillation_dolar > 0 THEN FALSE
    ELSE NULL
  END AS has_divergence
FROM {{ ref('obt_oscillations') }}
