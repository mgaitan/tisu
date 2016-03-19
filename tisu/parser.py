import re
from collections import namedtuple
from docutils.core import publish_doctree
from recommonmark.parser import CommonMarkParser
from tisu.models import Issue, Metadata


def get_metadata(text):
    regex = re.compile(r'^:(state|assignee|labels|milestone):\s*?(.*)',
                       flags=re.MULTILINE)
    meta = Metadata((k, v.strip()) for k, v in re.findall(regex, text))
    if 'labels' in meta:
        meta['labels'] = [l.strip() for l in meta['labels'].split(',')]
    return meta


def parser(path):

    with open(path) as fh:
        source = fh.read()
    lines = source.split('\n')
    dt = publish_doctree(source, parser=CommonMarkParser())

    tokens = {}

    for i, (sec_id, section) in enumerate(dt.ids.items()):
        if section.parent.tagname != 'document':
            continue
        text = section.astext()
        title = text.split('\n')[0].strip()
        number = None
        matched = re.match(r'(.*)\[#(\d+)]$', title)
        if matched:
            title, number = matched.groups()

        metadata = get_metadata(text)

        tokens[section.line] = (title.strip(),
                                int(number) if number else None,
                                metadata)
    k = list(sorted(tokens.keys()))
    k.append(len(lines) + 2)
    return [Issue(title=tokens[s][0],
                  number=tokens[s][1],
                  metadata=tokens[s][2],
                  body='\n'.join(lines[s:e - 2])) for s, e in zip(k, k[1:])]


if __name__ == '__main__':
    import sys
    parser(sys.argv[0])
