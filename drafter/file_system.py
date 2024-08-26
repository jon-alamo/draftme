import os
import dotenv

dotenv.load_dotenv('.env')
DEFAULT_EXCLUDES = ['__*', '.*']
DEFAULT_INCLUDES = ['__init__.py']

exclude = os.getenv('EXCLUDE', 'build').split(',') + DEFAULT_EXCLUDES
include = os.getenv('INCLUDE', '*').split(',') + DEFAULT_INCLUDES


def match_string(string: str, pattern: str) -> bool:
    if not pattern:
        return not string
    elif not string:
        return pattern == '*'

    if pattern[0] == '*':
        return match_string(string, pattern[1:]) or (
                    bool(string) and match_string(string[1:], pattern))

    if pattern[0] == '?':
        return bool(string) and match_string(string[1:], pattern[1:])

    if pattern[0] == string[0]:
        return match_string(string[1:], pattern[1:])

    return False


def is_valid_item(item):
    if item.endswith('/'):
        item = item[:-1]
    item = os.path.basename(item)
    if any([match_string(item, pattern) for pattern in include]):
        return True
    if any([match_string(item, pattern) for pattern in exclude]):
        return False


def iterate_project_path(path):
    items = [os.path.join(path, item) for item in os.listdir(path)]
    for item in filter(is_valid_item, items):
        if os.path.isdir(item):
            yield from iterate_project_path(item)
        elif os.path.isfile(item):
            yield item


def generate_file_structure(path):
    structure = ['Project file structure:']
    structure = structure + ['├── ' + item for item in iterate_project_path(path)]
    structure[-1] = structure[-1].replace('├── ', '└── ')
    return '\n'.join(structure)


def get_file_content(f):
    try:
        return f.read()
    except:
        return '<encoded file>'


def generate_file_contents(path):
    content = []
    for item in iterate_project_path(path):
        if os.path.isdir(item):
            content.append(generate_file_contents(item))
        elif os.path.isfile(item):
            with open(item, 'r', encoding='utf-8') as f:
                file_content = get_file_content(f)
                content.append((
                    f'File: {item}:\n'
                    f'{{file_content}}\n{file_content}\n{{file_content}}'
                    '\n'
                ))
    return '\n'.join(content)

