import re
from pathlib import Path

from docutils.core import publish_doctree
from recommonmark.parser import CommonMarkParser

from .models import Issue, Metadata

META_REGEX = re.compile(
    r"^:(state|assignee|labels|milestone|parent|project|issuetype):\s*?(.*)\r?\n?", flags=re.MULTILINE
)


def get_metadata(text):
    meta = Metadata((k, v.strip()) for k, v in re.findall(META_REGEX, text))
    if "labels" in meta:
        meta["labels"] = [label.strip() for label in meta["labels"].split(",")]
    return meta


def clean_metadata(text):
    return re.sub(META_REGEX, "", text)


def parser(path: Path | str) -> list[Issue]:
    if isinstance(path, str):
        path = Path(path)

    source = path.read_text()
    lines = source.split("\n")
    dt = publish_doctree(source, parser=CommonMarkParser())

    tokens = {}

    for _i, (_sec_id, section) in enumerate(dt.ids.items()):
        if section.parent.tagname != "document":
            continue
        text = section.astext()
        title = text.split("\n")[0].strip()
        number = None
        matched = re.match(r"^\[#(\d+)]\s*?(.*)$", title)
        if matched:
            number, title = matched.groups()

        metadata = get_metadata(text)

        tokens[section.line] = (title.strip(), int(number) if number else None, metadata)
    k = sorted(tokens.keys())
    k.append(len(lines) + 2)
    return [
        Issue(
            title=tokens[s][0],
            number=tokens[s][1],
            metadata=tokens[s][2],
            body=clean_metadata("\n".join(lines[s : e - 2])),
        )
        for s, e in zip(k, k[1:])
    ]


if __name__ == "__main__":
    import sys

    parser(sys.argv[0])
