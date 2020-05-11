from merger import merge

import pytest


@pytest.mark.parametrize('lists,merged', (([1, 4, 5], [1, 3, 4], [2, 6]), [1, 1, 2, 3, 4, 4, 5, 6]))
def test_merges_lists(lists, merged):
    assert merge(lists) == merged
