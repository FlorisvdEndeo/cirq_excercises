import cirq
from math import pi, asin, sqrt

def multiple_controlled_Z(qubits):
    aux = [cirq.GridQubit(0,y) for y in range(len(qubits),2*len(qubits)-2)]
    gates = [cirq.TOFFOLI(*bits) for bits in zip(qubits[2:], aux, aux[1:])]

    return cirq.Circuit(
        cirq.TOFFOLI(*qubits[:2], aux[0]),
        gates,
        cirq.CZ(aux[-1], qubits[-1]),
        reversed(gates),
        cirq.TOFFOLI(*qubits[:2], aux[0]),
    )


def W(qubits):
    circuit = cirq.Circuit(cirq.H(qubits[0]),
    cirq.H(qubits[1]),
    cirq.X(qubits[0]), cirq.X(qubits[1]), cirq.H(qubits[1]), cirq.CNOT(qubits[0], qubits[1]),
    cirq.H(qubits[1]), cirq.X(qubits[0]), cirq.X(qubits[1]), cirq.H(qubits[0]), cirq.H(qubits[1]))
    circuit.append(cirq.measure)

    return circuit


def grover_iterate(oracle, qubits):
    circuit = cirq.Circuit()

    # +------------------------+
    # |Type your solution below|
    # +------------------------+

    # +------------------------+
    # |Type your solution above|
    # +------------------------+

    return circuit


def grover(oracle, qubits):
    circuit = cirq.Circuit()

    # +------------------------+
    # |Type your solution below|
    # +------------------------+

    # +------------------------+
    # |Type your solution above|
    # +------------------------+

    return circuit


