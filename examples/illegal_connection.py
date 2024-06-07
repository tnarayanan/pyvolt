import pyvolt as pv
from pyvolt import components as comp

circuit = pv.Circuit()
# define the components of the circuit
circuit.add(voltage_source := comp.VoltageSource(name="Voltage Source", v=5))
circuit.add(resistor := comp.Resistor(name="150ohm resistor", ohm=150))
circuit.add(diode := comp.Diode(name="LED", v_f=2))
# define the connections between components
voltage_source.vplus >> resistor.n1
resistor.n2 >> diode.anode

# error: these two cannot connect, as they are different nodes
resistor.n1 >> resistor.n2
