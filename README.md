
# DraftMe

DraftMe is a Python command tool designed to assist in starting awesome code projects iteratively, with human supervision at every iteration. 

## Overview

The project allows users to send the current project file structure as part of the user prompt along with the change request for each iteration. There's a limit to the maximum number of tokens accepted by the OpenAI models, which can be a constraint for large-scale projects.

The functionality is encapsulated in a single command-line command `draftme`, which is followed by a string containing the change request. The root directory is the current working directory where a `.env` file must exist with a valid OpenAI API key named `OPENAI_API_KEY`.

## Installation

1. Ensure Python (and pip) is installed in your system.
2. From a terminal, install the tool with:
    ```bash
    pip install git+https://github.com/jon-alamo/draftme.git
    ```

## Usage

1. From the terminal, create a new directory where to start a new project or navigate to an existing one.
2. Ensure a `.env` file exists in the root directory with your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```
3. Use the command `draftme` followed by a string with requested changes to the project as follows:
   ```bash
   draftme "Add a new function to example.py"
   ```

## Warning!!
- Changes on you project files are done automatically and are permanent, so there's no way to recover files once those have been changed so consider using git for version control and track every change by commiting before running the draftme command. 

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

