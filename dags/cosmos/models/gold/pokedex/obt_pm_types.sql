{{
    config(
        materialized='table',
        enabled=true,
        tags=['pokemons'],
    )
}}

SELECT
    p.id as pokemon_id
    ,p.name as pokemon_name
    ,p.type_1 as pokemon_type
    ,m.type as move_type
    ,m.name as move_name
FROM {{ ref("tb_pokemon_types")}} p
JOIN {{ref("tb_moves_types")}} m on m.type = p.type_1

