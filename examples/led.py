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
diode.cathode >> voltage_source.vminus
# set the circuit reference voltage
circuit.gnd >> voltage_source.vminus
# compile the circuit
circuit.compile()
# probe the circuit
print("V before diode:", circuit.inspect_voltage(diode.anode))
print("V after diode:", circuit.inspect_voltage(diode.cathode))
