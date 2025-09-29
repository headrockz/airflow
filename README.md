# Começando com o DBT (Data Build Tool)

O [DBT](https://www.getdbt.com/) é uma ferramenta de transformação de dados open-source. Ele fornece uma abordagem baseada em código para transformações de dados, facilitando a colaboração, o controle de versão e a manutenção de seus fluxos de trabalho de dados. É uma das ferramentas mais poderosas para Modern Data Stacks.

## Projeto

Esse projeto é um pipeline end-to-end utilizando Airflow, DBT e PostgreSQL. Fazendo a ingestão de uma base em csv de pokemons e movimentos e criando visões para postgres utilizando o DBT e orquestrando pelo Airflow.

### Estrutura do projeto

```bash
├── cosmos # executando o dbt junto com o airflow
│   ├── macros
│   │     └── my macros
│   ├── models
│   │     └── my models
│   ├── seeds
│   │     └── moves.csv
│   │     └── moves_pokemons.csv
│   │     └── pokemons.csv
│   ├── tests
│   │     └── my tests
│   ├──
│   ├── dbt_project.yaml
│   └── profiles.yml
├── dags
│   └── my dags
├── images
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Executando o Projeto

Para executar o DBT no mesmo ambiente que o Airflow, estou utilizando o provider da Astronomer chamado [Cosmos](https://docs.astronomer.io/learn/airflow-dbt). Para executar esse projeto, entre na pasta ***dbt_airflow***, digite `docker-compose up -d`, depois entre na interface web do Airflow [http://localhost:8080](http://localhost:8080), o usuário e senha são **airflowdbt**

É necessário configurar a connection do Postgres dentro do Airflow

![image](/images/connection_postgres.png)
