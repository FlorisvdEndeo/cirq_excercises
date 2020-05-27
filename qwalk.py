import numpy as np

# Import Qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
from qiskit.tools.visualization import plot_histogram, plot_state_city



# Construct a quantum circuit that initialises qubits to a custom state
circuit = QuantumCircuit(9)

for qubit in range(3)
    circuit.h(qubit)
#0 to 3, physical QuantumRegister
#4 to 7 ancillary
# 8 and 9 aux estimation
