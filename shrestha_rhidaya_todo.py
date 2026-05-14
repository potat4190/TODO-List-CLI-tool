"""
TODO List CLI Tool
==================
Final Project for CINF108 --- Rhidaya Shrestha (rshrestha2@albany.edu)

A TODO list command line tool.

Here are some of the sources I got help from:
1. https://stackoverflow.com/questions/66597855/creating-todolist-using-python-oop
2. https://stackoverflow.com/questions/65328753/how-to-solve-command-line-problem-using-python-argparse
3. https://www.geeksforgeeks.org/python/python-exit-commands-quit-exit-sys-exit-and-os-_exit/
4. https://stackoverflow.com/questions/7427101/simple-argparse-example-wanted-1-argument-3-results
"""

import argparse
import csv
import os
import sys


VALID_CATEGORIES = ["project", "homework", "study", "other"]
VALID_STATUSES = ["incomplete", "in-progress", "complete"]

# The text written at the top of every TODO csv file.
FILE_HEADER = "id,category,description,status"

class TodoItem:
    """Represents one entry on the TODO list."""

    def __init__(self, item_id, category, description, status):
        # We force item_id to be an int.
        self.item_id = int(item_id)
        self.category = category
        self.description = description
        self.status = status

    def to_csv_line(self):
        """
        Turn this item into one comma-separated line for the file.
        """
        return f"{self.item_id},{self.category},{self.description},{self.status}"

    def display_line(self):
        """Return a tab-separated line for printing this item to the screen."""
        return f"{self.item_id}\t|\t{self.category}\t|\t{self.status}\t|\t{self.description}"


class TodoList:
    """Manages a collection of TodoItem objects, backed by a CSV file on disk."""

    def __init__(self, filename):
        # os.path.abspath turns a relative path like "TODO.csv" into the
        # full absolute path. Storing the absolute path means our error
        # messages can show the user exactly where on disk the file lives.
        self.filename = os.path.abspath(filename)
        self.items = []
        # Load any existing items right away so the in-memory list matches
        # whatever is currently saved to disk.
        self.load()

    def load(self):
        """Read items from self.filename, if the file exists."""
        if not os.path.exists(self.filename):
            return

        f = open(self.filename, "r", encoding="utf-8", newline="")
        reader = csv.reader(f)
        rows = list(reader)
        f.close()

        # An empty file has nothing to load.
        if len(rows) == 0:
            return

        # The very first row should be our header row. If it isn't, the user has pointed --list-name at some other csv and we refuse to touch it (we don't want to overwrite their data).
        header_line = ",".join(rows[0])
        if header_line != FILE_HEADER:
            print(
                f"Error: '{self.filename}' does not look like a TODO file. "
                f"Expected first line '{FILE_HEADER}', got '{header_line}'."
            )
            sys.exit(1)

        # Walk every row *after* the header and turn it into a TodoItem.
        for row in rows[1:]:
            if len(row) == 0:
                continue
            if len(row) < 4:
                print(f"Warning: skipping malformed line: {','.join(row)}")
                continue
            file_id = row[0]
            file_category = row[1]
            file_description = ",".join(row[2:-1])
            file_status = row[-1]
            new_item = TodoItem(
                file_id, file_category, file_description, file_status
            )
            self.items.append(new_item)

    def save(self):
        """Write every in-memory item back out to the CSV file."""
        f = open(self.filename, "w", encoding="utf-8")
        # Always write the header line first so the next load() can recognise the file as one of our TODO lists.
        f.write(FILE_HEADER + "\n")
        for item in self.items:
            f.write(item.to_csv_line() + "\n")
        f.close()

    def next_id(self):
        """Return the next free id number to give to a brand new item."""
        # If there are no items yet, start counting at 1.
        if len(self.items) == 0:
            return 1
        # Otherwise the new id is one more than the current highest id.
        highest = 0
        for item in self.items:
            if item.item_id > highest:
                highest = item.item_id
        return highest + 1

    def find_by_id(self, item_id):
        """Return the item with the given id, or None if no match."""
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    def add_item(self, category, description, status):
        """Create a new TodoItem, append it to the list, and return it."""
        new_item = TodoItem(self.next_id(), category, description, status)
        self.items.append(new_item)
        return new_item

    def display(self):
        """Print every item in the list to the terminal."""
        short_name = os.path.basename(self.filename)
        print()
        print(f"--- TODO LIST ({short_name}) ---")
        if len(self.items) == 0:
            print("(no items yet -- use the 'add' command to create one)")
            print()
            return
        # Header row of the table.
        print("ID\t|\tCATEGORY\t|\tSTATUS\t\t|\tDESCRIPTION")
        print("-" * 80)
        for item in self.items:
            print(item.display_line())
        print()



