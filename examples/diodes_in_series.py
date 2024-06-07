import pyvolt as pv
from pyvolt import components as comp

circuit = pv.Circuit()
# define the components of the circuit
circuit.add(voltage_source := comp.VoltageSource(name="Vcc", v=5))
circuit.add(diode1 := comp.Diode(name="diode1", v_f=3))
circuit.add(diode2 := comp.Diode(name="diode2", v_f=3))

voltage_source.vplus >> diode1.anode
diode1.cathode >> diode2.anode
diode2.cathode >> voltage_source.vminus

circuit.gnd >> voltage_source.vminus

circuit.compile()