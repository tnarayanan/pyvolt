import pyvolt as pv
from pyvolt import components as comp

circuit = pv.Circuit()
# define the components of the circuit
(voltage_source := comp.VoltageSource(name="Vcc", v=5)) in circuit
(r1 := comp.Resistor(name="r1", ohm=200)) in circuit
(r2 := comp.Resistor(name="r2", ohm=300)) in circuit
# define the connections between components
voltage_source.vplus >> r1.n1
r1.n2 >> r2.n1
r2.n2 >> voltage_source.vminus
# set the circuit reference voltage
circuit.gnd >> voltage_source.vminus
# compile the circuit
circuit.compile()
