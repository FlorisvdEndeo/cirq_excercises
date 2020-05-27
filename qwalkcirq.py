import cirq

circuit = cirq.Circuit()

phys = (cirq.GridQubit(0,i) for i in range(3))

ancil = (cirq.GridQubit(0,i) for i in range(4,6))

ancil = (cirq.GridQubit(0,i) for i in range(6,8))

for n in


cirq.expand_matrix_in_orthogonal_basis(m: numpy.ndarray, basis: Dict[str, numpy.ndarray])
