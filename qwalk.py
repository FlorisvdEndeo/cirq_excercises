import numpy as np

# Import Qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
from qiskit.tools.visualization import plot_histogram, plot_state_city



# Construct a quantum circuit that initialises qubits to a custom state
circ = QuantumCircuit(2, 2)
circ.initialize([1, 0, 0, 1] / np.sqrt(2), [0, 1])
circ.measure([0,1], [0,1])

# Select the QasmSimulator from the Aer provider
simulator = Aer.get_backend('qasm_simulator')

# Execute and get counts
result = execute(circ, simulator).result()
counts = result.get_counts(circ)
plot_histogram(counts, title="Bell initial statevector")
