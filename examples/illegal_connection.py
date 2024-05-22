import pyvolt as pv
from pyvolt import components as comp

circuit = pv.Circuit()
# define the components of the circuit
(voltage_source := comp.VoltageSource(name="Voltage Source", v=5)) in circuit
(resistor := comp.Resistor(name="150ohm resistor", ohm=150)) in circuit
(diode := comp.Diode(name="LED", v_f=2, i_f=20e-3)) in circuit
# define the connections between components
voltage_source.vplus >> resistor.n1
resistor.n2 >> diode.anode

# error: these two cannot connect, as they are different nodes
resistor.n1 >> resistor.n2