# Small helper functions that print friendly error messages and quit.


def error_exit(message):
    """Print a single error line and exit with a non-zero status."""
    print(f"Error: {message}")
    sys.exit(1)


def check_required(value, flag_name):
    """Quit if the user did not supply a required optional flag."""
    if value is None:
        error_exit(f"missing required argument {flag_name}.")


def check_allowed(value, allowed_values, flag_name):
    """Quit if value is not one of the allowed options for this flag."""
    if value not in allowed_values:
        # Build a list of what the allowed values are.
        options = ", ".join(allowed_values)
        error_exit(
            f"invalid value '{value}' for {flag_name}. "
            f"Must be one of: {options}."
        )


def parse_id(raw_id):
    """Convert a user-typed --id string into an int (quits on bad input)."""
    if not raw_id.isdigit():
        error_exit(f"--id must be a number, got '{raw_id}'.")
    return int(raw_id)


# Main entry point

def main():
    parser = argparse.ArgumentParser(
        description=(
            "A simple TODO list CLI tool. Tasks are saved in a CSV file so "
            "they persist between runs. Use --list-name to manage multiple "
            "separate lists."
        )
    )

    parser.add_argument(
        "command",
        help="Action to perform: view, add, status, or edit",
    )

    parser.add_argument(
        "-n", "--list-name",
        help="Path to the TODO list CSV file (default: TODO.csv)",
        default="TODO.csv",
    )

    parser.add_argument(
        "-c", "--category",
        help="Category for the task (project, homework, study, other)",
    )

    parser.add_argument(
        "-d", "--description",
        help="Description text for the task",
    )

    parser.add_argument(
        "-s", "--status",
        help="Status (incomplete, in-progress, complete)",
    )

    parser.add_argument(
        "-i", "--id",
        help="ID number of the item to update or edit",
    )

    args = parser.parse_args()

    todo_list = TodoList(args.list_name)


    if args.command == "view":
        # No extra arguments needed, just shows the list.
        todo_list.display()

    elif args.command == "add":
        # Adding requires a category and a description. Status is optional and falls back to "incomplete" if the user doesn't supply one.
        check_required(args.category, "--category")
        check_required(args.description, "--description")
        check_allowed(args.category, VALID_CATEGORIES, "--category")

        new_status = args.status
        if new_status is None:
            new_status = "incomplete"
        check_allowed(new_status, VALID_STATUSES, "--status")

        new_item = todo_list.add_item(
            args.category, args.description, new_status
        )
        todo_list.save()
        short_name = os.path.basename(todo_list.filename)
        print(
            f"Added item #{new_item.item_id} to '{short_name}': "
            f"[{new_item.category}] {new_item.description} "
            f"({new_item.status})"
        )

    elif args.command == "status":
        # A status change requires both an id and the new status value.
        check_required(args.id, "--id")
        check_required(args.status, "--status")
        check_allowed(args.status, VALID_STATUSES, "--status")

        target_id = parse_id(args.id)
        item = todo_list.find_by_id(target_id)
        if item is None:
            error_exit(f"no item with id {target_id} in this list.")
        item.status = args.status
        todo_list.save()
        print(f"Item #{item.item_id} status set to '{item.status}'.")

    elif args.command == "edit":
        # Editing requires an id, plus at least one field to change.
        check_required(args.id, "--id")
        if (
            args.category is None
            and args.description is None
            and args.status is None
        ):
            error_exit(
                "nothing to edit. Provide at least one of "
                "--category, --description, or --status."
            )
        target_id = parse_id(args.id)
        item = todo_list.find_by_id(target_id)
        if item is None:
            error_exit(f"no item with id {target_id} in this list.")
        if args.category is not None:
            check_allowed(args.category, VALID_CATEGORIES, "--category")
            item.category = args.category
        if args.description is not None:
            item.description = args.description
        if args.status is not None:
            check_allowed(args.status, VALID_STATUSES, "--status")
            item.status = args.status
        todo_list.save()
        print(
            f"Updated item #{item.item_id}: [{item.category}] "
            f"{item.description} ({item.status})"
        )

    else:
        # Anything else is an unrecognised command. Show the user a hint.
        error_exit(
            f"unknown command '{args.command}'. "
            f"Valid commands are: view, add, status, edit."
            f"\nUse --help for help"
        )


if __name__ == "__main__":
    main()
