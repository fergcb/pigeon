import argparse

from parser import parse
from interpreter import interpret
from stack import Stack

parser = argparse.ArgumentParser(
    prog="pigeon",
    description="An interpreter for the Pigeon programming language."
)

subparsers = parser.add_subparsers(help="subcommands", dest="subcommand", required=False)

run_parser = subparsers.add_parser("run", help="Run a Pigeon source file.")
run_parser.add_argument("file", type=str, help="The Pigeon source file to run.")
run_parser.add_argument("-e", dest="explain", action='store_true', help="Explain the code as it is executed.")

exec_parser = subparsers.add_parser("exec", help="Execute a string of Pigeon code.")
exec_parser.add_argument("code", type=str, help="The Pigeon code to run.")
exec_parser.add_argument("-e", dest="explain", action='store_true', help="Explain the code as it is executed.")

docs_parser = subparsers.add_parser("docs", help="Generate documentation.")
docs_parser.add_argument("-o", dest="output", help="Emit docs as a markdown file.")


def run_code(code: str, explain: bool):
    tokens = parse(code)
    interpret(tokens, explain)


def run_file(path: str, explain: bool):
    """
    Open a file and interpret the contents as Pigeon source code
    """
    try:
        f = open(path, "r", encoding="UTF-8")
    except IOError:
        print(f"Failed to open file '{path}'.")
        return
    else:
        with f:
            code = f.read()
            run_code(code, explain)


def run_repl():
    stack = Stack()

    while True:
        code = input(" >>> ")
        if code == ":exit":
            return
        tokens = parse(code)
        interpret(tokens, False, stack)
        print(stack)


def main():
    args = parser.parse_args()
    match args.subcommand:
        case "run":
            run_file(args.file, args.explain)
        case "exec":
            run_code(args.code, args.explain)
        case "docs":
            from docs import generate_docs
            generate_docs(args.output)
        case _:
            run_repl()


if __name__ == "__main__":
    main()
