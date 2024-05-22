import pyvolt as pv
from pyvolt import components as comp


class Arduino(pv.Component):
    def __init__(self, name: str = "", n_pins: int = 5):
        super().__init__(name)
        self.n_pins = n_pins
        self.pin_voltages = [0 for _ in range(n_pins)]
        self.pin_connections = [self.new_node_ref() for _ in range(n_pins)]

        self.gnd_connection = self.new_node_ref()

    def pin(self, pin):
        return self.pin_connections[pin]

    @property
    def gnd(self):
        return self.gnd_connection

    def pin_on(self, pin):
        self.pin_voltages[pin] = 5

    def pin_off(self, pin):
        self.pin_voltages[pin] = 0


circuit = pv.Circuit()

# define the components of the circuit
(arduino := Arduino(name="arduino", n_pins=1)) in circuit
(resistor := comp.Resistor(name="150ohm", ohm=150)) in circuit
(diode := comp.Diode(name="led", v_f=2, i_f=20e-3)) in circuit

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
