import string
from types import UnionType
from typing import get_origin, get_args

import functions


def stringify_type(param: type) -> str:
    if param is any:
        return "any"
    if get_origin(param) is UnionType:
        return "/".join([stringify_type(a) for a in get_args(param)])
    return param.__name__


def generate_docs(output_path=None):
    docs_string = ""
    for group in functions.registry.all():
        for func in group.functions:
            docs_string += f"## (`` {func.symbol} ``) {func.name}"

            params = [stringify_type(param) for param in func.params]
            pairs = [(string.ascii_lowercase[i], param) for i, param in enumerate(params)]

            if len(func.params) > 0:
                docs_string += " (" + ", ".join(f"`` {name}: {param} ``" for name, param in pairs) + ")"

            return_type = func.return_type
            rt_string = "`void`" if return_type is None else ("`` " + stringify_type(return_type) + " ``") + ":"
            docs_string += " -> " + rt_string

            desc = func.desc
            for name, param in pairs:
                desc = desc.replace(f"%t{name}", param if param != "any" else "value")
                desc = desc.replace(f"%{name}", f"`{name}`")

            docs_string += "\n" + desc + "\n\n"

    if output_path is None:
        print(docs_string)
    else:
        try:
            f = open(output_path, "w")
            f.write(docs_string)
        except IOError:
            print(f"Failed to open file '{output_path}'.")
            return
        else:
            f.close()
