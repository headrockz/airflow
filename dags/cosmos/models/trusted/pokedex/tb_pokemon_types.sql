{{config(
    materialized='table',
    enabled=true,
    tags=['pokemons'],
    )
}}

with cte as (
    SELECT
        id
        ,type_1
        ,type_2
        ,name
        ,description
        ,weight
        ,height
        ,mega_evolves
        ,evolves
    FROM {{ ref('pokemons') }}

)

{{ dbt_utils.deduplicate(
    relation='cte',
    partition_by='id',
    order_by='id, name'
   )
}}
