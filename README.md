# TODO-LIST

A command line interface (CLI) tool, written in Python, for managing a TODO list.

This is the final project for **CINF108**.

---

## 1. Core Functionalities

The tool exposes four actions from the command line:

1. **View** - print every task in the list as a table.
2. **Add** - create a new task with a category, description, and status.
3. **Status** - change the completion status of an existing task by id.
4. **Edit** - change one or more fields (category, description, status) of
   an existing task by id.

Every TODO item stores four pieces of information:

| Field         | Type     | Meaning                                                              |
| ------------- | -------- | -------------------------------------------------------------------- |
| `id`          | integer  | Unique numeric identifier, assigned automatically when an item is added. |
| `category`    | string   | One of: `project`, `homework`, `study`, `other`.                     |
| `description` | string   | Free-text description of what the task involves.                     |
| `status`      | string   | One of: `incomplete`, `in-progress`, `complete`.                     |

The list is saved automatically after every change, so you never have to
remember to save the file manually. The default file is `TODO.csv` in the
current folder, but the `--list-name` flag lets you point the tool at any
other file (e.g. `work-todo.csv`, `chores.csv`) to manage multiple lists.

---

## 2. How to Run the Code

### General form

```
python shrestha_rhidaya_todo.py <command> [options]
```

`<command>` is a required positional argument that says which action to
perform. Options use a short flag (`-c`) or a long flag (`--category`).

### 2.1 `view` - Display the list

Shows every task in the file as a tab-separated table with a header row.

```
python shrestha_rhidaya_todo.py view
```


If the file is empty, you get a friendly message instead of an empty table.

### 2.2 `add` - Add a new task

- Required: `--category` (`-c`) and `--description` (`-d`).
- Optional: `--status` (`-s`) - defaults to `incomplete` if not given.

```
python shrestha_rhidaya_todo.py add -c homework -d "Math chapter 3"
python shrestha_rhidaya_todo.py add -c project -d "CINF108 final" -s in-progress
```

The id is assigned automatically (always the current highest id + 1, or
`1` if the list is empty).

### 2.3 `status` - Change the status of a task

- Required: `--id` (`-i`) and `--status` (`-s`).

```
python shrestha_rhidaya_todo.py status -i 1 -s complete
python shrestha_rhidaya_todo.py status -i 2 -s in-progress
```

### 2.4 `edit` - Update an existing task

- Required: `--id` (`-i`), plus **at least one** of `--category`,
  `--description`, or `--status` (otherwise there is nothing to change
  and the program will refuse the request).

```
python shrestha_rhidaya_todo.py edit -i 2 -d "Updated description"
python shrestha_rhidaya_todo.py edit -i 1 -c project -s complete
```

Any field you do not pass is left untouched.

### 2.5 `--list-name` - Manage multiple lists

By default the tool reads from and writes to `TODO.csv`. Pass `-n`
(or `--list-name`) followed by any filename to manage a separate list:

```
python shrestha_rhidaya_todo.py -n work-todo.csv add -c other -d "Email professor"
python shrestha_rhidaya_todo.py -n work-todo.csv view
python shrestha_rhidaya_todo.py -n chores.csv add -c other -d "Buy groceries"
```

The flag goes before the command word because argparse parses all of the
top-level options together.

### 2.6 `--help` - Built-in usage info

argparse generates a help screen automatically:

```
python shrestha_rhidaya_todo.py --help
python shrestha_rhidaya_todo.py -h
```

## 3. Concepts Used and Important Details

This section explains the Python concepts the program is built on, in
roughly the order they appear in the file.

### 3.1 Modules

The script imports four standard-library modules at the top:

- **`argparse`**
- **`csv`**
- **`os`**
- **`sys`**

### 3.2 Constants

At the top of the file there are three module-level constants:

- `VALID_CATEGORIES = ["project", "homework", "study", "other"]`
- `VALID_STATUSES   = ["incomplete", "in-progress", "complete"]`
- `FILE_HEADER      = "id,category,description,status"`

### 3.3 `TodoItem` class

Represents one task on the list.


### 3.4 `TodoList` class

Represents the whole list and handles everything to do with the file.


### 3.5 Helper functions for input validation

Instead of crashing with a Python traceback when the user makes a
mistake, the script funnels every error through four tiny helpers:


### 3.6 The CSV save file

The default file is `TODO.csv` and it always starts with the header line:

```
id,category,description,status
```

---
