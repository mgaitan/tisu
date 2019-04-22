"""Tisú: your issue tracker, in a text file

Usage:
  tisu push <markdown_file> [--repo=<repo>] [--user=<user>] [--pass=<pass>]
  tisu pull <markdown_file> [--repo=<repo>] [--state=<state>]

Options:
  -h --help         Show this screen.
  --version         Show version.
  --repo=<repo>     Github repo (as: user/name). [default: inferred from git remote]
  --state=<state>   Filter by issue state [default: open].
  --user=<user>     Github username to send issues. Repo's username if no given.
  --pass=<pass>     Github password. Prompt if no given.
"""
from getpass import getpass
import re
from subprocess import check_output
from docopt import docopt
from .parser import parser
from .gh import GithubManager


def pull(repo, path, state):
    issues = GithubManager(repo).fetcher(state)
    with open(path, 'w') as fh:
        for issue in issues:
            fh.write(str(issue))


def push(path, repo, username, password):
    issues = parser(path)
    issues = GithubManager(repo, username, password).sender(issues)


def github_from_git():
    s = check_output(['git', 'remote', '-v'])
    return re.findall(r'[\w\-]+\/[\w\-]+', s.decode('utf8'))[0]


def main():
    args = docopt(__doc__, version='tissue 0.1')
    repo = args['--repo'] if args['--repo'] != 'inferred from git remote' else github_from_git()
    if args['pull']:
        pull(repo, args['<markdown_file>'], args['--state'])

    elif args['push']:
        password = args['--pass'] or getpass('Github password: ')
        username = args.get('--user', repo.split('/')[0])
        push(args['<markdown_file>'], repo, username, password)


if __name__ == '__main__':
    main()
