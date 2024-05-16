from pyvolt.node import NodeRef
from pyvolt.components import Component, Ground


class Circuit:
    def __init__(self):
        self.gnd_comp = Ground(name="Ground")
        self.components: list[Component] = [self.gnd_comp]

    @property
    def gnd(self):
        return self.gnd_comp.gnd

    def compile(self):
        visited_nodes = set()
        visited_nodes.add(self.gnd.node)

        stack = [self.gnd.node]

        while len(stack) > 0:
            # print(stack)
            cur_node = stack.pop()

            print(f"Node {cur_node.node_id}")
            for component in cur_node.connected_comps:
                print(f"\t{component}")
                # print(f"\t\t{component.node_refs}")
                for node_ref in component.node_refs:
                    if node_ref.node not in visited_nodes:
                        # print(f"adding node {node_ref.node.node_id}")
                        visited_nodes.add(node_ref.node)
                        stack.append(node_ref.node)
                    # else:
                        # print(f"node {node_ref.node.node_id} already in vis")

    def inspect_voltage(self, node_ref: NodeRef) -> float:
        return 0.0

    def __contains__(self, component: Component) -> Component:
        self.components.append(component)
        return component
