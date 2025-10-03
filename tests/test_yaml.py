import os
import pytest
import yaml
from pathlib import Path


def test_yaml_files():
    """Test if YAML files are valid."""
    file_dir = os.path.dirname(os.path.abspath(__file__))
    configs_dir = Path(file_dir).parent

    # Coletando todos os arquivos YAML, excluindo pasta target
    yaml_files = []
    for path in configs_dir.rglob("*.[y][am]*l"):
        # Ignora arquivos na pasta target
        if not any(ignore in path.parts for ignore in {'target', '.venv', 'dbt_packages'}):
            yaml_files.append(path)
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"Invalid YAML File {yaml_file}: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
