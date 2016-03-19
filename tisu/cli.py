"""Tisú: your issue tracker, in a text file

Usage:
  tisu push <markdown_file> <repo> [--user=<user>] [--pass=<pass>]
  tisu pull <markdown_file> <repo> [--state=<state>]

Options:
  -h --help         Show this screen.
  --version         Show version.
  --state=<state>   Filter by issue state [default: open].
  --user=<user>     Github username to send issues. Repo's username if no given.
  --pass=<pass>     Github password. Prompt if no given.
"""

from docopt import docopt
from tisu.parser import parser
from tisu.gh import GithubManager
from getpass import getpass


def pull(repo, path, state):
    issues = GithubManager(repo).fetcher(state)
    with open(path, 'w') as fh:
        for issue in issues:
            fh.write(str(issue))


def push(path, repo, username, password):
    issues = parser(path)
    issues = GithubManager(repo, username, password).sender(issues)


def main():
    args = docopt(__doc__, version='tissue 0.1')
    if args['pull']:
        pull(args['<repo>'], args['<markdown_file>'], args['--state'])

    elif args['push']:
        password = args.get('<pass>', getpass('Github password: '))
        username = args.get('<user>', args['<repo>'].split('/')[0])
        push(args['<markdown_file>'], args['<repo>'], username, password)


if __name__ == '__main__':
    main()
