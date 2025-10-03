# Airflow + dbt Project

End-to-end data pipeline using Apache Airflow, dbt, and PostgreSQL for data transformation and orchestration.

## Tech Stack

- **[Apache Airflow](https://airflow.apache.org/)** - Workflow orchestration
- **[dbt](https://www.getdbt.com/)** - Data transformation  
- **[Astronomer Cosmos](https://docs.astronomer.io/learn/airflow-dbt)** - dbt integration for Airflow
- **[PostgreSQL](https://www.postgresql.org/)** - Database

## Project Structure

```text
airflow/
├── dags/                   # Airflow DAGs
│   ├── cosmos/             # dbt project
│   │   ├── models/         # dbt models (trusted/gold layers)
│   │   ├── seeds/          # Static CSV data
│   │   ├── macros/         # Reusable dbt functions
│   │   └── tests/          # Data quality tests
│   └── *.py                # DAG files
├── includes/               # Additional modules
├── plugins/                # Airflow plugins
├── tests/                  # Project tests
├── docker-compose.yaml     # Docker services
├── Dockerfile              # Custom Airflow image
└── pyproject.toml          # Python dependencies
```

## Quick Start

1. **Clone and start services:**

```bash
docker-compose up -d
```

2. **Access Airflow UI:**

- URL: <http://localhost:8080>
- User: `airflow`
- Password: `airflow`

3. **Configure PostgreSQL connection in Airflow:**

- Connection ID: `postgres`
- Host: `postgres`
- Database: `airflow`
- User: `airflow`
- Password: `airflow`

## Data Pipeline

The project processes Pokemon and financial data through dbt layers:

- **Seeds**: Raw CSV data (pokemon, moves, dollar/ibov)
- **Trusted**: Clean and standardized data
- **Gold**: Aggregated metrics and analysis

## Testing

The project includes automated tests for data quality and YAML validation:

```bash
# Run all tests
pytest
# Run with coverage
pytest --cov=tests --cov-report=html
# Run specific test
pytest tests/test_yaml.py -v
```

## Dynamic DAG Generation

The project includes a dynamic DAG generator that creates Airflow DAGs from YAML configuration files, eliminating repetitive Python code.

See detailed documentation: [Dynamic Generator README](includes/dynamic_generator/README.md)


