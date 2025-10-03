{% macro extract_date_parts(date_column) %}
    EXTRACT(YEAR FROM {{ date_column }}) AS year,
    TO_CHAR({{ date_column }}, 'Month') AS month_name,
    EXTRACT(MONTH FROM {{ date_column }}) AS month
{% endmacro %}
