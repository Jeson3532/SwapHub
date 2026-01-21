import yaml
import os
from pathlib import Path
import pyprojroot as ppr

current_dir = Path(__file__)
prompts_path = ppr.here() / 'config' / 'prompts'


def get_prompt(prompt_name: str, section_name: str = 'system_prompt', encoding='utf-8'):
    with open(os.path.join(prompts_path, prompt_name), "r", encoding=encoding) as f:
        data = yaml.safe_load(f)
    return data[section_name]


