import pyvolt as pv
from pyvolt import components as comp

circuit = pv.Circuit()
# define the components of the circuit
circuit.add(voltage_source := comp.VoltageSource(name="Vdd", v=5))
circuit.add(pmos := comp.Transistor(name="pMOS", v_th=-0.5))
circuit.add(nmos := comp.Transistor(name="nMOS", v_th=0.5))

voltage_source.vplus >> pmos.source
pmos.drain >> nmos.drain
nmos.source >> voltage_source.vminus

# gate control
input = "low"

(voltage_source.vplus if input == "high" else voltage_source.vminus) >> pmos.gate

pmos.gate >> nmos.gate

circuit.gnd >> voltage_source.vminus

circuit.compile(print_output=True)

print(f"input = {input}, output = {"low" if circuit.inspect_voltage(pmos.drain) < 1 else "high"}")