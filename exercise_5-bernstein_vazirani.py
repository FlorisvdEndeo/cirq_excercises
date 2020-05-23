import cirq


def bernstein_vazirani(oracle, qubits):
    circuit = cirq.Circuit()
    n = len(qubits)
    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(oracle.all_operations())
    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(cirq.measure(*qubits, key = 's'))
    return circuit


if __name__ == "__main__":
    s = "0110"  # We will be testing the circuit for this value of s
    qubits = [cirq.GridQubit(0, i) for i in range(len(s))]
    oracle = cirq.Circuit().from_ops(
        [cirq.Z(qubits[i]) for i, c in enumerate(s) if c == "1"]
    )
    circuit = bernstein_vazirani(oracle, qubits)
    res = cirq.Simulator().run(circuit, repetitions=20)
    print_circuit = lambda circuit: "  " + (
        str(circuit).replace("\n", "\n  ")
        if len(circuit) > 0
        else "<<This circuit contains no gates.>>"
    )
    print("We are testing your circuit on the input s = {}.".format(s))
    print("The corresponding oracle is:")
    print()
    print(print_circuit(oracle))
    print()
    print("The full circuit is:")
    print()
    print(print_circuit(circuit))
    print()
    print(
        "If you implemented Bernstein-Vazirani's algorithm correctly, we should obtain the following measurement outcomes:"
    )
    print()
    print("  s={}".format(", ".join(x * 20 for x in s)))
    print()
    print("The actual outcome is:")
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
