import pyvolt as pv
from pyvolt import components as comp


class Arduino(pv.Component):
    def __init__(self, name: str = "", n_pins: int = 5):
        super().__init__(name)
        self.pin_connections: list[pv.NodeRef] = [self.new_node_ref(f"pin{i}") for i in range(n_pins)]
        self.gnd_connection = self.new_node_ref("gnd")

    def pin(self, pin):
        return self.pin_connections[pin]

    @property
    def gnd(self):
        return self.gnd_connection

    def pin_on(self, pin):
        self.pin_connections[pin].set_voltage(5)

    def pin_off(self, pin):
        self.pin_connections[pin].set_voltage(0)


circuit = pv.Circuit()

# define the components of the circuit
circuit.add(arduino := Arduino(name="arduino", n_pins=1))
circuit.add(resistor := comp.Resistor(name="r1", ohm=150))
circuit.add(diode := comp.Diode(name="LED", v_f=2))

# define the connections between components
arduino.pin(0) >> resistor.n1
resistor.n2 >> diode.anode
diode.cathode >> arduino.gnd

# set the circuit reference voltage
circuit.gnd >> arduino.gnd

# CASE 1: pin 0 is on
arduino.pin_on(0)
circuit.compile()
print("V before diode:", circuit.inspect_voltage(diode.anode))
print("V after diode:", circuit.inspect_voltage(diode.cathode))

# CASE 2: pin 0 is off
arduino.pin_off(0)
circuit.compile()
print("V before diode:", circuit.inspect_voltage(diode.anode))
print("V after diode:", circuit.inspect_voltage(diode.cathode))
