import pyvolt as pv
from pyvolt import components as comp

circuit = pv.Circuit()
# define the components of the circuit
circuit.add(voltage_source := comp.VoltageSource(name="Vcc", v=5))
circuit.add(resistor := comp.Resistor(name="r1", ohm=150))
circuit.add(diode := comp.Diode(name="LED", v_f=2))
circuit.add(switch := comp.Switch(name="switch"))
# define the connections between components
voltage_source.vplus >> resistor.n1
resistor.n2 >> diode.anode
diode.cathode >> switch.n1
switch.n2 >> voltage_source.vminus
# set the circuit reference voltage
circuit.gnd >> voltage_source.vminus
# compile the circuit
switch.closed = True
circuit.compile()
# probe the circuit
print("V before diode:", circuit.inspect_voltage(diode.anode))
print("I before diode:", circuit.inspect_current(diode.anode))
print("V after diode:", circuit.inspect_voltage(diode.cathode))
