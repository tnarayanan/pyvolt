# pyvolt: a circuit specification library

Pyvolt makes circuit specification and simulation easy.

## Installation and import

Install pyvolt using `pip install pyvolt`.

Import pyvolt using `import pyvolt as pv` and `import pyvolt.components as comp`.

## Tutorial

### Create a circuit

```python
circuit = pv.Circuit()
```

### Create components

Create a `VoltageSource`, `Resistor`, `Diode`, `Switch`, or `Transistor` and attach it to the circuit:

```python
(voltage_source := comp.VoltageSource(name="V", v=5)) in circuit
(resistor := comp.Resistor(name="r1", ohm=150)) in circuit
(diode := comp.Diode(name="LED", v_f=2)) in circuit
```

### Connect components

Pyvolt uses the `>>` operator to connect components instead of defining nodes explicitly:

```python
voltage_source.vplus >> resistor.n1
resistor.n2 >> diode.anode
diode.cathode >> voltage_source.vminus
```

### Connect the circuit ground

The circuit's ground is set by connecting it to any other component terminal. The node connected to the circuit ground is defined as having a voltage of zero.

```python
circuit.gnd >> voltage_source.vminus
```

### Compile the circuit

```python
circuit.compile()
```

### Interpreting the compilation output

Here is the output of `circuit.compile()` on the circuit defined in this tutorial:

```
Compiled circuit
----------------
Node 0: v=5.0
    V.vplus: i=0.02
    r1.n1: i=-0.02
Node 1: v=2.0
    LED.anode: i=-0.02
    r1.n2: i=0.02
Node 2: v=0.0
    V.vminus: i=-0.02
    LED.cathode: i=0.02
    Ground.gnd: i=0.0
----------------
```

We interpret this output as follows:

* The node with `V.vplus` and `r1.n1` has voltage 5V, with 20 milliamps of current flowing from `V.vplus` into `r1.n1`
* The node with `LED.anode` and `r1.n2` has voltage 2V, with 20 milliamps of current flowing from `r1.n2` to `LED.anode`
* The node with `V.vminus`, `LED.cathode`, and `Ground.gnd` has voltage 0V, with 20 milliamps of current flowing from `LED.cathode` to `V.vminus`

Pyvolt's convention is positive currents flowing out of components and negative currents flowing into components.

### Inspecting voltages and currents

After a circuit has been compiled, we can use the `inspect_voltage` and `inspect_current` methods:

```python
print("V before diode:", circuit.inspect_voltage(diode.anode))  # V before diode: 2.0
print("I before resistor:", circuit.inspect_current(resistor.n1))  # I before resistor: -0.02
```

### Custom components

We can define custom components by calling the `new_node_ref(name)` method inside of `Component` classes for each connection the component has. We can set the target voltage or current of a node or branch by calling `set_voltage` or `set_current` on the node reference, respectively.

```python
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
```





