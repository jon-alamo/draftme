
# DraftMe

DraftMe is a Python library designed to assist in creating awesome code projects iteratively, with human supervision at every iteration. 

## Overview

The project allows users to send the current project file structure as part of the user prompt along with the change request for each iteration. There's a limit to the maximum number of tokens accepted by the OpenAI models, which can be a constraint for large-scale projects.

The functionality is encapsulated in a single command-line command `draftme`, which is followed by a string containing the change request. The root directory is the current working directory where a `.env` file must exist with a valid OpenAI API key named `OPENAI_API_KEY`.

## Installation

1. Clone the repository or download the source code.
2. Ensure you have Python installed.
3. Install the necessary dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

After setting up, you can use the `draftme` command to request changes. Ensure your `.env` file in the root directory contains your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

Use the command as follows:

```bash
draftme "Add a new function to example.py"
```

## Running Tests

You can run the test suite to ensure the functionality of the tool:

```bash
python -m unittest discover -s tests
```

## Example

Suppose you want to refactor a function in `example.py`. You would run:

```bash
draftme "Refactor function my_function in example.py"
```

The system will then analyze your request and the current state of the project, and make the necessary changes iteratively.

## Special Considerations

- Ensure the `.env` file is in the root directory.
- Remember the limitations regarding the number of tokens for the OpenAI model.
- For large-scale projects, consider breaking down change requests into smaller, more manageable parts.

## License

This project is licensed under the MIT License.

