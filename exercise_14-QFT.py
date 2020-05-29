import cirq

def QFT(qubits):
    circuit = cirq.Circuit()

    for i, bit1 in enumerate(qubits,1):
        circuit.append(cirq.H(bit1))
        for j, bit2 in enumerate(qubits[i:],1):
            circuit.append(cirq.CZ(bit1, bit2)**(0.5**j))

    for bit1, bit2 in zip(qubits[:len(qubits)//2], qubits[:len(qubits)//2-1:-1]):
        circuit.append([
            cirq.CNOT(bit1, bit2),
            cirq.CNOT(bit2, bit1),
            cirq.CNOT(bit1, bit2),
        ])

    return circuit

if __name__ == "__main__":
    import numpy as np
    np.set_printoptions(linewidth = 180)
    qubits = [cirq.GridQubit(0,i) for i in range(3)]
    circuit = QFT(qubits)
    matrix = circuit.unitary(qubit_order = list(circuit.all_qubits().difference(qubits)) + qubits)[:8,:8]
    expected_matrix = np.exp(.25j*np.pi * (np.arange(8)[:,np.newaxis] * np.arange(8)[np.newaxis,:])) / np.sqrt(8)
    inner_product = np.sum(np.conj(expected_matrix.flatten()) * matrix.flatten()) / 8
    corrected_matrix = np.exp(-1.j * np.angle(inner_product)) * matrix
    print_circuit = lambda circuit : "  " + (str(circuit).replace('\n','\n  ') if len(circuit) > 0 else "<<This circuit contains no gates.>>")
    print_matrix = lambda matrix : "  " + np.array2string(matrix, formatter = {'complex_kind' : lambda x : "{:1.3f}".format(x).rjust(16)}).replace('\n','\n  ')
    print("We will be checking whether the correct 3-qubit quantum Fourier transform is constructed.")
    print("The circuit you constructed is:")
    print()
    print(print_circuit(circuit))
    print()
    print("If you implemented the algorithm correctly, the corresponding matrix should be:")
    print()
    print(print_matrix(expected_matrix))
    print()
    print("The matrix corresponding to the circuit you drew is:")
    print()
    print(print_matrix(corrected_matrix))
    print()
    print("The absolute value of the vectorized inner product was: {}.".format(abs(inner_product)))
    print("If you did everything correctly, this value should be 1.0.")
