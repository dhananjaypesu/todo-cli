"""Command-line entry point."""

import argparse
import sys

from . import __version__
from .store import DEFAULT_PATH, TaskStore


def build_parser():
    parser = argparse.ArgumentParser(prog="todo", description="Manage a simple to-do list.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--file", default=DEFAULT_PATH, help="path to the task file")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("title", nargs="+")

    ls = sub.add_parser("list", help="list tasks")
    ls.add_argument("--all", action="store_true", help="include completed tasks")

    done = sub.add_parser("done", help="mark a task as completed")
    done.add_argument("id", type=int)

    rm = sub.add_parser("remove", help="delete a task")
    rm.add_argument("id", type=int)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    store = TaskStore(args.file)

    try:
        if args.command == "add":
            task = store.add(" ".join(args.title))
            print(f"Added #{task['id']}: {task['title']}")
        elif args.command == "list":
            tasks = store.tasks if args.all else store.pending()
            if not tasks:
                print("Nothing to do.")
            for t in tasks:
                mark = "x" if t["done"] else " "
                print(f"[{mark}] #{t['id']} {t['title']}")
        elif args.command == "done":
            task = store.complete(args.id)
            print(f"Completed #{task['id']}: {task['title']}")
        elif args.command == "remove":
            task = store.remove(args.id)
            print(f"Removed #{task['id']}: {task['title']}")
    except KeyError as exc:
        print(exc.args[0], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
