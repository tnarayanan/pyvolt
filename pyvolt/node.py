from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Self

if TYPE_CHECKING:
    from pyvolt.components import Component

from pyvolt.errors import NodeConnectionError

class Node:
    __next_node_id: int = 0

    def __init__(self):
        self.node_id: int = Node.__next_node_id
        Node.__next_node_id += 1

        self.v: float = 0.0
        self.connected_comps: set[Component] = set()

    def __eq__(self, other: Self) -> bool:
        return self.node_id == other.node_id
    
    def __hash__(self) -> int:
        return self.node_id


class NodeRef:
    def __init__(self, component):
        self.node: Optional[Node] = None
        self.component: Component = component

    def __rshift__(self, node_ref: Self):
        if self.node is None and node_ref.node is None:
            # create new shared Node
            self.node = Node()
            node_ref.node = self.node
        elif self.node is None:
            # connect own node ref to other node
            self.node = node_ref.node
        elif node_ref.node is None:
            # connect other node_ref to own node
            node_ref.node = self.node
        elif self.node != node_ref.node:
            # both nodes exist and are different, which is an error
            raise NodeConnectionError("Trying to connect two distinct nodes together")

        # the only other case is when both nodes exist and are the same node,
        # which is a redundant connection

        # add the components to the node's set of connected components
        self.node.connected_comps.add(self.component)
        node_ref.node.connected_comps.add(node_ref.component)

    def __repr__(self) -> str:
        return f"NodeRef({self.node.node_id if self.node is not None else "None"})"