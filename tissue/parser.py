from docutils.core import publish_doctree


def issue_parser(source):
    lines = source.split('\n')
    dt = publish_doctree(source)
    titles = []
    tokens = {}

    for i, (sec_id, section) in enumerate(dt.ids.items()):
        if section.parent.tagname != 'document':
            continue
        title = section.astext().split('\n')[0]
        tokens[section.line] = title
    k = list(sorted(tokens.keys()))
    k.append(len(lines) + 2)
    return [(tokens[s], '\n'.join(lines[s:e - 2])) for s, e in zip(k, k[1:])]

