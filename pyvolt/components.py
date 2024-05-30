from pyvolt.node import NodeRef


class Component:
    def __init__(self, name: str = ""):
        self.name: str = name
        self.node_refs: list[NodeRef] = []

    def new_node_ref(self, name: str = "") -> NodeRef:
        self.node_refs.append(NodeRef(self, name=name))
        return self.node_refs[-1]

    def __repr__(self):
        return f"{self.name}: {type(self).__name__}"


class Ground(Component):
    def __init__(self, name: str = ""):
        super().__init__(name)
        self.gnd: NodeRef = self.new_node_ref("gnd")


class VoltageSource(Component):
    def __init__(self, name: str = "", v: float = 5):
        super().__init__(name)
        self.v: float = v

        self.vplus: NodeRef = self.new_node_ref("vplus")
        self.vminus: NodeRef = self.new_node_ref("vminus")


class Resistor(Component):
    def __init__(self, name: str = "", ohm: float = 100):
        super().__init__(name)
        self.ohm: float = ohm

        self.n1: NodeRef = self.new_node_ref("n1")
        self.n2: NodeRef = self.new_node_ref("n2")


class Diode(Component):
    def __init__(self, name: str = "", v_f: float = 2):
        super().__init__(name)
        self.v_f: float = v_f

        self.anode: NodeRef = self.new_node_ref("anode")
        self.cathode: NodeRef = self.new_node_ref("cathode")


class Switch(Component):
    def __init__(self, name: str = "", closed: bool = True):
        super().__init__(name)
        self.closed: bool = closed

        self.n1: NodeRef = self.new_node_ref("n1")
        self.n2: NodeRef = self.new_node_ref("n2")
