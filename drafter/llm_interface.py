
import os
import openai
import dotenv
import datetime
from colorama import Fore, Style
import shutil

import drafter.prompts as prompts
import drafter.file_system as fs

dotenv.load_dotenv('.env')

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
model = 'gpt-4o'

logs_dir = 'logs'
backup_dir = 'backups'
iterations_dir = '.history'
redo_dir = 'redos'
max_iterations = 10


def ensure_dirs(path):
    if path and path != '':
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


def backup_file(path, content, iteration_dir):
    backup_path = os.path.join(iteration_dir, path)
    ensure_dirs(backup_path)
    with open(backup_path, 'w') as f:
        f.write(content)


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

    format_output("(*￣▽￣)b Sending request to OpenAI. This may take a while...", style=Style.BRIGHT, color=Fore.YELLOW)

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
    print(f"{style}{color}⮞ {message}{Style.RESET_ALL}{Fore.RESET}")


def write_file(path, content, iteration_dir):
    if os.path.exists(path):
        with open(path, 'r') as f:
            original_content = f.read()
        backup_file(path, original_content, iteration_dir)
    ensure_dirs(path)
    with open(path, 'w') as f:
        f.write(content)
    return len(content.split('\n'))


def create_file(path, content, iteration_dir):
    format_output(f'🛠️ Creating file: {path}', style=Style.BRIGHT, color=Fore.GREEN)
    num_lines = write_file(path, content, iteration_dir)
    format_output(f'File {path} created with {num_lines} lines. 💾', style=Style.BRIGHT, color=Fore.GREEN)


def edit_file(path, content, iteration_dir):
    format_output(f'🛠️ Editing file: {path}', style=Style.BRIGHT, color=Fore.YELLOW)
    num_lines = write_file(path, content, iteration_dir)
    format_output(f'File {path} edited with {num_lines} lines. 📝', style=Style.BRIGHT, color=Fore.YELLOW)


def delete_file(path, content=None, iteration_dir=iterations_dir):
    if os.path.exists(path):
        with open(path, 'r') as f:
            original_content = f.read()
        backup_file(path, original_content, iteration_dir)
    format_output(f'🛠️ Deleting file: {path}', style=Style.BRIGHT, color=Fore.RED)
    os.remove(path)
    format_output(f'File {path} deleted. 🗑️', style=Style.BRIGHT, color=Fore.RED)


def undo_last_change():
    iteration_folders = sorted([d for d in os.listdir(iterations_dir) if os.path.isdir(os.path.join(iterations_dir, d))], reverse=True)
    if not iteration_folders:
        format_output("No iterations found. Nothing to undo.", style=Style.BRIGHT, color=Fore.YELLOW)
        return
    latest_iteration = iteration_folders[0]
    backed_up_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(os.path.join(iterations_dir, latest_iteration)) for f in filenames]
    
    ensure_dirs(redo_dir)
    redo_backup_path = os.path.join(redo_dir, latest_iteration)
    ensure_dirs(redo_backup_path)
    
    for file_path in backed_up_files:
        original_path = file_path.replace(iterations_dir + os.sep + latest_iteration + os.sep, "")
        if os.path.exists(original_path):
            shutil.copyfile(original_path, os.path.join(redo_backup_path, original_path))
        ensure_dirs(original_path)
        shutil.copyfile(file_path, original_path)
    shutil.rmtree(os.path.join(iterations_dir, latest_iteration))
    format_output(f"Undo last change: restored files from iteration {latest_iteration}.", style=Style.BRIGHT, color=Fore.GREEN)


def redo_last_change():
    redo_folders = sorted([d for d in os.listdir(redo_dir) if os.path.isdir(os.path.join(redo_dir, d))])
    if not redo_folders:
        format_output("No redo operations found.", style=Style.BRIGHT, color=Fore.YELLOW)
        return
    most_recent_redo = redo_folders[-1]
    backed_up_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(os.path.join(redo_dir, most_recent_redo)) for f in filenames]
    for file_path in backed_up_files:
        restored_path = file_path.replace(redo_dir + os.sep + most_recent_redo + os.sep, "")
        ensure_dirs(restored_path)
        shutil.copyfile(file_path, restored_path)
    format_output(f"Redo last change: files restored from iteration {most_recent_redo}.", style=Style.BRIGHT, color=Fore.GREEN)


ACTIONS = {
    '[ADD]': create_file,
    '[EDIT]': edit_file,
    '[DELETE]': delete_file
}
CODEBLOCK = '{codeblock}'


def parse_action(line):
    for name, method in ACTIONS.items():
        if name in line:
            path = line.split(name)[-1].strip()
            if '/' not in path:
                path = os.path.join('.', path)
            return method, path
    return None, None


def run_operation(method, path, codeblock_lines=None, iteration_dir=''):
    if method and path:
        content = '\n'.join(codeblock_lines) if type(codeblock_lines) is list else ''
        method(path, content, iteration_dir)


def cleanup_old_iterations():
    iteration_folders = sorted([d for d in os.listdir(iterations_dir) if os.path.isdir(os.path.join(iterations_dir, d))])
    while len(iteration_folders) > max_iterations:
        oldest_iteration = iteration_folders.pop(0)
        shutil.rmtree(os.path.join(iterations_dir, oldest_iteration))


def execute_response(response):
    log_response(response)
    date_string = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    current_iteration_dir = os.path.join(iterations_dir, date_string)
    
    method = path = None
    is_codeblock = False
    codeblock_lines = []
    for line in response.split('\n'):
        if line.startswith(PROPOSAL) and not is_codeblock:
            run_operation(method, path, codeblock_lines, current_iteration_dir)
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
    run_operation(method, path, codeblock_lines, current_iteration_dir)
    
    cleanup_old_iterations()
    format_output("🎉 Operation completed successfully! 🎉", style=Style.BRIGHT, color=Fore.CYAN)
    
