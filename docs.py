import string

import functions


def generate_docs(output_path=None):
    docs_string = ""
    for group in functions.registry.all():
        for func in group.functions:
            docs_string += f"## (`{func.symbol}`) {func.name}"

            if len(func.params) > 0:
                param_strings = [f"`{arg.__name__}`" for arg in func.params]
                docs_string += " (" + ", ".join(param_strings) + ")"

            desc = func.desc
            for i, param in enumerate(func.params):
                a = string.ascii_lowercase[i]
                desc = desc.replace(f"%t{a}", "value" if param is ... else param.__name__)
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
