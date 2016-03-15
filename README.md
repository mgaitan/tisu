# Tisú

Your project's issue tracker, in a text file

Note: this is a work in progress. Pull request and feedback are welcome


## Install

$ [sudo] pip3 install -U https://github.com/mgaitan/tisu/archive/master.zip

## Usage

```
(tissue)tin@morochita:~$ tisu --help
Tisú: your issue tracker, in a text file

Usage:
  tisu push <markdown_file> <repo> [--user=<user>] [--pass=<pass>]
  tisu pull <markdown_file> <repo> [--state=<state>]

Options:
  -h --help         Show this screen.
  --version         Show version.
  --state=<state>   Filter by issue state [default: open].
  --user=<user>     Github username to send issues. Repo's username if no given.
  --pass=<pass>     Github password. Prompt if no given.
```
