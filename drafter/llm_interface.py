
import os
import openai
import dotenv
import datetime
from colorama import Fore, Style

import drafter.prompts as prompts
import drafter.file_system as fs

dotenv.load_dotenv('.env')

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
model = 'gpt-4o'

logs_dir = 'logs'

def ensure_dirs(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def log_file(content, key):
    date_string = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'{date_string}-{key}.txt'
    file_path = os.path.join(logs_dir, file_name)
    ensure_dirs(file_path)
    with open(file_path, 'w') as f:
        f.write(content)

def log_prompt(prompt):
    log_file(prompt, 'prompt')

def log_response(response):
    log_file(response, 'response')

def get_iteration(command):
    path = '.'
    file_structure = fs.generate_file_structure(path)
    file_content = fs.generate_file_contents(path)
    user_prompt = prompts.USER_PROMPT.format(
        file_structure=file_structure,
        file_content=file_content,
        command=command
    )
    system_prompt = prompts.SYSTEM
    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
    )
    log_prompt(user_prompt)
    return response.choices[0].message.content

PROPOSAL = '[PROPOSAL]'

def format_output(message, style=Style.RESET_ALL, color=Fore.RESET):
    print(f"{style}{color}{message}{Style.RESET_ALL}{Fore.RESET}")

def write_file(path, content):
    ensure_dirs(path)
    with open(path, 'w') as f:
        f.write(content)

def create_file(path, content):
    format_output(f'Creating file: {path}', style=Style.BRIGHT, color=Fore.GREEN)
    return write_file(path, content)

def edit_file(path, content):
    format_output(f'Editing file: {path}', style=Style.BRIGHT, color=Fore.YELLOW)
    return write_file(path, content)

def delete_file(path, content=''):
    format_output(f'Deleting file: {path}', style=Style.BRIGHT, color=Fore.RED)
    os.remove(path)

ACTIONS = {
    '[ADD]': create_file,
    '[EDIT]': edit_file,
    '[DELETE]': delete_file
}
CODEBLOCK = '```'

def parse_action(line):
    for name, method in ACTIONS.items():
        if name in line:
            path = line.split(name)[-1].strip()
            return method, path
    return None, None

def run_operation(method, path, codeblock_lines=None):
    if method and path:
        content = '\n'.join(codeblock_lines) if type(codeblock_lines) is list else ''
        method(path, content)

def execute_response(response):
    log_response(response)
    method = path = None
    is_codeblock = False
    codeblock_lines = []
    for line in response.split('\n'):
        if line.startswith(PROPOSAL):
            run_operation(method, path, codeblock_lines)
            codeblock_lines = []
            method, path = parse_action(line)
        elif not is_codeblock and line.startswith(CODEBLOCK):
            is_codeblock = True
            codeblock_lines.append(line.replace(CODEBLOCK, ''))
        elif is_codeblock:
            if line.startswith(CODEBLOCK):
                is_codeblock = False
                line = line.replace(CODEBLOCK, '')
            codeblock_lines.append(line)
    run_operation(method, path, codeblock_lines)
    format_output("Operation completed successfully.", style=Style.BRIGHT, color=Fore.CYAN)
