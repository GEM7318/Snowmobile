"""
Module contains parsing utilities used by :class:`Script`, :class:`Statement`,
:class:`Markup`, and :class:`Section`.
"""
from typing import List, Tuple


def up(nm: str):
    """Utility to truncate upper-casing strings as opposed to str.upper()."""
    return nm.upper() if nm else nm


def strip(val: str, trailing: bool = True, blanks: bool = True) -> str:
    """Utility to strip a variety whitespace from a string."""
    splitter = val.split("\n")
    if trailing:
        splitter = [v.strip() for v in splitter]
    if blanks:
        splitter = [v for v in splitter if v and not v.isspace()]
    return "\n".join(splitter)


# -- arg_to_list test cases
# input_to_expected = [
#     (
#         """['.*_ignore', "ignore.*",'dummy pattern']""",
#         ['.*_ignore', 'ignore.*', 'dummy pattern']
#     ),
# ]
# for item in input_to_expected:
#     input, expected = item
#     assert arg_to_list(input) == expected


def dict_flatten(
    attrs: dict, delim: str = None, indent_char: str = None, bullet_char: str = None
) -> List[Tuple[str, str, str]]:
    """Flattens a dictionary to its atomic state and performs parsing operations.

    Recursively flattens dictionary to its atomic elements, separating each
    child key with a `delim` relative to its parent key. This flattening
    enables the parsing of a dictionary into a valid set of nested markdown
    bullets with indents mirroring its hierarchy.

    Args:
        attrs (dict):
            Dictionary of attributes; most likely the :attr:`attrs_parsed`
            from :class:`Statement`.
        delim (str):
            Delimiter to use for separating nested keys; defaults to '~';
        indent_char (str):
            Character to use for indents; defaults to a tab ('\t).
        bullet_char (str):
            Character to use for bullets/sub-bullets; defaults to '-'.

    Returns (List[Tuple[str, str, str]]):
        A list of tuples containing:
            1.  A string of the indentation to use; for 1st-level attributes,
                this will just be the `bullet_char`.
            2.  The fully stratified key, including parents; for 1st-level
                attributes this will mirror the original key that was provided.
            3.  The value of the associated key; this will always mirror the
                value that was provided.

    """
    flattened = list()
    delim = delim or "~"
    c = indent_char or "\t"
    bullet_char = bullet_char or "-"

    def recurse(t, parent_key=""):
        if isinstance(t, dict):
            for k, v in t.items():
                sub_key = f"{parent_key}{delim}{k}"
                recurse(v, sub_key if parent_key else k)
        else:
            depth = len(parent_key.split(delim)) - 1
            indent = f"{c * depth}{bullet_char}" if depth else ""
            flattened.append((indent, parent_key, t))

    recurse(attrs)

    return flattened


def p(nm: str) -> Tuple[str, str]:
    """Utility to parse schema from dot-prefixed object if included."""
    nm = nm or str()
    partitions = [p for p in nm.partition('.') if p]
    if len(partitions) == 3:
        schema, _, name = partitions
    elif nm.strip().startswith('__'):
        schema, name = nm.strip()[2:], str()
    else:
        schema, name = str(), nm.strip()
    return schema, name
