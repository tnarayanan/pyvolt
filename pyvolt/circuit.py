from typing import Any
from pyvolt.node import Node, NodeRef
from pyvolt.components import Component, Diode, Ground, Resistor, Switch, VoltageSource

from ortools.linear_solver import pywraplp


class Circuit:
    def __init__(self):
        self.gnd_comp = Ground(name="Ground")
        self.components: list[Component] = [self.gnd_comp]

    @property
    def gnd(self):
        return self.gnd_comp.gnd

    def compile(self):
        solver: pywraplp.Solver = pywraplp.Solver.CreateSolver("SCIP")
        # solver: pywraplp.Solver = pywraplp.Solver.CreateSolver("GLOP")
        if not solver:
            raise RuntimeError("Could not instantiate solver")
        
        v_vars: dict[Node, Any] = {}
        i_vars: dict[NodeRef, Any] = {}
        diode_on_vars: list = []
        tmp_cnt = 0

        for component in self.components:
            for node_ref in component.node_refs:
                if node_ref.node not in v_vars:
                    v_vars[node_ref.node] = solver.NumVar(-solver.infinity(), solver.infinity(), f"Node_{node_ref.node.node_id}")
                if node_ref not in i_vars:
                    i_vars[node_ref] = solver.NumVar(-solver.infinity(), solver.infinity(), f"NodeRef_{node_ref.node_ref_id}")

            # CONVENTION: currents always flow into nodes, away from components

            match component:
                case VoltageSource(v=v):
                    # voltage difference must be equal to v
                    solver.Add(v_vars[component.vplus.node] - v_vars[component.vminus.node] == v)
                    # current must be equal
                    solver.Add(i_vars[component.vplus] == -i_vars[component.vminus])
                    solver.Add(i_vars[component.vplus] >= 0)
                case Resistor(ohm=ohm):
                    # voltage difference must be equal to current/resistance
                    solver.Add(v_vars[component.n1.node] - v_vars[component.n2.node] == i_vars[component.n2] * ohm)
                    # current must be equal
                    solver.Add(i_vars[component.n1] == -i_vars[component.n2])
                case Diode(v_f=v_f):
                    is_diode_on = solver.IntVar(0, 1, f"tmp{tmp_cnt}")
                    tmp_cnt += 1
                    diode_on_vars.append(is_diode_on)
                    # simple model: voltage difference must be equal to v_f if the diode is on
                    # solver.Add(v_vars[component.anode.node] - v_vars[component.cathode.node] == v_f)
                    solver.Add(v_vars[component.anode.node] - v_vars[component.cathode.node] >= v_f - 10000 * (1 - is_diode_on))
                    solver.Add(v_vars[component.anode.node] - v_vars[component.cathode.node] <= v_f + 10000 * (1 - is_diode_on))
                    # current on anode and cathode must be equal
                    solver.Add(i_vars[component.anode] == -i_vars[component.cathode])
                    # current is greater than zero if the diode is on, but zero if the diode is off
                    solver.Add(i_vars[component.cathode] >= -10000 * (1 - is_diode_on))
                    solver.Add(i_vars[component.cathode] <= 10000 * is_diode_on)

                case Switch(closed=closed):
                    solver.Add(i_vars[component.n1] == -i_vars[component.n2])
                    if closed:
                        solver.Add(v_vars[component.n1.node] == v_vars[component.n2.node])
                    else:
                        solver.Add(i_vars[component.n1] == 0)
                case _:
                    for node_ref in component.node_refs:
                        if node_ref.target_v is not None:
                            solver.Add(v_vars[node_ref.node] == node_ref.target_v)
                        if node_ref.target_i is not None:
                            solver.Add(i_vars[node_ref] == node_ref.target_i)
        
        solver.Add(v_vars[self.gnd.node] == 0)

        for node in v_vars:
            node_ref_i_vars = [i_vars[node_ref] for node_ref in node.connected_node_refs]
            solver.Add(sum(node_ref_i_vars) == 0)
        
        objective = solver.Objective()
        for diode_var in diode_on_vars:
            objective.SetCoefficient(diode_var, 1)
        objective.SetMaximization()

        # solver.Maximize(0)
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            # print("Solution:")
            # print(f"Objective value = {solver.Objective().Value():0.1f}")
            for node in v_vars:
                node.v = round(v_vars[node].solution_value(), 6)
            for node_ref in i_vars:
                node_ref.i = round(i_vars[node_ref].solution_value(), 8)
        else:
            print("The problem does not have an optimal solution.")
                    


        visited_nodes = set()
        visited_nodes.add(self.gnd.node)

        stack = [self.gnd.node]

        while len(stack) > 0:
            cur_node = stack.pop()

            print(f"Node {cur_node.node_id}: v={cur_node.v}, i={[nr.i for nr in cur_node.connected_node_refs]}")
            for component in cur_node.connected_comps:
                print(f"\t{component}")
                for node_ref in component.node_refs:
                    if node_ref.node not in visited_nodes:
                        visited_nodes.add(node_ref.node)
                        stack.append(node_ref.node)

    def inspect_voltage(self, node_ref: NodeRef) -> float:
        return node_ref.get_voltage()
    
    def inspect_current(self, node_ref: NodeRef) -> float:
        return node_ref.get_current()

    def __contains__(self, component: Component) -> Component:
        self.components.append(component)
        return component
