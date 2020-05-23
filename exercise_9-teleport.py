import cirq


def setup(qubit_epr_alice, qubit_epr_bob):
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubit_epr_alice))
    circuit.append(cirq.CNOT(qubit_epr_alice, qubit_epr_bob))
    return circuit


def teleport_alice(qubit_orig_state, qubit_epr_alice):
    circuit = cirq.Circuit()
    for a in range(1):
        xx= cirq.X**a
        zz= cirq.Z**a
        circuit.append(xx(qubit_orig_state))
        circuit.append(zz(qubit_epr_alice))
        circuit.append(cirq.CNOT(qubit_orig_state, qubit_epr_alice))
        circuit.append(cirq.H(qubit_orig_state))
        circuit.append(cirq.measure(qubit_orig_state, key = 'z'))
        circuit.append(cirq.measure(qubit_epr_alice, key = 'x'))

    return circuit


def teleport_bob(qubit_epr_bob, measurement_outcomes):
    circuit = cirq.Circuit()
    xa = cirq.X**measurement_outcomes['x']
    za = cirq.Z**measurement_outcomes['z']
    circuit.append(za(qubit_epr_bob))
    circuit.append(xa(qubit_epr_bob))

    #notcorrectyetbutcan'tbearsed
    return circuit


if __name__ == "__main__":
    import numpy as np
    import itertools as it
    import sys

    qubit_orig_state = cirq.GridQubit(0, 0)
    qubit_epr_alice = cirq.GridQubit(0, 1)
    qubit_epr_bob = cirq.GridQubit(0, 2)

    setup_circuit = setup(qubit_epr_alice, qubit_epr_bob)
    teleport_alice_circuit = teleport_alice(qubit_orig_state, qubit_epr_alice)

    teleport_circuit = cirq.Circuit()
    teleport_circuit.append(setup_circuit.all_operations())
    teleport_circuit.append(teleport_alice_circuit.all_operations())

    first_qubits = [qubit_orig_state, qubit_epr_alice, qubit_epr_bob]
    qubit_list = first_qubits + list(
        teleport_circuit.all_qubits().difference(set(first_qubits))
    )

    initial_state = np.array([0.5, 0.5 * np.sqrt(3)], dtype=np.complex64)
    result = cirq.Simulator().simulate(
        teleport_circuit,
        initial_state=np.kron(
            initial_state,
            np.array(
                [1] + [0] * (2 ** (len(qubit_list) - 1) - 1),
                dtype=np.complex64,
            ),
        ),
        qubit_order=qubit_list,
    )

    measurement_results = {
        k: int("".join("1" if c else "0" for c in v), 2)
        for k, v in result.measurements.items()
    }
    teleport_bob_circuit = teleport_bob(qubit_epr_bob, measurement_results)
    additional_qubit_list = list(
        teleport_bob_circuit.all_qubits().difference(set(qubit_list))
    )
    new_qubit_list = qubit_list + additional_qubit_list

    result_state = (
        cirq.Simulator()
        .simulate(
            teleport_bob_circuit,
            initial_state=np.kron(
                result.final_state,
                np.array(
                    [1] + [0] * (2 ** len(additional_qubit_list) - 1),
                    dtype=np.complex64,
                ),
            ),
            qubit_order=new_qubit_list,
        )
        .final_state
    )

    num_aux_qubits = len(new_qubit_list) - 3
    bipartite_matrix = np.empty(
        (2, 2 ** (num_aux_qubits + 2)), dtype=np.complex64
    )
    for j, k in it.product(range(4), range(2 ** num_aux_qubits)):
        bipartite_matrix[0, j * 2 ** num_aux_qubits + k] = result_state[
            j * 2 ** (num_aux_qubits + 1) + k
        ]
        bipartite_matrix[1, j * 2 ** num_aux_qubits + k] = result_state[
            j * 2 ** (num_aux_qubits + 1) + 2 ** num_aux_qubits + k
        ]
    u, s, v = np.linalg.svd(bipartite_matrix)
    entanglement_measure = s[0]
    bob_state = u[:, 0]

    inner_product = np.sum(np.conj(bob_state) * initial_state)
    corrected_result_state = bob_state * np.exp(1.0j * np.angle(inner_product))

    print_circuit = lambda circuit: "  " + (
        str(circuit).replace("\n", "\n  ")
        if len(circuit) > 0
        else "<<This circuit contains no gates.>>"
    )
    print("We will be teleporting the following state:")
    print()
    print("  [{:1.3f}]\n  [{:1.3f}]".format(*initial_state))
    print()
    print("The entangled resource is constructed with the following circuit:")
    print()
    print(print_circuit(setup_circuit))
    print()
    print("Alice performs the following operations to teleport the state:")
    print()
    print(print_circuit(teleport_alice_circuit))
    print()
    print("The following measurement results were obtained:")
    print()
    if measurement_results:
        for k, v in sorted(measurement_results.items()):
            print("  {} = {}".format(k, v))
    else:
        print("  <<This circuit contains no measurements.>>")
    print()
    print("Bob performs the following operations to retrieve the state:")
    print()
    print(print_circuit(teleport_bob_circuit))
    print()
    if abs(entanglement_measure - 1.0) > 1e-4:
        print(
            "Bob's qubit is entangled with other qubits, so the teleportation did not succeed."
        )
        sys.exit()
    print("The resulting state is:")
    print()
    print("  [{:1.3f}]\n  [{:1.3f}]".format(*corrected_result_state))
    print()
    print(
        "The absolute value of the inner product is: {:1.3f}.".format(
            np.abs(inner_product)
        )
    )
    print(
        "That means that the state was {}correctly teleported.".format(
            "not " if abs(np.abs(inner_product) - 1.0) > 1e-4 else ""
        )
    )
