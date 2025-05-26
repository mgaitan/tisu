"""
Tisú: your issue tracker, in a text file

Usage:
  tisu push <markdown_file> [--tracker=<tracker>] [--repo=<repo> | --project=<project>] [--state=<state>] ...
  tisu pull <markdown_file> [--tracker=<tracker>] [--repo=<repo> | --project=<project>] [--state=<state>] ...
  tisu (-h | --help)
  tisu --version

Options:
  --tracker=<tracker>      issue backend: [default: github] or "jira"
  --repo=<repo>            Github repo (as: user/name). [default: inferred from git remote]

  --project=<project>      JIRA project key (e.g. PROJ) - only if --tracker=jira
  --server=<server>        URL of the server
  --version                Show version.
  --state=<state>          Filter by issue state [default: open].
  --username=<username>    Github username to send issues. Repo's username if no given.
  --pass=<pass>            Github password. Prompt if user is given and it is not.
  --token=<token>          Personal app token. Default to GITHUB_TOKEN or JIRA_TOKEN environment variable.
                           Get one at https://github.com/settings/tokens
  -h --help                Show this screen.

"""

import os
import re
from getpass import getpass
from pathlib import Path
from subprocess import check_output

from docopt import docopt

from . import __version__
from .managers.github import GithubManager
from .parser import parser


def github_from_git():
    s = check_output(["git", "remote", "-v"])
    return re.findall(r"[\w\-]+\/[\w\-]+", s.decode("utf8"))[0]


def main():
    args = docopt(__doc__, version=__version__)

    tracker = args["--tracker"] or "github"
    path = args["<markdown_file>"]

    repo = args["--repo"] if args["--repo"] != "inferred from git remote" else github_from_git()

    if tracker == "github":
        token = args.get("--token") or os.environ.get("GITHUB_TOKEN")
        username = args.get("--username", repo.split("/")[0])
        password = args.get("--pass", getpass("Github password: ") if not token else None)
        manager = GithubManager(repo, token or username, password)
    else:
        import yaml

        from .managers.jira import JiraManager

        try:
            config_file = Path("~/.config/.jira/.config.yml").expanduser()
            default_from_jira_cli = yaml.safe_load(config_file.read_text())
        except FileNotFoundError:
            default_from_jira_cli = {}
        token = args.get("--token") or os.environ.get("JIRA_API_TOKEN")
        username = args.get("--username") or os.environ.get("JIRA_API_LOGIN") or default_from_jira_cli.get("login")
        server = args["--server"] or os.environ.get("JIRA_API_SERVER") or default_from_jira_cli["server"]
        project = args["--project"] or os.environ.get("JIRA_API_PROJECT") or default_from_jira_cli["project"]["key"]
        manager = JiraManager(project, server, username, token)

    if args["pull"]:
        issues = manager.fetcher(args["--state"])
        file_path = Path(path)
        file_path.write_text("".join(str(issue) for issue in issues))
    elif args["push"]:
        issues = parser(path)
        manager.sender(issues)


if __name__ == "__main__":
    main()
