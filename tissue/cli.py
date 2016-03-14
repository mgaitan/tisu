"""Tissue: your issue tracker, in a text file

Usage:
  cli.py pull <repo> <markdown_file> [--state=<state>]
  cli.py push <markdown_file> <repo>

Options:
  -h --help         Show this screen.
  --version         Show version.
  --state=<state>   Filter by issue state [default: open].
"""

from docopt import docopt
from tissue.parser import fetcher


def pull(repo, path, state):
    issues = fetcher(repo, state)
    with open(path, 'w') as fh:
        for issue in issues:
            fh.write(issue.dump())


def main():
    args = docopt(__doc__, version='tissue 0.1')
    if args['pull']:
        pull(args['<repo>'], args['<markdown_file>'], args['--state'])


if __name__ == '__main__':
    main()