if __name__ == "__main__":
    import numpy as np

    np.set_printoptions(linewidth=200)
    print_circuit = lambda circuit: "  " + (
        str(circuit).replace("\n", "\n  ")
        if len(circuit) > 0
        else "<<This circuit contains no gates.>>"
    )
    print_matrix = lambda matrix: "  " + np.array2string(
        matrix,
        formatter={"complex_kind": lambda x: "{:1.1f}".format(x).rjust(9)},
    ).replace("\n", "\n  ")

    # Multiple controlled Z tests
    qubits = [
        cirq.GridQubit(0, 0),
        cirq.GridQubit(0, 1),
        cirq.GridQubit(0, 2),
        cirq.GridQubit(0, 3),
    ]
    multiple_controlled_Z_circuit = multiple_controlled_Z(qubits)
    matrix = multiple_controlled_Z_circuit.unitary(
        list(multiple_controlled_Z_circuit.all_qubits().difference(qubits))
        + qubits
    )[:16, :16]
    expected_matrix = np.diag(
        np.array([1.0] * 15 + [-1.0], dtype=np.complex64)
    )
    inner_product = (
        np.sum(np.conj(expected_matrix.flatten() * matrix.flatten())) / 16
    )
    corrected_matrix = np.exp(-1.0j * np.angle(inner_product)) * matrix
    print(
        "+------------------------------------------------------------------------------------------------+"
    )
    print(
        "|Part 1: We will test whether your multiple controlled Z circuit is working properly on 4 qubits.|"
    )
    print(
        "+------------------------------------------------------------------------------------------------+"
    )
    print("Your circuit is:")
    print()
    print(print_circuit(multiple_controlled_Z_circuit))
    print()
    print(
        "If you implemented the circuit well, it should implement the following matrix:"
    )
    print()
    print(print_matrix(expected_matrix))
    print()
    print("The matrix that is actually implemented is given as:")
    print()
    print(print_matrix(corrected_matrix))
    print()
    print(
        "The absolute value of the vectorized inner product between both matrices is: {}.".format(
            abs(inner_product)
        )
    )
    print(
        "If you implemented the multiple controlled Z circuit correctly, this value should be 1.0."
    )
    print()

    # W tests
    qubits = [
        cirq.GridQubit(0, 0),
        cirq.GridQubit(0, 1),
        cirq.GridQubit(0, 2),
        cirq.GridQubit(0, 3),
    ]
    W_circuit = W(qubits)
    matrix = W_circuit.unitary(
        qubit_order=list(W_circuit.all_qubits().difference(qubits)) + qubits
    )[:16, :16]
    expected_matrix = (
        np.eye(16, dtype=np.complex64)
        - np.array([1] * 16)[:, np.newaxis]
        * np.array([1] * 16)[np.newaxis, :]
        / 8.0
    )
    inner_product = (
        np.sum(np.conj(expected_matrix.flatten() * matrix.flatten())) / 16
    )
    corrected_matrix = np.exp(-1.0j * np.angle(inner_product)) * matrix
    print(
        "+----------------------------------------------------------------------------+"
    )
    print(
        "|Part 2: We will test whether your W circuit is working properly on 4 qubits.|"
    )
    print(
        "+----------------------------------------------------------------------------+"
    )
    print("Your circuit is:")
    print()
    print(print_circuit(W_circuit))
    print()
    print(
        "If you implemented the circuit well, it should implement the following matrix:"
    )
    print()
    print(print_matrix(expected_matrix))
    print()
    print("The matrix that is actually implemented is given as:")
    print()
    print(print_matrix(corrected_matrix))
    print()
    print(
        "The absolute value of the vectorized inner product between both matrices is: {}.".format(
            abs(inner_product)
        )
    )
    print(
        "If you implemented the W circuit correctly, this value should be 1.0."
    )
    print()

    # Grover iterate tests
    qubits = [
        cirq.GridQubit(0, 0),
        cirq.GridQubit(0, 1),
        cirq.GridQubit(0, 2),
        cirq.GridQubit(0, 3),
    ]
    oracle = cirq.Circuit()
    oracle.append(cirq.X(qubits[1]))
    oracle.append(cirq.CNOT(qubits[1], qubits[2]))
    oracle.append(cirq.X(qubits[2]))
    oracle.append(cirq.CNOT(qubits[2], qubits[0]))
    oracle.append(cirq.TOFFOLI(qubits[0], qubits[1], cirq.GridQubit(0, 42)))
    oracle.append(cirq.CCZ(qubits[2], cirq.GridQubit(0, 42), qubits[3]))
    oracle.append(cirq.TOFFOLI(qubits[0], qubits[1], cirq.GridQubit(0, 42)))
    oracle.append(cirq.CNOT(qubits[2], qubits[0]))
    oracle.append(cirq.X(qubits[2]))
    oracle.append(cirq.CNOT(qubits[1], qubits[2]))
    oracle.append(cirq.X(qubits[1]))
    grover_iterate_circuit = grover_iterate(oracle, qubits)
    matrix = grover_iterate_circuit.unitary(
        qubit_order=list(
            grover_iterate_circuit.all_qubits().difference(qubits)
        )
        + qubits
    )[:16, :16]
    oracle_matrix = oracle.unitary(
        qubit_order=list(oracle.all_qubits().difference(qubits)) + qubits
    )[:16, :16]
    expected_matrix = (
        np.eye(16, dtype=np.complex64)
        - np.array([1] * 16)[:, np.newaxis]
        * np.array([1] * 16)[np.newaxis, :]
        / 8.0
    ) @ oracle_matrix
    inner_product = (
        np.sum(np.conj(expected_matrix.flatten() * matrix.flatten())) / 16
    )
    corrected_matrix = np.exp(-1.0j * np.angle(inner_product)) * matrix
    print(
        "+----------------------------------------------------------------------------+"
    )
    print(
        "|Part 3: We will test whether your grover iterate works properly on 4 qubits.|"
    )
    print(
        "+----------------------------------------------------------------------------+"
    )
    print("The oracle circuit is:")
    print()
    print(print_circuit(oracle))
    print()
    print("Your circuit is:")
    print()
    print(print_circuit(grover_iterate_circuit))
    print()
    print(
        "If you implemented the circuit well, it should implement the following matrix:"
    )
    print()
    print(print_matrix(expected_matrix))
    print()
    print("The matrix that is actually implemented is given as:")
    print()
    print(print_matrix(corrected_matrix))
    print()
    print(
        "The absolute value of the vectorized inner product between both matrices is: {}.".format(
            abs(inner_product)
        )
    )
    print(
        "If you implemented the grover iterate circuit correctly, this value should be 1.0."
    )
    print()

    # Grover's algorithm test
    qubits = [
        cirq.GridQubit(0, 0),
        cirq.GridQubit(0, 1),
        cirq.GridQubit(0, 2),
        cirq.GridQubit(0, 3),
    ]
    oracle = cirq.Circuit()
    oracle.append(cirq.X(qubits[1]))
    oracle.append(cirq.CNOT(qubits[1], qubits[2]))
    oracle.append(cirq.X(qubits[2]))
    oracle.append(cirq.CNOT(qubits[2], qubits[0]))
    oracle.append(cirq.TOFFOLI(qubits[0], qubits[1], cirq.GridQubit(0, 42)))
    oracle.append(cirq.CCZ(qubits[2], cirq.GridQubit(0, 42), qubits[3]))
    oracle.append(cirq.TOFFOLI(qubits[0], qubits[1], cirq.GridQubit(0, 42)))
    oracle.append(cirq.CNOT(qubits[2], qubits[0]))
    oracle.append(cirq.X(qubits[2]))
    oracle.append(cirq.CNOT(qubits[1], qubits[2]))
    oracle.append(cirq.X(qubits[1]))
    grover_circuit = grover(oracle, qubits)
    res = cirq.Simulator().run(grover_circuit, repetitions=20)
    print(
        "+---------------------------------------------------------------------------+"
    )
    print(
        "|Part 4: We will test whether Grover's algorithm works properly on 4 qubits.|"
    )
    print(
        "+---------------------------------------------------------------------------+"
    )
    print("The oracle circuit is:")
    print()
    print(print_circuit(oracle))
    print()
    print(
        "Your circuit is (might look weird if things wrap around to the next line, copy to text editor and disable text wrapping to see what is going on):"
    )
    print()
    print(print_circuit(grover_circuit))
    print()
    print(
        "If you implemented Grover's algortihm correctly, the measurement outcome should roughly look like this:"
    )
    print()
    print("  a={}, {}, {}, {}".format("0" * 20, "0" * 20, "1" * 20, "1" * 20))
    print()
    print(
        "The actual measurement outcome is (a few measurement errors may occur as the success probability is not 100%):"
    )
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
