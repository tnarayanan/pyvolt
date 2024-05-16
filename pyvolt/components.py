from pyvolt.node import NodeRef


class Component:
    def __init__(self):
        self.node_refs: list[NodeRef] = []

    def new_node_ref(self) -> NodeRef:
        self.node_refs.append(NodeRef(self))
        return self.node_refs[-1]


class Ground(Component):
    def __init__(self):
        super().__init__()
        self.node: NodeRef = self.new_node_ref()


class VoltageSource(Component):
    def __init__(self, v: float = 5):
        super().__init__()
        self.v: float = v

        self.vplus: NodeRef = self.new_node_ref()
        self.vminus: NodeRef = self.new_node_ref()


class Resistor(Component):
    def __init__(self, ohm: float = 100):
        super().__init__()
        self.ohm: float = ohm

        self.n1: NodeRef = self.new_node_ref()
        self.n2: NodeRef = self.new_node_ref()


class Diode(Component):
    def __init__(self, v_f: float = 2, i_f: float = 1e-2):
        super().__init__()
        self.v_f: float = v_f
        self.i_f: float = i_f

        self.anode: NodeRef = self.new_node_ref()
        self.cathode: NodeRef = self.new_node_ref()
