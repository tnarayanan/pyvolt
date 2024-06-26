from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Self

if TYPE_CHECKING:
    from pyvolt.components import Component

from pyvolt.errors import NodeConnectionError, NodeError

class Node:
    __next_node_id: int = 0

    def __init__(self):
        self.node_id: int = Node.__next_node_id
        Node.__next_node_id += 1

        self.v: float = 0.0
        self.connected_comps: set[Component] = set()
        self.connected_node_refs: set[NodeRef] = set()

    def __eq__(self, other: Self) -> bool:
        return self.node_id == other.node_id
    
    def __hash__(self) -> int:
        return self.node_id


class NodeRef:
    __next_node_ref_id: int = 0

    def __init__(self, component, name):
        self.node_ref_id: int = NodeRef.__next_node_ref_id
        NodeRef.__next_node_ref_id += 1

        self.name = name

        self.node: Optional[Node] = None
        self.component: Component = component

        self.target_v: Optional[float] = None
        self.target_i: Optional[float] = None

        self.i: float = 0.0

    def get_voltage(self) -> float:
        if self.node is None:
            raise NodeError("Must set node before accessing voltage")
        return self.node.v

    def set_voltage(self, voltage: Optional[float]):
        self.target_v = voltage

    def get_current(self) -> float:
        if self.node is None:
            raise NodeError("Must set node before accessing current")
        return self.i

    def set_current(self, current: Optional[float]):
        self.target_i = current

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

        # add the node refs to the node's set of connected node refs
        self.node.connected_node_refs.add(self)
        node_ref.node.connected_node_refs.add(node_ref)

    def __repr__(self) -> str:
        return f"NodeRef({self.name}{": " if self.name != "" else ""}{self.node.node_id if self.node is not None else "None"})"
    
    def __eq__(self, other: Self) -> bool:
        return self.node_ref_id == other.node_ref_id
    
    def __hash__(self) -> int:
        return self.node_ref_id