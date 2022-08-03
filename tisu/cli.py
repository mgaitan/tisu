"""
Tisú: your issue tracker, in a text file

Usage:
  tisu push <markdown_file> [--repo=<repo>] [(--username=<username> [--pass=<pass>]|--token=<token>)]
  tisu pull <markdown_file> [--repo=<repo>] [--state=<state>] [(--username=<username> [--pass=<pass>]|--token=<token>)]

Options:
  -h --help                 Show this screen.
  --version                 Show version.
  --repo=<repo>             Github repo (as: user/name). [default: inferred from git remote]
  --state=<state>           Filter by issue state [default: open].
  --username=<username>     Github username to send issues. Repo's username if no given.
  --pass=<pass>             Github password. Prompt if user is given and it is not.
  --token=<token>           Personal app token. Default to GITHUB_TOKEN environment variable.
                            Get one at https://github.com/settings/tokens
"""
import os
import re
from getpass import getpass
from subprocess import check_output

from docopt import docopt

from .gh import GithubManager
from .parser import parser

__version__ = "1.2"


def pull(repo, path, state, username_or_token=None, password=None):
    issues = GithubManager(repo, username_or_token, password).fetcher(state)
    with open(path, 'w') as fh:
        for issue in issues:
            fh.write(str(issue))


def push(path, repo, username_or_token, password):
    issues = parser(path)
    issues = GithubManager(repo, username_or_token, password).sender(issues)


def github_from_git():
    s = check_output(['git', 'remote', '-v'])
    return re.findall(r'[\w\-]+\/[\w\-]+', s.decode('utf8'))[0]


def main():
    args = docopt(__doc__, version=__version__)
    repo = args['--repo'] if args['--repo'] != 'inferred from git remote' else github_from_git()
    token = args.get('--token') or os.environ.get("GITHUB_TOKEN")
    
    username = args.get('--username', repo.split('/')[0])
    password = args.get('--pass', getpass('Github password: ') if not token else None)

    if args['pull']:
        pull(repo, args['<markdown_file>'], args['--state'], username_or_token=token or username, password=password)
    elif args['push']:
        push(args['<markdown_file>'], repo, token or username, password)


if __name__ == '__main__':
    main()
