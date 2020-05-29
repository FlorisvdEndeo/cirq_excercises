import cirq
from math import pi


def iterative_reflection(oracle, qubit, angle):
    circuit = cirq.Circuit(
        cirq.H(qubit)
    )

    for _ in range(int(pi/angle/8)):
        circuit.append(oracle.all_operations())
        circuit.append(cirq.Z(qubit))

    circuit.append(cirq.measure(qubit, key='x'))
    return circuit


if __name__ == "__main__":
    qubit = cirq.GridQubit(0, 0)
    oracle = cirq.Circuit()
    oracle.append(cirq.X(qubit))
    oracle.append(cirq.Y(qubit) ** (-7.0 / 8.0))
    circuit = iterative_reflection(oracle, qubit, pi / 32.0)
    res = cirq.Simulator().run(circuit, repetitions=20)
    print_circuit = lambda circuit: "  " + (
        str(circuit).replace("\n", "\n  ")
        if len(circuit) > 0
        else "<<This circuit contains no gates.>>"
    )
    print(
        "We will try your circuit with an oracle that reflects through the axis that is located at theta = +pi/32"
    )
    print("The phase oracle of f is the following circuit:")
    print()
    print(print_circuit(oracle))
    print()
    print("Your circuit is:")
    print()
    print(print_circuit(circuit))
    print()
    print(
        "If you implemented the circuit correctly, you should obtain the following measurement outcome:"
    )
    print()
    print("  x=" + "0" * 20)
    print()
    print("The following measurement results were obtained:")
    print()
    print(
        "  "
        + (
            str(res).replace("\n", "\n  ")
            if len(res.measurements) > 0
            else "<<There were no measurements.>>"
        )
    )
    print()
