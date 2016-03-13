from docutils.core import publish_doctree

from github import Github

def parser(path):
    with open(path) as fh:
        source = fh.read()
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


def fetcher(repo):

    g = Github()
    repo = g.get_repo(repo)
    issues = []
    for issue in repo.get_issues(state='open'):
        issues.append((issue.title, issue.body))
    return issues

if __name__ == '__main__':
    from pprint import pprint
    pprint(fetcher('mgaitan/waliki'))
