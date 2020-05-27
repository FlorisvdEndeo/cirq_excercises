import cirq
from cmath import polar, exp
from math import atan2,pi,e,sqrt
import numpy as np


def ZYZ(qubit):
    U = np.array([
        [-0.36 + 0.48j, -0.48 + 0.64j],
        [-0.7488 - 0.2816j, 0.5616 + 0.2112j]
    ])

    gamma, beta, alpha = cirq.linalg.deconstruct_single_qubit_matrix_into_angles(U)

    return cirq.Circuit(
        cirq.Z(qubit)**(gamma/pi),
        cirq.Y(qubit)**(beta/pi),
        cirq.Z(qubit)**(alpha/pi),
    )


def ABC(cq, tq):
    U = np.array([
        [-0.36 + 0.48j, -0.48 + 0.64j],
        [-0.7488 - 0.2816j, 0.5616 + 0.2112j]
    ])

    detU = np.linalg.det(U)
    phase = atan2(detU.imag, detU.real) / U.shape[0]

    c, b, a = cirq.linalg.deconstruct_single_qubit_matrix_into_angles(U)

    # Decomposition into AXBXC, but with CNOT instead of X
    return cirq.Circuit(
        # C
        cirq.Z(tq)**((c-a)/2/pi),
        # X
        cirq.CNOT(cq, tq),
        # B
        cirq.Z(tq)**(-(c+a)/2/pi), cirq.Y(tq)**(-b/2/pi),
        # X
        cirq.CNOT(cq, tq),
        # A
        cirq.Y(tq)**(b/2/pi), cirq.Z(tq)**(a/pi),
        # Phase shift
        cirq.S(cq)**(-phase)
    )


if __name__ == "__main__":
    import numpy as np
    np.set_printoptions(linewidth=200)
    print_circuit = lambda circuit : "  " + (str(circuit).replace('\n','\n  ') if len(circuit) > 0 else "<<This circuit contains no gates.>>")
    print_matrix = lambda matrix : "  " + np.array2string(matrix, formatter = {'complex_kind' : lambda x : "{:1.3f}".format(x).rjust(16)}).replace('\n','\n  ')
    U = np.array([[-0.36+0.48j, -0.48+0.64j], [-0.7488-0.2816j, 0.5616+0.2112j]], dtype = np.complex64)

    # Check the single qubit gate
    qubit = cirq.GridQubit(0,0)
    circuit = ZYZ(qubit)
    matrix = circuit.unitary(qubit_order = [qubit] + list(circuit.all_qubits().difference([qubit])))
    expected_matrix = U
    inner_product = np.conj(expected_matrix.flatten().T) @ matrix.flatten() / 2
    corrected_matrix = np.exp(-1.j * np.angle(inner_product)) * matrix
    print("+--------------------------------------------------------------------------------------------+")
    print("|Part 1: We will check if you implemented a quantum circuit whose matrix representation is U.|")
    print("+--------------------------------------------------------------------------------------------+")
    print("The circuit you constructed was:")
    print()
    print(print_circuit(circuit))
    print()
    print("If you constructed the circuit correctly, its matrix representation should be:")
    print()
    print(print_matrix(expected_matrix))
    print()
    print("The actual matrix representation is:")
    print()
    print(print_matrix(corrected_matrix))
    print()
    print("The inner product between the vectorized expected and the actual matrix representation is: {:1.3f}.".format(abs(inner_product)))
    print("If you implemented the circuit correctly, this should be 1.000.")
    print()

    # Check the controlled gate
    cq,tq = cirq.GridQubit(0,0),cirq.GridQubit(0,1)
    circuit = ABC(cq,tq)
    matrix = circuit.unitary(qubit_order = [cq,tq] + list(circuit.all_qubits().difference([cq,tq])))
    expected_matrix = np.array([[1., 0. ,0., 0.],[0., 1. ,0., 0.],[0., 0., U[0,0], U[0,1]], [0., 0., U[1,0], U[1,1]]], dtype = np.complex64)
    inner_product = np.conj(expected_matrix.flatten().T) @ matrix.flatten() / 4
    corrected_matrix = np.exp(-1.j * np.angle(inner_product)) * matrix
    print("+-----------------------------------------------------------------------------------------------+")
    print("|Part 2: We will check if you implemented a quantum circuit whose matrix representation is C(U).|")
    print("+-----------------------------------------------------------------------------------------------+")
    print("The circuit you constructed was:")
    print()
    print(print_circuit(circuit))
    print()
    print("If you constructed the circuit correctly, its matrix representation should be:")
    print()
    print(print_matrix(expected_matrix))
    print()
    print("The actual matrix representation is:")
    print()
    print(print_matrix(corrected_matrix))
    print()
    print("The inner product between the vectorized expected and the actual matrix representation is: {:1.3f}.".format(abs(inner_product)))
    print("If you implemented the circuit correctly, this should be 1.000.")
