import pytest
from merger import merge, Node


def to_linked_list(normal_list):
    start = Node(normal_list[0])
    point = start
    for item in normal_list[1:]:
        node = Node(item)
        point.next = node
        point = point.next
    return start


@pytest.mark.parametrize('lists,merged', [(([1, 4, 5], [1, 3, 4]), [1, 1, 3, 4, 4, 5]),
                                          (([1, 4, 5], [1, 3, 4], [2, 6], [9]), [1, 1, 2, 3, 4, 4, 5, 6, 9])])
def test_merges_lists(lists, merged):
    linked_lists = [to_linked_list(_list) for _list in lists]
    assert merge(linked_lists) == to_linked_list(merged)
