# Tisú


Tisú [*tiˈsu*, **tissue** in spanish] allows to manage your (github) project's issue tracker, using a single text file

Note: this is a work in progress. Pull requests and feedback are welcome.

## Install

```
$ pip3 install --user -U tisu
```

## Usage

Tisú can import and export your issues using a simple markdown file, where each section
is a different issue.

```
# issue title

issue body

```

If an issue already exists in your tracker, the number is a prefix in the title, wrapped
by square brackets:

```
# [#1] issue title
```

In this case, Tisú will update that issue instead to create a new one.

This is the current command line help:

```
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
```


To access private repositories you need a [personal access token](https://github.com/settings/tokens).


### Example

Suppose you want to push a couple of issues like in
[this TODO.md](https://github.com/mgaitan/tisu/blob/caf8cdd34d7dea04e7e36a23a4e08748364f09c5/TODO.md)
file.

```
$ tisu push TODO.md mgaitan/tisu
Github password:
Created #11: support metadata
Created #12: setup travis CI
```

Result in:

![](https://cloud.githubusercontent.com/assets/2355719/13778398/451fa440-ea94-11e5-985d-84d8770cf531.png)

Then, I can pull and overwrite the file.

```
$ tisu pull TODO.md
```

[This is the result](https://github.com/mgaitan/tisu/blob/07c478a15f0dd12b5f5ba1a7636f9703e9f201fc/TODO.md).
As in this case I didn't change anything online, the content is (almost) the same, but note that
each title has its ID number.

## Working with metadata

Tisú can also synchronize the issue's metadata with ease.

The format is `:<meta_var>: <value/s>`, where `<meta_var>` is one `assignee`, `labels`
or `milestone`. These metadata lines can be in any position under the title (and not
neccesarily all, in this order nor all together) and if present,
they are removed from the issue's description sent.

For example, create a new issue with some metadata

```
# Make a video

:assignee: mgaitan
:labels: docs, idea
:milestone: sprint 1

Make an screencast showing how to use Tisú.

```

If later you want to close this issue, you can add mark it with `:state: closed` and push.

```
# [#13] Make a video

:assignee: mgaitan
:labels: docs, idea
:milestone: sprint 1

Make an screencast showing how to use Tisú.

:state: closed
```
