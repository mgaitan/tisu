import os.path
from tisu.parser import parser, get_metadata, clean_metadata


def s(file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sources', file)


def test_multiples_issues():
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


def test_get_metadata():
    meta = get_metadata(open(s('with_metadata.md')).read())
    assert meta == {'assignee': 'mgaitan',
                    'labels': ['x', 'y', 'z'],
                    'milestone': 'sprint1',
                    'state': 'open'}


def test_get_metadata_is_stable():
    meta = get_metadata(open(s('with_metadata.md')).read())
    assert meta == get_metadata(str(meta))


def test_no_metadata_return_no_output():
    meta = get_metadata('No\n\nmetadata')
    assert str(meta) == ''


def test_clean_metadata():
    text = clean_metadata(open(s('with_metadata.md')).read())
    assert text == '# test1\n\n\nbody\n'


def test_clean_metadata_not_a_block():
    text = clean_metadata("""# title

:labels: x,b,z
some content
:milestone:sprint1

more content
""")
    assert text == '# title\n\nsome content\n\nmore content\n'


def test_with_metatada():
    issues = parser(s('with_metadata.md'))
    assert len(issues) == 1
    assert issues[0].title == 'test1'
    assert issues[0].number is None
    assert issues[0].body == '\n\nbody\n'
    assert issues[0].metadata == {'assignee': 'mgaitan',
                                  'labels': ['x', 'y', 'z'],
                                  'milestone': 'sprint1'}
