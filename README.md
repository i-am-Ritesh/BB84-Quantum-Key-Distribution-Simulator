# BB84-Quantum-Key-Distribution-Simulator
# 🔐 BB84 Quantum Key Distribution Simulator

**Team:** Q-Syndicate  
**Track:** Quantum Computing / Cryptography  
**Problem Statement:** Secure Quantum Key Distribution using BB84

---

## 📖 Project Overview

This project is an **end-to-end web-based simulator** of the **BB84 Quantum Key Distribution (QKD) protocol** — the world's first quantum cryptography protocol, proposed by Bennett and Brassard in 1984.

Classical public-key cryptography (RSA, ECC) relies on computational hardness that will be broken by future quantum computers running **Shor's algorithm**. BB84 instead bases its security on the **laws of physics** — specifically the **no-cloning theorem** and the fact that measuring a quantum state in the wrong basis disturbs it irreversibly.

Our simulator models the complete BB84 pipeline with three actors:

- **Alice** — prepares and sends qubits
- **Bob** — receives and measures qubits
- **Eve** *(optional)* — performs an intercept-resend attack

It demonstrates how eavesdropping is **automatically detected** through a rise in the **Quantum Bit Error Rate (QBER)**, and how error correction + privacy amplification produce a shorter but information-theoretically secure final key.

### Key Features

- ✅ Full BB84 protocol simulation using **Qiskit** and **Qiskit Aer**
- ✅ Configurable **qubit count**, **channel noise**, and **Eve attack**
- ✅ Real-time **QBER analysis** with an ~11% eavesdropping threshold
- ✅ **Cascade-style error correction** and **SHA-256 privacy amplification**
- ✅ Interactive **web UI** built with Flask + HTML/CSS/JavaScript
- ✅ **Matplotlib visualizations** (QBER, key-length reduction, basis distribution, Eve activity)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      BROWSER (Frontend)                     │
│   index.html  •  style.css  •  script.js  (Fetch API)       │
└──────────────────────────┬──────────────────────────────────┘
                           │  HTTP POST /simulate
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FLASK BACKEND (app.py)                   │
│              REST API  •  CORS-enabled                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               BB84 SIMULATION CORE (Python)                 │
│                                                             │
│   bb84.py              → Main orchestrator                  │
│   quantum_channel.py   → Noisy channel model                │
│   eve.py               → Intercept-resend attacker          │
│   error_correction.py  → Cascade parity reconciliation      │
│   privacy_amplification.py → SHA-256 hashing                │
│   bb84_statistics.py   → Metrics & summary                  │
│   plots.py             → Matplotlib visualizations          │
│                                                             │
│              Qiskit + Qiskit Aer (Quantum)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Project Structure

```
Minor_Project/
│
├── backend/
│   ├── app.py                     # Flask REST API
│   ├── bb84.py                    # BB84 protocol orchestrator
│   ├── quantum_channel.py         # Noisy quantum channel
│   ├── eve.py                     # Eavesdropper (intercept-resend)
│   ├── error_correction.py        # Cascade-style reconciliation
│   ├── privacy_amplification.py   # SHA-256 key compression
│   ├── bb84_statistics.py         # Statistics calculator
│   └── plots.py                   # Matplotlib visualizations
│
└── frontend/
    ├── index.html                 # Web UI
    ├── style.css                  # Styling
    └── script.js                  # Fetch API + DOM handling
```

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites

