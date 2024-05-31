import pyvolt as pv
from pyvolt import components as comp

circuit = pv.Circuit()
# define the components of the circuit
(voltage_source := comp.VoltageSource(name="Vcc", v=5)) in circuit
(diode1 := comp.Diode(name="diode1", v_f=3)) in circuit
(diode2 := comp.Diode(name="diode2", v_f=3)) in circuit
# (resistor := comp.Resistor(name="r1", ohm=150)) in circuit

voltage_source.vplus >> diode1.anode
diode1.cathode >> diode2.anode
diode2.cathode >> voltage_source.vminus
# diode2.cathode >> resistor.n1
# resistor.n2 >> voltage_source.vminus

circuit.gnd >> voltage_source.vminus

circuit.compile()