# BB84 Quantum Key Distribution (QKD) Simulator
This project implements a simulation of the "BB84 Quantum Key Distribution (QKD) protocol using Python, Qiskit, and Flask". The simulator demonstrates how two parties (Alice and Bob) can securely establish a shared secret key over a quantum channel while detecting the presence of an eavesdropper (Eve).
The project includes a web-based interface for running simulations and visualizing the protocol's output.

# Features
* BB84 Quantum Key Distribution protocol
* Quantum circuit implementation using Qiskit
* Alice and Bob random bit and basis generation
* Quantum channel with configurable noise
* Eve intercept-resend attack simulation
* Basis sifting
* Quantum Bit Error Rate (QBER) calculation
* Error correction module
* Privacy amplification module
* Protocol statistics generation
* Graphical visualization using Matplotlib
* Flask REST API backend
* Interactive HTML/CSS/JavaScript frontend

# Project Structure
Minor_Project/
├── backend/
│   ├── app.py
│   ├── bb84.py
│   ├── quantum_channel.py
│   ├── eve.py
│   ├── error_correction.py
│   ├── privacy_amplification.py
│   ├── statistics.py
│   └── plots.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── requirements.txt
└── README.md

# Technologies Used
* Python 3.x
* Qiskit
* Qiskit Aer
* Flask
* Flask-CORS
* NumPy
* Matplotlib
* HTML
* CSS
* JavaScript

# Installation
Clone the repository:
git clone <repository-url>
cd Minor_Project
Install the required packages:
pip install -r requirements.txt

# Running the Backend
Navigate to the backend directory:
cd backend
Start the Flask server:
python app.py
The server will start at:
http://127.0.0.1:5000

# Running the Frontend
Open the 'frontend/index.html' file in a web browser or serve it using a local web server.

# Running the Simulator from the Terminal
To execute the simulator without the web interface:
python bb84.py
This displays:
* Alice bits
* Alice bases
* Bob bases
* Bob measurements
* Sifted keys
* Secret key
* QBER
* Eve measurements
* Error correction results
* Privacy amplification results
* Protocol statistics
It also generates visualization plots.

# Simulation Workflow
1. Alice generates random bits.
2. Alice randomly selects quantum bases.
3. Alice prepares quantum states.
4. Qubits are transmitted through the quantum channel.
5. Optional Eve intercept-resend attack.
6. Bob randomly selects measurement bases.
7. Bob measures received qubits.
8. Alice and Bob perform basis sifting.
9. Quantum Bit Error Rate (QBER) is calculated.
10. Error correction is performed.
11. Privacy amplification generates the final secret key.
12. Protocol statistics and plots are produced.

# Generated Statistics
The simulator reports:
* Total transmitted qubits
* Sifted key length
* Secret key length
* Quantum Bit Error Rate (QBER)
* Transmission efficiency
* Key generation rate

# Generated Plots
The simulator can generate:
* Alice vs Bob basis distribution
* Key length comparison
* Quantum Bit Error Rate (QBER)
* Alice vs Bob sifted key comparison
* Eve basis selection distribution

# Future Improvements
* Support additional QKD protocols
* Advanced error correction algorithms
* More realistic quantum noise models
* Interactive protocol visualization
* Live protocol animation
* Export simulation results
* Performance benchmarking
* Multi-user simulations

# Educational Purpose
This project is intended for educational purposes to demonstrate the principles of quantum cryptography and the BB84 Quantum Key Distribution protocol using Qiskit.

# License
This project is intended for academic and educational use.