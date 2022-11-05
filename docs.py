import string

import functions


def generate_docs(output_path=None):
    docs_string = ""
    for function in functions.get_all():
        docs_string += f"\n## `{function.symbol}`\n"
        docs_string += f"**Vectorizable?** {'Yes' if function.allow_arrays else 'No'}\n"
        docs_string += f"### Signatures:\n"
        for sig in function.sigs:
            arg_types, action, desc = sig
            for i, arg in enumerate(arg_types):
                a = string.ascii_lowercase[i]
                desc = desc.replace(f"%t{a}", "value" if arg is ... else arg.__name__)
            if len(arg_types) > 0:
                types = ", ".join(["`any`" if arg is ... else f"`{arg.__name__}`" for arg in arg_types])
            else:
                types = "None"
            docs_string += f"- **{types}**: {desc}\n"

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
