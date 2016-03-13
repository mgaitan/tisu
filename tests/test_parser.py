import os.path
from tissue.parser import issue_parser


def s(file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sources', file)


def test_issue_parser():
    issues = issue_parser(s('issues.rst'))
    assert issues == [('Fix the parser', '\nThis would be the content of and issue\n\nsubseccion 1.1\n++++++++++++++\n\nthis is a subsection, part of the issue body\n\n'),   # noqa
                      ('Improve tests', '\nAnother issue\n'),
                      ('Be happy', "\nThe life's milestone.\n")]
