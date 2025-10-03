{{
    config(
        post_hook="select count(*) from {{ this }}",
        materialized='table',
        enabled=true,
        tags=['dolar'],
    )
}}

SELECT 
  dim_time.date_day
  ,dim_time."year"
  ,dim_time.month_name
  ,dim_time.weekday_name
  ,dim_time.year_start_date
  ,dim_time.year_end_date
  ,dolar.fechamento_ibov as close_ibov
  ,dolar.fechamento_dolar as close_dolar
FROM {{ ref('dolar_ibov') }} as dolar 
LEFT JOIN {{ ref('time') }} as dim_time ON dolar.data = dim_time.date_day
