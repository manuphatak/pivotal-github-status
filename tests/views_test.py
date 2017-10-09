from app.views import get_story_ids
import pytest


@pytest.mark.parametrize('test_input, expected', [
    ('Test Story [Fixes #151356728]', ('151356728', )),
    ('Test Story [#151356728]', ('151356728', )),
    ('Test Story', tuple()),
    ('Test Story []', tuple()),
    ('Test Story [#,]', tuple()),
    ('Test Story [#151356728,#151356729,]', ('151356728', '151356729')),
    ('Test Story [Fixes #151356728, Delivers #151356729]', ('151356728',
                                                            '151356729')),
    ('Test Story [Fixes #151356728, #151356729]', ('151356728', '151356729')),
])
def test_it_gets_story_ids_from_title(test_input, expected):
    assert tuple(get_story_ids(test_input)) == expected
