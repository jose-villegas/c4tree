"""The comment a C or C++ file opens with, as prose: what a module says it is."""
import re

C_SUFFIXES = (".c", ".h", ".cc", ".cpp", ".cxx", ".hh", ".hpp", ".hxx")
PRAGMA_ONCE = re.compile(r"\A\s*#\s*pragma\s+once[^\n]*\n")


def top_comment(text):
    """The file's first comment, when only whitespace or a leading `#pragma
    once` comes before it, as its prose lines: comment markers and leading
    `*` stripped, blank lines kept as "". A run of `//` lines is one comment;
    a blank line or code ends it. None when code comes first."""
    head = PRAGMA_ONCE.sub("", text, count=1).lstrip()
    if head.startswith("/*"):
        end = head.find("*/", 2)
        body = head[2:end if end >= 0 else len(head)]
        return [re.sub(r"^\*+", "", re.sub(r"^/?\*+$", "", line.strip())).strip() for line in body.split("\n")]
    if head.startswith("//"):
        lines = []
        for line in head.split("\n"):
            if not line.strip().startswith("//"):
                break
            lines.append(re.sub(r"^//+", "", line.strip()).strip())
        return lines
    return None

