import cirq


def setup(qubit_alice, qubit_bob):
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubit_alice))
    circuit.append(cirq.CNOT(qubit_alice, qubit_bob))
    return circuit


def encode(qubit_alice, x, z):
    circuit = cirq.Circuit()
    xx= cirq.X**x
    zz= cirq.Z**z
    circuit.append(xx(qubit_alice))
    circuit.append(zz(qubit_alice))
    return circuit


def decode(qubit_alice, qubit_bob):
    circuit = cirq.Circuit()
    circuit.append(cirq.CNOT(qubit_alice, qubit_bob))
    circuit.append(cirq.H(qubit_alice))
    circuit.append(cirq.measure(qubit_alice, key = 'z'))
    circuit.append(cirq.measure(qubit_bob, key = 'x'))

    return circuit


if __name__ == "__main__":
    qubit_alice = cirq.GridQubit(0, 0)
    qubit_bob = cirq.GridQubit(0, 1)
    x, z = 1, 1
    setup_circuit = setup(qubit_alice, qubit_bob)
    encode_circuit = encode(qubit_alice, x, z)
    decode_circuit = decode(qubit_alice, qubit_bob)
    complete_circuit = cirq.Circuit()
    complete_circuit.append(setup_circuit.all_operations())
    complete_circuit.append(encode_circuit.all_operations())
    complete_circuit.append(decode_circuit.all_operations())
    res = cirq.Simulator().run(complete_circuit, repetitions=20)
    print_circuit = lambda circuit: "  " + (
        str(circuit).replace("\n", "\n  ")
        if len(circuit) > 0
        else "<<This circuit contains no gates.>>"
    )
    print(
        "We are testing your circuit on the input bits x = {} and z = {}.".format(
            x, z
        )
    )
    print("The Bell state is constructed using this circuit:")
    print()
    print(print_circuit(setup_circuit))
    print()
    print("Alice encodes x and z into the state using this circuit:")
    print()
    print(print_circuit(encode_circuit))
    print()
    print("The decoding circuit you implemented is:")
    print()
    print(print_circuit(decode_circuit))
    print()
    print("So, the total circuit becomes:")
    print()
    print(print_circuit(complete_circuit))
    print()
    print(
        "If you implemented the decoding step correctly, we should obtain the following measurement outcomes:"
    )
    print()
    print("  x={}".format(str(x) * 20))
    print("  z={}".format(str(z) * 20))
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
