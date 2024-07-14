import os
import dotenv

dotenv.load_dotenv('.env')
exclude = os.getenv('EXCLUDE').split(',')

EXCLUDE_DIR_STARTS = ['__', '.']
EXCLUDE_FIL_STARTS = ['.']


def is_valid_dir(dirname):
    if dirname.endswith('/'):
        dirname = dirname[:-1]
    dirname = os.path.basename(dirname)
    if dirname in exclude:
        return False
    return not any(dirname.startswith(patt) for patt in EXCLUDE_DIR_STARTS)


def is_valid_file(file_name):
    if file_name.endswith('/'):
        file_name = file_name[:-1]
    file_name = os.path.basename(file_name)
    if file_name in exclude:
        return False
    return not any(file_name.startswith(patt) for patt in EXCLUDE_FIL_STARTS)


def is_valid_item(item):
    if os.path.isdir(item):
        return is_valid_dir(item)
    if os.path.isfile(item):
        return is_valid_file(item)
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


def generate_file_contents(path):
    content = []
    for item in iterate_project_path(path):
        if os.path.isdir(item):
            content.append(generate_file_contents(item))
        elif os.path.isfile(item):
            with open(item, 'r') as f:
                content.append((
                    f'File: {item}:\n'
                    f'{{file_content}}\n{f.read()}\n{{file_content}}'
                    '\n'
                ))
    return '\n'.join(content)

