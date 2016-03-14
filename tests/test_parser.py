import os.path
from tissue.parser import parser


def s(file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sources', file)


def test_issue_parser():
    issues = parser(s('issues.md'))
    assert len(issues) == 3
    assert issues[0].title == 'Fix the parser'
    assert issues[0].body == '\nThis would be the content of and issue\n\n## subseccion 1.1\n\nthis is a subsection, part of the issue body\n'
    assert issues[1].title == 'Improve tests'
    assert issues[1].body == '\nAnother issue'
    assert issues[2].title == 'Be happy'
    assert issues[2].body == "\nThe life's milestone.\n"


def test_with_number():
    issues = parser(s('issue_with_number.md'))
    assert len(issues) == 1
    assert issues[0].title == 'Fix the parser'
    assert issues[0].number == 18

