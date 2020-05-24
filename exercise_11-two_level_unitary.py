import cirq

def two_level_unitary(cU, qubits):
    circuit = cirq.Circuit()

    # +------------------------+
    # |Type your solution below|
    # +------------------------+



    # +------------------------+
    # |Type your solution above|
    # +------------------------+

    return circuit

if __name__ == "__main__":
    i,j = 0b0110010,0b1100100
    import numpy as np
    from math import cos,sin,pi
    from functools import reduce
    import itertools as it
    qubits = [cirq.GridQubit(0,i) for i in range(7)]
    theta = 4*pi/9
    U = np.array([[cos(theta), sin(theta)], [-sin(theta), cos(theta)]], dtype = np.complex64)
    cU_circuit = cirq.Circuit()
    sqU = cirq.SingleQubitMatrixGate(U)
    sqU._circuit_diagram_info_ = lambda self : cirq.protocols.CircuitDiagramInfo(('U',))
    cU = reduce(lambda x,_ : cirq.ControlledGate(x), qubits[:-1], sqU)
    cU_circuit.append(cU(*qubits))
    circuit = two_level_unitary(cU_circuit, qubits)
    C = circuit.to_unitary_matrix()
    non_trivial_entries = {}
    for k,l in it.product(*map(range, C.shape)):
        if (k == l and abs(C[k,l] - 1.) > 1e-4) or (k != l and abs(C[k,l]) > 1e-4):
            non_trivial_entries[(k,l)] = C[k,l]
    print_circuit = lambda circuit : "  " + (str(circuit).replace('\n','\n  ') if len(circuit) > 0 else "<<This circuit contains no gates.>>")
    print("The oracle circuit is:")
    print()
    print(print_circuit(cU_circuit))
    print()
    print("The full circuit is:")
    print()
    print(print_circuit(circuit))
    print()
    print("Let G be the matrix representation of this circuit. The only non-trivial matrix entries of G should be:")
    print()
    print("  G[{:07b},{:07b}] = {}".format(i,i,U[0,0]))
    print("  G[{:07b},{:07b}] = {}".format(i,j,U[0,1]))
    print("  G[{:07b},{:07b}] = {}".format(j,i,U[1,0]))
    print("  G[{:07b},{:07b}] = {}".format(j,j,U[1,1]))
    print()
    print("The actual non-trivial matrix entries of C are:")
    print()
    if non_trivial_entries:
        for (k,l),v in sorted(non_trivial_entries.items()):
            print("  G[{:07b},{:07b}] = {}".format(k,l,v))
    else:
        print("  <No non-trivial entries.>>")
    print()
