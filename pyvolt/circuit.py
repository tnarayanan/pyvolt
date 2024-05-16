import pyvolt as pv
import pyvolt.components as comp


class Circuit:
    def __init__(self):
        gnd_comp = comp.Ground()
        self.components: list[pv.Component] = [gnd_comp]
        self.gnd: pv.NodeRef = pv.NodeRef(gnd_comp)

    def compile(self):
        pass

    def inspect_voltage(self, node_ref: pv.NodeRef) -> float:
        return 0.0

    def __contains__(self, component: pv.Component) -> pv.Component:
        self.components.append(component)
        return component
