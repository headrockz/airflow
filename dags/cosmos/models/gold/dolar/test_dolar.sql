{{
    config(
        materialized='table',
        enabled=true,
        tags=['dolar'],
    )
}}

SELECT
    *
FROM {{ ref("obt_monthly_avg")}} p
