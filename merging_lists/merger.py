from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Node:
    val: int = None
    next: Node = None

    @property
    def last(self) -> bool:
        return self.next is None

    def __lt__(self, other: Node) -> bool:
        return self.val < other.val


def merge(lists: List[Node]) -> Node:
    """
    Merges linked lists.
    """
    while len(lists) > 1:
        lists = [Merger(lists[i], lists[i + 1]).merge() for i in range(0, len(lists) - 1, 2)]
    return lists[0]


class Merger:

    def __init__(self, node_1: Node, node_2: Node):
        self.nodes = [node_1, node_2]
        self.start = Node()
        self.point = self.start

    def merge(self) -> Node:
        """
        Merges two linked lists.
        """
        while not self._reached_end:
            self._move_point()
            self._choose_node(self._min)
        self._connect_rest(self._min)
        return self.start.next

    @property
    def _min(self) -> int:
        """
        Returns list with lesser minimum element.
        """
        return 0 if self.nodes[0] < self.nodes[1] else 1

    @property
    def _reached_end(self) -> bool:
        """
        True is one of the nodes is last in its list.
        """
        return any(node.last for node in self.nodes)

    def _move_forward(self, node_index) -> None:
        """
        Switches node to next one.
        """
        self.nodes[node_index] = self.nodes[node_index].next

    def _move_point(self):
        """
        Creates new element in merged list.
        """
        self.point.next = Node()
        self.point = self.point.next

    def _choose_node(self, node_index):
        """
        Copies value from node to current list.
        """
        self.point.val = self.nodes[node_index].val
        self._move_forward(node_index)

    def _connect_rest(self, starting_node_index):
        """
        Links nodes to the end of merged list starting from given node.
        """
        self.point.next = self.nodes.pop(starting_node_index)
        self._scroll_point()
        self.point.next = self.nodes.pop()

    def _scroll_point(self):
        """
        Moves current node to the end of the list.
        """
        while self.point.next is not None:
            self.point = self.point.next
