#!/usr/bin/env python3

import yaml
import os

from jinja2 import Template, Environment, FileSystemLoader
from pathlib import Path
from datetime import datetime

file_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(file_dir))
template = env.get_template("process_file.jinja2")

file_dir = os.path.join(file_dir, "configs")
for filename in os.listdir(file_dir):
    if filename.endswith(".yaml") or filename.endswith(".yml"):
        print(f"Processando arquivo de configuração: {filename}")
        with open(os.path.join(file_dir, filename), 'r', encoding='utf-8') as f:
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                config = yaml.safe_load(f)
        
            python_functions = []
            for task in config['tasks']:
                if task.get('type') == 'python' and 'python_function' in task:
                    python_functions.append(task['python_function'])
            
            dag_code = template.render(
                dag_id=config['dag_id'],
                description=config.get('description'),
                schedule_interval=config.get('schedule_interval', None),
                tags=config.get('tags', ['dynamic']),
                imports=config.get('imports', ''),
                tasks=config['tasks'],
                dependencies=config.get('dependencies', []),
                python_functions=python_functions,
            )
        
        
        dag_filename = f"{config['dag_id']}.py"
        dags_dir = Path(file_dir).parent.parent.parent / "dags"
        dag_filepath = dags_dir / dag_filename
        
        with open(dag_filepath, 'w', encoding='utf-8') as f:
            f.write(dag_code)
        
        print(f"DAG gerado com sucesso: {dag_filepath}")

    print(f"📁 Localização: {dag_filepath}")
