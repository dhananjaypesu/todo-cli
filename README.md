# todo-cli

A small command-line to-do list manager written in Python. Tasks are stored in a JSON file (`~/.todo.json` by default).

## Usage

```bash
python -m todo add Buy groceries
python -m todo list
python -m todo done 1
python -m todo list --all
python -m todo remove 1
```

Use `--file path/to/tasks.json` to work with a different task file.

## Tests

```bash
pip install pytest
pytest
```
