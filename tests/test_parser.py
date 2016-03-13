from tissue.parser import issue_parser


content = """

Fix the parser
--------------

This would be the content of and issue

subseccion 1.1
++++++++++++++

this is a subsection, part of the issue body


Improve tests
---------------

Another issue

Be happy
---------

The life milestone.
"""


def test_issue_parser():
    issues = issue_parser(content)
    assert issues == [('Fix the parser', '\nThis would be the content of and issue\n\nsubseccion 1.1\n++++++++++++++\n\nthis is a subsection, part of the issue body\n\n'),   # noqa
                      ('Improve tests', '\nAnother issue\n'),
                      ('Be happy', '\nThe life milestone.\n')]
