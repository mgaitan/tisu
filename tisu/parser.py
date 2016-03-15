import re
from docutils.core import publish_doctree
from recommonmark.parser import CommonMarkParser
from github import Github
from .models import Issue


def parser(path):
    with open(path) as fh:
        source = fh.read()
    lines = source.split('\n')
    dt = publish_doctree(source, parser=CommonMarkParser())
    tokens = {}

    for i, (sec_id, section) in enumerate(dt.ids.items()):
        if section.parent.tagname != 'document':
            continue
        title = section.astext().split('\n')[0].strip()
        number = None
        matched = re.match(r'(.*)\[#(\d+)]$', title)
        if matched:
            title, number = matched.groups()
        tokens[section.line] = title.strip(), int(number) if number else None
    k = list(sorted(tokens.keys()))
    k.append(len(lines) + 2)
    return [Issue(title=tokens[s][0], number=tokens[s][1],
                  body='\n'.join(lines[s:e - 2])) for s, e in zip(k, k[1:])]


def fetcher(repo, state):
    g = Github()
    repo = g.get_repo(repo)
    issues = []
    for issue in repo.get_issues(state=state):
        issues.append(Issue(issue.title, issue.body, issue.number))
    return issues


def writer(repo, issues):
    g = Github()
    repo = g.get_repo(repo)
    import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    from pprint import pprint
    pprint(fetcher('mgaitan/waliki'))
