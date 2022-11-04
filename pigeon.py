import argparse

from parser import parse
from interpreter import interpret

parser = argparse.ArgumentParser(
    prog="pigeon",
    description="An interpreter for the Pigeon programming language."
)

subparsers = parser.add_subparsers(help="subcommands", dest="subcommand", required=True)

run_parser = subparsers.add_parser("run", help="Run a Pigeon source file.")
run_parser.add_argument("file", type=str, help="The Pigeon source file to run.")
run_parser.add_argument("-e", dest="explain", action='store_true', help="Explain the code as it is executed.")


def run_file(path: str, explain: bool):
    """
    Open a file and interpret the contents as Pigeon source code
    """
    try:
        f = open(path, "r")
    except IOError:
        print(f"Failed to open file '{path}'.")
        return
    else:
        with f:
            code = f.read()
            tokens = parse(code)
            interpret(tokens, explain)


def main():
    args = parser.parse_args()
    match args.subcommand:
        case "run":
            run_file(args.file, args.explain)


if __name__ == "__main__":
    main()
