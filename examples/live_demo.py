import pyvolt as pv
from pyvolt import components as comp

circuit = pv.Circuit()

(voltage_source := comp.VoltageSource(name="V_in", v=5)) in circuit
(resistor := comp.Resistor(name="R", ohm=150)) in circuit
(diode := comp.Diode(name="LED", v_f=2, i_f=20e-3)) in circuit

voltage_source.vplus >> resistor.n1
resistor.n2 >> diode.anode
diode.cathode >> voltage_source.vminus

circuit.gnd >> voltage_source.vminus

circuit.compile()

print(f"V before diode: {circuit.inspect_voltage(diode.anode)}")
print(f"V after diode: {circuit.inspect_voltage(diode.cathode)}")
