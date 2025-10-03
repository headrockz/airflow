{{
    config(
        materialized='table',
        enabled=true,
        tags=['pokemons'],
    )
}}

with cte as (
    SELECT
        id
        ,name
        ,type
        ,power
        ,accuracy
    FROM {{ ref('moves') }}

)

{{ dbt_utils.deduplicate(
    relation='cte',
    partition_by='id',
    order_by='id, name'
   )
}}
