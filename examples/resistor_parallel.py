import pyvolt as pv
from pyvolt import components as comp

circuit = pv.Circuit()
# define the components of the circuit
(voltage_source := comp.VoltageSource(name="Voltage Source", v=5)) in circuit
(r1 := comp.Resistor(name="resistor 1", ohm=400)) in circuit
(r2 := comp.Resistor(name="resistor 2", ohm=400)) in circuit
(r3 := comp.Resistor(name="resistor 3", ohm=300)) in circuit
# define the connections between components
voltage_source.vplus >> r1.n1
voltage_source.vplus >> r2.n1
r1.n2 >> r3.n1
r2.n2 >> r3.n1
r3.n2 >> voltage_source.vminus
# set the circuit reference voltage
circuit.gnd >> voltage_source.vminus
# compile the circuit
circuit.compile()
