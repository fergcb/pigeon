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
run_parser.add_argument("-e", dest="explain", action="store_true", help="Explain the code as it is executed.")
run_parser.add_argument("-i", dest="input", type=str, help="An input file to be pushed to the stack.")

exec_parser = subparsers.add_parser("exec", help="Execute a string of Pigeon code.")
exec_parser.add_argument("code", type=str, help="The Pigeon code to run.")
exec_parser.add_argument("-e", dest="explain", action='store_true', help="Explain the code as it is executed.")
exec_parser.add_argument("-i", dest="input", type=str, help="An input file to be pushed to the stack.")

docs_parser = subparsers.add_parser("docs", help="Generate documentation.")
docs_parser.add_argument("-o", dest="output", help="Emit docs as a markdown file.")


def read_file(path: str) -> str | None:
    try:
        f = open(path, "r", encoding="UTF-8")
    except IOError:
        return None
    else:
        return f.read()


def run_code(code: str, explain: bool, input_path: str):
    input_text = read_file(input_path)
    if input_text is None:
        print("Failed to open input file '%s'." % (input_path,))
        return

    tokens = parse(code)
    interpret(tokens, explain, Stack([input_text]))


def run_file(path: str, explain: bool, input_path: str):
    """
    Open a file and interpret the contents as Pigeon source code
    """
    code = read_file(path)
    if code is None:
        print("Failed to open source file '%s'." % (path,))
        return

    run_code(code, explain, input_path)


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
            run_file(args.file, args.explain, args.input)
        case "exec":
            run_code(args.code, args.explain, args.input)
        case "docs":
            from docs import generate_docs
            generate_docs(args.output)
        case _:
            run_repl()


if __name__ == "__main__":
    main()
