# 🚀 Dynamic DAG Generator

Sistema simples e eficiente para gerar DAGs do Airflow dinamicamente usando arquivos de configuração YAML.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Uso Básico](#uso-básico)
- [Configuração de DAGs](#configuração-de-dags)
- [Tipos de Tarefas](#tipos-de-tarefas)
- [Schedule Intervals](#schedule-intervals)
- [Dependências](#dependências)
- [Exemplos](#exemplos)
- [Troubleshooting](#troubleshooting)

## 🎯 Visão Geral

O **Dynamic DAG Generator** permite criar DAGs do Airflow através de arquivos de configuração YAML simples, eliminando a necessidade de escrever código Python repetitivo para cada DAG.

## 📁 Estrutura do Projeto

```bash
includes/dynamic_generator/
├── README.md
├── generate_dag.py          # Script principal de geração
├── process_file.jinja2      # Template Jinja2 para DAGs
└── configs/                 # Diretório de configurações
    ├── multi_task.yaml      # Exemplo com múltiplas tarefas
    └── simple_task.yaml     # Exemplo simples
```

## 🛠 Instalação

### Pré-requisitos

- Python 3.7+
- Apache Airflow 2.0+
- PyYAML
- Jinja2

### Dependências

```bash
pip install pyyaml jinja2
```

## 🚀 Uso Básico

### 1. Criar Configuração YAML

Crie um arquivo na pasta `configs/`:

```yaml
# configs/meu_pipeline.yaml
dag_id: "meu_pipeline_etl"
description: "Pipeline de ETL de dados"
schedule_interval: "@daily"
tags:
  - "etl"
  - "dados"

tasks:
  - task_id: "extrair_dados"
    type: "bash"
    bash_command: "echo 'Extraindo dados...'"

  - task_id: "processar_dados"
    type: "python"
    python_callable: "print_message"
    python_imports: |
      from modules.utils import print_message
    op_kwargs:
      msg: "Processando dados"

dependencies:
  - upstream: "extrair_dados"
    downstream: "processar_dados"
```

### 2. Gerar DAG

```bash
python includes/dynamic_generator/generate_dag.py
```

### 3. Resultado

Um arquivo `meu_pipeline_etl.py` será criado na pasta `dags/` com todas as configurações do Airflow.

## 📝 Configuração de DAGs

### Estrutura Básica

```yaml
dag_id: "nome_unico_da_dag"           # Obrigatório
description: "Descrição da DAG"       # Opcional
schedule_interval: "@daily"           # Opcional (padrão: None)
tags:                                 # Opcional
  - "tag1"
  - "tag2"

tasks:                                # Obrigatório
  - task_id: "tarefa1"
    type: "bash"
    bash_command: "echo 'Hello'"

dependencies:                         # Opcional
  - upstream: "tarefa1"
    downstream: "tarefa2"
```

### Parâmetros Principais

| Parâmetro | Tipo | Descrição | Obrigatório |
|-----------|------|-----------|-------------|
| `dag_id` | string | Identificador único da DAG | ✅ |
| `description` | string | Descrição da DAG | ❌ |
| `schedule_interval` | string/null | Agendamento da DAG | ❌ |
| `tags` | list | Tags para categorização | ❌ |
| `tasks` | list | Lista de tarefas | ✅ |
| `dependencies` | list | Dependências entre tarefas | ❌ |

## 🔧 Tipos de Tarefas

### BashOperator

Execute comandos shell/bash:

```yaml
tasks:
  - task_id: "backup_database"
    type: "bash"
    bash_command: "pg_dump mydb > backup.sql"
```

### PythonOperator

Execute funções Python:

```yaml
tasks:
  - task_id: "process_data"
    type: "python"
    python_callable: "my_function"
    python_imports: |
      from modules.processing import my_function
    op_kwargs:
      param1: "value1"
      param2: 123
```

#### Parâmetros do PythonOperator

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `python_callable` | Nome da função a executar | `"process_data"` |
| `python_imports` | Imports necessários | `"from modules import func"` |
| `op_kwargs` | Parâmetros para a função | `{"msg": "hello"}` |

## 🔗 Dependências

### Sintaxe Simples

```yaml
dependencies:
  - upstream: "tarefa_anterior"
    downstream: "proxima_tarefa"
  - upstream: "tarefa_a"
    downstream: "tarefa_b"
```

### Exemplo com Múltiplas Dependências

```yaml
tasks:
  - task_id: "extract"
    type: "bash"
    bash_command: "echo 'Extracting'"

  - task_id: "transform"
    type: "bash" 
    bash_command: "echo 'Transforming'"

  - task_id: "load"
    type: "bash"
    bash_command: "echo 'Loading'"

  - task_id: "validate"
    type: "python"
    python_callable: "validate_data"

dependencies:
  - upstream: "extract"
    downstream: "transform"
  - upstream: "transform" 
    downstream: "load"
  - upstream: "load"
    downstream: "validate"
```

Resulta em: `extract → transform → load → validate`

## 📚 Exemplos

### Exemplo 1: Pipeline ETL Simples

```yaml
dag_id: "etl_vendas_diario"
description: "ETL diário de dados de vendas"
schedule_interval: "@daily"
tags: ["etl", "vendas", "daily"]

tasks:
  - task_id: "extract_sales"
    type: "bash"
    bash_command: "python scripts/extract_sales.py"

  - task_id: "transform_data"
    type: "python"
    python_callable: "transform_sales"
    python_imports: |
      from modules.transformers import transform_sales
    op_kwargs:
      source_table: "raw_sales"
      target_table: "clean_sales"

  - task_id: "load_warehouse"
    type: "bash"
    bash_command: "python scripts/load_to_warehouse.py"

dependencies:
  - upstream: "extract_sales"
    downstream: "transform_data"
  - upstream: "transform_data"
    downstream: "load_warehouse"
```

### Exemplo 2: Pipeline de Monitoramento

```yaml
dag_id: "monitoring_health_check"
description: "Verificação de saúde do sistema"
schedule_interval: "*/15 * * * *"  # A cada 15 minutos
tags: ["monitoring", "health"]

tasks:
  - task_id: "check_database"
    type: "python"
    python_callable: "check_db_connection"
    python_imports: |
      from modules.health import check_db_connection

  - task_id: "check_apis"
    type: "bash"
    bash_command: "curl -f http://api.example.com/health"

  - task_id: "send_alerts"
    type: "python"
    python_callable: "send_notification"
    python_imports: |
      from modules.alerts import send_notification
    op_kwargs:
      channel: "slack"
      message: "Sistema saudável"

# Sem dependências - tarefas executam em paralelo
```

### Exemplo 3: Pipeline Complexo

```yaml
dag_id: "complex_data_pipeline"
description: "Pipeline complexo de processamento"
schedule_interval: "0 3 * * *"  # Todo dia às 3:00 AM
tags: ["complex", "data", "ml"]

tasks:
  - task_id: "validate_input"
    type: "python"
    python_callable: "validate_source"
    python_imports: |
      from modules.validators import validate_source

  - task_id: "extract_customers"
    type: "bash"
    bash_command: "python etl/extract_customers.py"

  - task_id: "extract_orders"
    type: "bash" 
    bash_command: "python etl/extract_orders.py"

  - task_id: "join_data"
    type: "python"
    python_callable: "join_customer_orders"
    python_imports: |
      from modules.processors import join_customer_orders

  - task_id: "ml_predictions"
    type: "bash"
    bash_command: "python ml/predict_churn.py"

  - task_id: "generate_report"
    type: "python"
    python_callable: "create_report"
    python_imports: |
      from modules.reports import create_report
    op_kwargs:
      report_type: "daily_summary"

dependencies:
  - upstream: "validate_input"
    downstream: "extract_customers"
  - upstream: "validate_input"
    downstream: "extract_orders"
  - upstream: "extract_customers"
    downstream: "join_data"
  - upstream: "extract_orders"
    downstream: "join_data"
  - upstream: "join_data"
    downstream: "ml_predictions"
  - upstream: "ml_predictions"
    downstream: "generate_report"
```

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. DAG não aparece no Airflow
**Possíveis causas:**
- Erro de sintaxe no YAML
- `dag_id` duplicado
- Erro no template Python gerado

**Solução:**
```bash
# Verificar logs do Airflow
airflow dags list-import-errors

# Validar YAML
python -c "import yaml; yaml.safe_load(open('configs/seu_arquivo.yaml'))"
```

#### 2. Import Error em funções Python
**Problema:**
```
ImportError: cannot import name 'my_function' from 'modules.utils'
```

**Solução:**
- Verificar se o módulo está no PYTHONPATH
- Confirmar que a função existe
- Verificar a sintaxe do `python_imports`

#### 3. Dependências não funcionam
**Problema:** Tarefas executam fora de ordem

**Verificar:**
- Nomes das tarefas em `dependencies` conferem com `task_id`
- Não há dependências circulares
- Sintaxe YAML está correta

### Debug Mode

Para debugar a geração:

```python
# Adicionar prints no generate_dag.py
print(f"Processando: {config}")
print(f"DAG ID: {config['dag_id']}")
print(f"Tasks: {config['tasks']}")
```

### Validação de Configuração

```python
# Script para validar YAML antes da geração
import yaml

def validate_config(config_file):
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    # Verificações obrigatórias
    assert 'dag_id' in config, "dag_id é obrigatório"
    assert 'tasks' in config, "tasks é obrigatório"
    assert len(config['tasks']) > 0, "Deve ter pelo menos uma task"
    
    # Verificar task_ids únicos
    task_ids = [task['task_id'] for task in config['tasks']]
    assert len(task_ids) == len(set(task_ids)), "task_ids devem ser únicos"
    
    print("✅ Configuração válida!")

validate_config('configs/meu_arquivo.yaml')
```

## 🤝 Contribuição

### Adicionando Novos Tipos de Operadores

1. **Atualizar o template** (`process_file.jinja2`):
```jinja2
{% elif task.type == 'email' %}
{{task.task_id}} = EmailOperator(
    task_id='{{task.task_id}}',
    to='{{task.to}}',
    subject='{{task.subject}}',
    html_content='{{task.body}}',
    dag=dag
)
{% endif %}
```

2. **Documentar o novo tipo** neste README

3. **Criar exemplo** na pasta `configs/`

### Melhorias Sugeridas

- [ ] Validação automática de YAML
- [ ] Suporte a mais operadores (EmailOperator, S3Operator, etc.)
- [ ] Templates de configuração pré-definidos
- [ ] Interface web para criar configurações
- [ ] Testes automatizados

## 📄 Licença

Este projeto segue a mesma licença do projeto Airflow principal.

---

**Desenvolvido com ❤️ para simplificar a criação de DAGs no Airflow**
