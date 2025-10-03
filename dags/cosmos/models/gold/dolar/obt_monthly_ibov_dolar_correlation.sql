{{
    config(
        materialized='table',
        enabled=true,
        tags=['dolar'],
    )
}}

WITH daily_variations AS (
  SELECT
    {{ extract_date_parts('date_day') }},
    close_ibov,
    prev_close_ibov,
    oscillation_ibov,
    close_dolar,
    prev_close_dolar,
    oscillation_dolar
  FROM {{ ref('obt_oscillations') }}
),

filter AS (
    SELECT
    year,
    month_name,
    CORR(oscillation_ibov, oscillation_dolar) AS correlation_ibov_dolar
  FROM daily_variations
  WHERE oscillation_ibov IS NOT NULL AND oscillation_dolar IS NOT NULL
  GROUP BY 1, 2
)

SELECT
  *
  ,CASE
    WHEN correlation_ibov_dolar > 0.9 THEN 'very strong (positive)'
    WHEN correlation_ibov_dolar > 0.7 THEN 'strong (positive)'
    WHEN correlation_ibov_dolar > 0.5 THEN 'moderate (positive)'
    WHEN correlation_ibov_dolar > 0.3 THEN 'weak (positive)'
    WHEN correlation_ibov_dolar > 0 THEN 'very weak (positive)'
    WHEN correlation_ibov_dolar < -0.9 THEN 'very strong (negative)'
    WHEN correlation_ibov_dolar < -0.7 THEN 'strong (negative)'
    WHEN correlation_ibov_dolar < -0.5 THEN 'moderate (negative)'
    WHEN correlation_ibov_dolar < -0.3 THEN 'weak (negative)'
    WHEN correlation_ibov_dolar < 0 THEN 'very weak (negative)'
    ELSE NULL
  END AS correlation_type
FROM filter
