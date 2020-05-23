import cirq


def grover_1_of_4(oracle, qubit1, qubit2):
    c = cirq.Circuit()
    c.append(cirq.H(qubit1))
    c.append(cirq.H(qubit2))
    c.append(oracle.all_operations())
    input_qubits = [qubit1, qubit2]
    c.append(cirq.H.on_each(*input_qubits))
    c.append(cirq.X.on_each(*input_qubits))
    c.append(cirq.H.on(input_qubits[1]))
    c.append(cirq.CNOT(input_qubits[0], input_qubits[1]))
    c.append(cirq.H.on(input_qubits[1]))
    c.append(cirq.X.on_each(*input_qubits))
    c.append(cirq.H.on_each(*input_qubits))
    c.append(cirq.measure(*input_qubits, key = 'a'))
    return c


if __name__ == "__main__":
    qubit1 = cirq.GridQubit(0, 0)
    qubit2 = cirq.GridQubit(0, 1)
    s = 0b11
    oracle = cirq.Circuit()
    if s == 0b00:
        oracle.append(
            [cirq.Z(qubit1), cirq.Z(qubit2), cirq.CZ(qubit1, qubit2)]
        )
    elif s == 0b01:
        oracle.append([cirq.Z(qubit2), cirq.CZ(qubit1, qubit2)])
    elif s == 0b10:
        oracle.append([cirq.Z(qubit1), cirq.CZ(qubit1, qubit2)])
    elif s == 0b11:
        oracle.append([cirq.CZ(qubit1, qubit2)])
    circuit = grover_1_of_4(oracle, qubit1, qubit2)
    res = cirq.Simulator().run(circuit, repetitions=20)
    print_circuit = lambda circuit: "  " + (
        str(circuit).replace("\n", "\n  ")
        if len(circuit) > 0
        else "<<This circuit contains no gates.>>"
    )
    print("We are testing your circuit on the input s = {:02b}.".format(s))
    print("The corresponding oracle is:")
    print()
    print(print_circuit(oracle))
    print()
    print("The full circuit is:")
    print()
    print(print_circuit(circuit))
    print()
    print(
        "If you implemented Grover's algorithm correctly, we should obtain the following measurement outcomes:"
    )
    print()
    print("  a={}".format(", ".join(x * 20 for x in "{:02b}".format(s))))
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
