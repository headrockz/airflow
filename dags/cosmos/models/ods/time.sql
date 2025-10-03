{{
    config(
        materialized = "table"
    )
}}

WITH cte AS ( {{ dbt_date.get_date_dimension('2002-01-01', '2022-12-31') }} )
SELECT
    date_day as date_day
    ,prior_date_day as prior_date_day
    ,next_date_day as next_date_day
    ,prior_year_date_day as prior_year
    ,day_of_week as weekday
    ,day_of_week_name as weekday_name
    ,day_of_week_name_short as weekday_short_name
    ,day_of_month as month_day
    ,day_of_year as year_day
    ,week_start_date as week_start_date
    ,week_end_date as week_end_date
    ,week_of_year as year_week
    ,month_of_year as year_month
    ,month_name as month_name
    ,month_name_short as month_short_name
    ,month_start_date as month_start_date
    ,month_end_date as month_end_date
    ,year_number as year
    ,year_start_date as year_start_date
    ,year_end_date as year_end_date
FROM cte
