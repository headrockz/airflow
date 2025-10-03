# Dynamic DAG Generator

Simple and efficient system to generate Airflow DAGs dynamically using YAML configuration files.

## Project Structure

```bash
includes/dynamic_generator/
├── README.md
├── generate_dag.py          # Main generation script
├── process_file.jinja2      # Jinja2 template for DAGs
└── configs/                 # Configuration directory
    ├── multi_task.yaml      # Multi-task example
    └── simple_task.yaml     # Simple example
```

## Installation

- Python 3.7+
- Apache Airflow 2.0+
- PyYAML
- Jinja2

### Dependencies

```bash
pip install pyyaml jinja2
```

## Basic Usage

### 1. Create YAML Configuration

Create a file in the `configs/` folder:

```yaml
# configs/my_pipeline.yaml
dag_id: "my_etl_pipeline"
description: "Data ETL pipeline"
schedule_interval: "@daily"
imports: |
  from modules.utils import print_message
tags:
  - "etl"
  - "data"

tasks:
  - task_id: "extract_data"
    type: "bash"
    bash_command: "echo 'Extracting data...'"

  - task_id: "process_data"
    type: "python"
    python_callable: "print_message"
    op_kwargs:
      msg: "Processing data"

dependencies:
  - upstream: "extract_data"
    downstream: "process_data"
```

### 2. Generate DAG

```bash
python includes/dynamic_generator/generate_dag.py
```

### 3. Result

A `my_etl_pipeline.py` file will be created in the `dags/` folder with all Airflow configurations.

## 📝 DAG Configuration

### Basic Structure

```yaml
dag_id: "unique_dag_name"             # Required
description: "DAG description"        # Optional
imports: |
  from airflow.operators.bash import BashOperator
schedule_interval: "@daily"           # Optional
tags:                                 # Optional
  - "tag1"
  - "tag2"

tasks:                                # Required
  - task_id: "task1"
    type: "bash"
    bash_command: "echo 'Hello'"

dependencies:                         # Optional
  - upstream: "task1"
    downstream: "task2"
```

### Main Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `dag_id` | string | Unique DAG identifier | ✅ |
| `description` | string | DAG description | ❌ |
| `schedule_interval` | string/null | DAG scheduling | ❌ |
| `tags` | list | Tags for categorization | ❌ |
| `tasks` | list | Task list | ✅ |
| `dependencies` | list | Task dependencies | ❌ |

## Dependencies

```yaml
dependencies:
  - upstream: "previous_task"
    downstream: "next_task"
  - upstream: "task_a"
    downstream: "task_b"
```

### Example with Multiple Dependencies

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

Results in: `extract → transform → load → validate`

## Adding New Operator Types

**Update template** (`process_file.jinja2`):

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
