import pyvolt as pv
from pyvolt import components as comp

circuit = pv.Circuit()

(voltage_source := comp.VoltageSource(name="Vcc", v=5)) in circuit
(resistor := comp.Resistor(name="r1", ohm=150)) in circuit
(diode := comp.Diode(name="LED", v_f=2)) in circuit

voltage_source.vplus >> resistor.n1
resistor.n2 >> diode.anode
diode.cathode >> voltage_source.vminus

circuit.gnd >> voltage_source.vminus

circuit.compile()

print(f"V before diode: {circuit.inspect_voltage(diode.anode)}")
print(f"V after diode: {circuit.inspect_voltage(diode.cathode)}")
