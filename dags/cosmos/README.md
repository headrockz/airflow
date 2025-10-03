# dbt Project - Cosmos

dbt project for data transformation with pokedex models and financial data (dollar).

## Structure

```text
cosmos/
├── models/
│   ├── sources/          # Data source definitions
│   ├── trusted/          # Clean and standardized data layer
│   │   ├── dolar/        # Financial data (dollar/ibov)
│   │   └── pokedex/      # Pokemon/moves/types data
│   └── gold/             # Aggregation and analysis layer
│       ├── dolar/        # Financial metrics (correlation, volatility)
│       └── pokedex/      # Pokemon/moves/types analysis
├── seeds/                # Static data (CSV)
│   ├── pokemons/         # Base pokemon data (moves, pokemons, moves_pokemons)
│   └── stocks/           # Financial data (dolar_ibov, usd_brl)
├── macros/               # Reusable functions
└── tests/                # Data quality tests
```

## Commands

```bash
dbt run          # Run all models
dbt test         # Run data quality tests
dbt seed         # Load seeds (CSV)
dbt deps         # Install dependencies

# Selective execution
dbt run --select tb_dolar_ibov           # Specific model
dbt run --select tag:finance             # By tag
dbt run --select models/trusted/dolar/   # By folder
dbt test --select tb_pokemon_types       # Specific test
```

## Models

- **Trusted**: Clean data from sources (pokemon, moves, dollar/ibov)
- **Gold**: Analysis and metrics (correlations, volatility, aggregations)