- **Python 3.9+** ([download](https://www.python.org/downloads/))
- **pip** (comes with Python)
- A modern browser (Chrome / Edge / Firefox)
- *(Optional)* **VS Code** + Live Server extension for the frontend

### 2️⃣ Install Python Dependencies

Open a terminal inside the `backend/` folder and run:

```bash
pip install flask flask-cors qiskit qiskit-aer matplotlib
```

Or use a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate         # Windows
# source venv/bin/activate    # macOS / Linux

pip install flask flask-cors qiskit qiskit-aer matplotlib
```

### 3️⃣ Start the Flask Backend

```bash
cd backend
python app.py
```

Expected output:

```
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

⚠️ **Keep this terminal open.** The backend must stay running while you use the UI.

### 4️⃣ Launch the Frontend

**Option A — Live Server (recommended):**

1. Open the `frontend/` folder in VS Code
2. Right-click `index.html` → **Open with Live Server**
3. Browser opens at `http://127.0.0.1:5500/index.html`

**Option B — Direct open:**

Double-click `frontend/index.html` in File Explorer.  
*(Note: some browsers block CORS for `file://` origins — Live Server is safer.)*

### 5️⃣ Run a Simulation

1. Set **Number of Qubits** (start with 32)
2. Adjust **Noise** slider (0 – 0.20)
3. Toggle **Eve Attack** on/off
4. Click **Run Simulation**

Results appear instantly: Alice's bits/bases, Bob's measurements, sifted keys, the final secret key, and live QBER.

### 6️⃣ *(Optional)* Run Standalone Python Tests

Each module can be tested independently:

```bash
python bb84.py                    # Full simulation + plots
python quantum_channel.py         # Channel noise test
python eve.py                     # Eve behavior test
python error_correction.py        # Reconciliation test
python privacy_amplification.py   # Hashing test
python bb84_statistics.py         # Statistics test
python plots.py                   # Visualizations test
```

---

## 🔬 Implementation Details

### 1. Quantum Circuit Preparation (`bb84.py`)

Alice encodes each bit into a qubit:

| Bit | Basis | Preparation |
|-----|-------|-------------|
| 0   | `+` (Z) | \|0⟩ (no gate) |
| 1   | `+` (Z) | \|1⟩ (`X` gate) |
| 0   | `x` (X) | \|+⟩ (`H` gate) |
| 1   | `x` (X) | \|−⟩ (`X` → `H` gates) |

```python
def prepare_qubit(self, bit, basis):
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if basis == "x":
        qc.h(0)
    return qc
```

### 2. Measurement (`bb84.py`)

Bob applies an `H` gate if he chose the X basis, then measures:

```python
def measure_qubit(self, circuit, basis):
    qc = circuit.copy()
    if basis == "x":
        qc.h(0)
    qc.measure(0, 0)
    job = self.backend.run(qc, shots=1)
    counts = job.result().get_counts()
    return int(list(counts.keys())[0])
```

**Why it works:** If Bob uses the *same* basis as Alice, he gets the correct bit 100% of the time. If he uses the *wrong* basis, he gets a random result — which is why wrong-basis qubits are discarded during sifting.

### 3. Sifting (`bb84.py`)

Alice and Bob publicly compare bases (but *not* bits) and keep only matching positions:

```python
def sift_keys(self):
    self.sifted_alice = []
    self.sifted_bob = []
    for i in range(self.num_bits):
        if self.alice_bases[i] == self.bob_bases[i]:
            self.sifted_alice.append(self.alice_bits[i])
            self.sifted_bob.append(self.bob_results[i])
```

On average, **~50% of qubits survive sifting**.

### 4. Eavesdropping — Intercept-Resend (`eve.py`)

Eve intercepts each qubit, measures it in a random basis, then re-sends it prepared in her measured basis:

```python
def choose_basis(self):
    return random.choice(["+", "x"])
```

Because Eve guesses the basis correctly only ~50% of the time, her measurements **disturb** the qubits in ~25% of cases — which is exactly why QBER rises detectably.

### 5. Quantum Bit Error Rate (`bb84.py`)

```python
def calculate_qber(self):
    errors = sum(1 for a, b in zip(self.sifted_alice, self.sifted_bob) if a != b)
    self.qber = errors / len(self.sifted_alice) if self.sifted_alice else 0
```

- **QBER ≈ 0%** → clean channel, no Eve
- **QBER ≈ 11%** → security threshold (BB84 is compromised above this)
- **QBER ≈ 25%** → classic intercept-resend attack (Eve present, no noise)

### 6. Error Correction — Cascade Parity (`error_correction.py`)

Bits are divided into blocks; parity mismatches are detected and corrected:

```python
def reconcile(self, alice_key, bob_key):
    self.corrected_key = bob_key.copy()
    for start in range(0, len(alice_key), self.block_size):
        end = min(start + self.block_size, len(alice_key))
        a_block = alice_key[start:end]
        b_block = self.corrected_key[start:end]
        if self.parity(a_block) != self.parity(b_block):
            for i in range(len(a_block)):
                if a_block[i] != b_block[i]:
                    self.corrected_key[start + i] = a_block[i]
                    self.corrected_errors += 1
    return self.corrected_key
```

### 7. Privacy Amplification (`privacy_amplification.py`)

The corrected key is hashed with **SHA-256** to compress it into a shorter, uniformly random secret — defeating any partial information Eve may have gathered:

```python
bit_string = "".join(str(b) for b in corrected_key)
digest = hashlib.sha256(bit_string.encode()).hexdigest()
binary_hash = bin(int(digest, 16))[2:].zfill(256)
self.secret_key = binary_hash[:len(corrected_key)]
```

### 8. Statistics (`bb84_statistics.py`)

| Metric | Formula |
|--------|---------|
| Transmission efficiency | `sifted_key_length / total_qubits × 100` |
| Key generation rate | `secret_key_length / total_qubits × 100` |
| QBER | `errors / sifted_key_length` |

### 9. Flask REST API (`app.py`)

**Endpoint:** `POST /simulate`

**Request:**
```json
{
  "num_bits": 32,
  "eve": true,
  "noise_probability": 0.03
}
```

**Response:**
```json
{
  "success": true,
  "simulation": {
    "alice_bits": [...],
    "alice_bases": [...],
    "bob_bases": [...],
    "bob_results": [...],
    "sifted_alice": [...],
    "sifted_bob": [...],
    "secret_key": "101101...",
    "secret_key_length": 18,
    "qber": 0.1142,
    "eve_enabled": true,
    "noise_probability": 0.03,
    "statistics": { ... }
  }
}
```

### 10. Frontend (`script.js`)

- Reads inputs from the control panel
- Sends a `fetch()` POST to `http://127.0.0.1:5000/simulate`
- Populates the DOM with Alice/Bob/Eve data, sifted keys, and the final secret key
- Displays QBER and shows a live simulation log

---

## 📊 Expected Results

| Scenario | Sifted Key | QBER | Secret Key |
|----------|-----------|------|------------|
| No Eve, no noise | ~50% | 0% | Full length |
| No Eve, 3% noise | ~50% | ~3% | Reduced |
| Eve, no noise | ~50% | **~25%** | Severely reduced |

These match theoretical BB84 predictions and validate the simulator's correctness.

---

## 🚧 Challenges & Future Scope

**Challenges Addressed**

- Modelling realistic quantum noise and decoherence
- Balancing simulator fidelity vs. real quantum hardware behavior
- Performance scaling at large bit lengths (currently one circuit per qubit)

**Future Roadmap**

- Deploy on **real IBM Quantum hardware**
- Implement **LDPC / Turbo** error correction (replacing Cascade)
- Build a **multi-user QKD network** simulator
- Enhanced privacy amplification using **universal hashing**
- Real-time 3D **Bloch sphere** visualization of qubit states

---

## 👥 Team — Q-Syndicate

| Role | Name |
|------|------|
| Team Lead | **Ritesh Raj** |

**Track:** Quantum Computing / Cryptography  
**Project:** Secure Quantum Key Distribution using BB84

---

## 📄 License

This project is developed for academic and hackathon purposes (Hackathon 2.0).  
Feel free to fork, learn from, and extend it.

---

## 🙏 Acknowledgements

- **IBM Quantum** — for Qiskit and Qiskit Aer
- **Bennett & Brassard (1984)** — for the original BB84 protocol
- **Flask**, **Matplotlib**, and the open-source Python community
