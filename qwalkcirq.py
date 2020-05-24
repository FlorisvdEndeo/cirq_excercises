import cirq

c = cirq.Circuit()

phys = (cirq.GridQubit(0,i) for i in range(3))

ancil = (cirq.GridQubit(0,i) for i in range(4,6))

ancil = (cirq.GridQubit(0,i) for i in range(6,8))

print(c)
