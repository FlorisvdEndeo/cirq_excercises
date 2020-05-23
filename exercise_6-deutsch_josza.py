import cirq


def deutsch_josza_circuit(oracle, qubits):
    circuit = cirq.Circuit()
    n = len(qubits)
    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(oracle.all_operations())
    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(
        cirq.measure(*qubits, key = 's')
    )
    # +------------------------+
    # |Type your solution below|
    # +------------------------+

    # +------------------------+
    # |Type your solution above|
    # +------------------------+

    return circuit


def deutsch_josza_postprocess(outcome):
    if '1' in outcome:
        result = 'balanced'
    else: result = 'constant'
    # +------------------------+
    # |Type your solution below|
    # +------------------------+

    # +------------------------+
    # |Type your solution above|
    # +------------------------+

    return result


if __name__ == "__main__":
    qubits = [cirq.GridQubit(0, i) for i in range(3)]
    oracle = cirq.Circuit().from_ops(
        [
            cirq.CZ(qubits[0], qubits[1]),
            cirq.CZ(qubits[0], qubits[2]),
            cirq.CZ(qubits[1], qubits[2]),
        ]
    )
    circuit = deutsch_josza_circuit(oracle, qubits)
    res = cirq.Simulator().run(circuit, repetitions=20).measurements
    postprocessed = (
        []
        if "s" not in res
        else list(
            map(
                lambda x: (x, deutsch_josza_postprocess(x)),
                map(
                    lambda x: "".join(map(lambda y: str(int(y)), x)), res["s"]
                ),
            )
        )
    )
    print_circuit = lambda circuit: "  " + (
        str(circuit).replace("\n", "\n  ")
        if len(circuit) > 0
        else "<<This circuit contains no gates.>>"
    )
    print(
        "We are testing your circuit with the function f(x1,x2,x3) = (x1*x2 + x1*x3 + x2*x3) % 2."
    )
    print("The corresponding oracle is:")
    print()
    print(print_circuit(oracle))
    print()
    print("The circuit you implemented is:")
    print()
    print(print_circuit(circuit))
    print()
    print("The measurement outcomes and their postprocessed result are:")
    print()
    print(
        "  "
        + (
            "\n  ".join("'{}' => '{}'".format(*x) for x in postprocessed)
            if postprocessed
            else "<<There were no measurement operations with key 's'.>>"
        )
    )
    print()
    print(
        "If you implemented Deutsch-Josza's algorithm correctly, you should obtain that all measurement outcomes above yield 'balanced' after postprocessing."
    )
