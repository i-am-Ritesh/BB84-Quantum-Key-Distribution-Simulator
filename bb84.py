#BB84 Quantum Key Distribution Protocol Simulator
import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from quantum_channel import QuantumChannel
from error_correction import ErrorCorrection
from eve import Eve
from privacy_amplification import PrivacyAmplification
from bb84_statistics import Statistics
from plots import BB84Plots
class BB84Simulator:
    def __init__(
            self,
            num_bits=32,
            eve=False,
            noise_probability=0.0
    ):
        self.num_bits = num_bits
        self.eve = eve
        self.eve_device = Eve()
        self.channel = QuantumChannel(noise_probability)
        self.backend = AerSimulator()
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_results = []
        self.sifted_alice = []
        self.sifted_bob = []
        self.corrected_key = []
        self.final_key = ""
        self.qber = 0
        self.error_correction = ErrorCorrection()
        self.privacy = PrivacyAmplification()
        self.statistics = Statistics()
    def random_bits(self):
        return random.choices([0, 1], k=self.num_bits)
    def random_bases(self):
        return random.choices(["+", "x"], k=self.num_bits)
    def prepare_qubit(self, bit, basis):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)
        if basis == "x":
            qc.h(0)
        return qc
    def measure_qubit(self, circuit, basis):
        qc = circuit.copy()
        if basis == "x":
            qc.h(0)
        qc.measure(0, 0)
        job = self.backend.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        measured = int(list(counts.keys())[0])
        return measured
    def transmit(self):
        self.alice_bits = self.random_bits()
        self.alice_bases = self.random_bases()
        self.bob_bases = self.random_bases()
        self.bob_results = []
        self.eve_device.clear()
        for i in range(self.num_bits):
            circuit = self.prepare_qubit(
            self.alice_bits[i],
            self.alice_bases[i]
        )
            if self.eve:
                eve_basis = self.eve_device.choose_basis()
                eve_result = self.measure_qubit(
                circuit,
                eve_basis
            )
                self.eve_device.bases.append(eve_basis)
                self.eve_device.results.append(eve_result)
                circuit = self.prepare_qubit(
                eve_result,
                eve_basis
            )
            result = self.measure_qubit(
                circuit,
                self.bob_bases[i]
         )
            result = self.channel.transmit(result)
            self.bob_results.append(result)
    def perform_error_correction(self):
        self.corrected_key = self.error_correction.reconcile(
            self.sifted_alice,
            self.sifted_bob
        )
    def sift_keys(self):
        self.sifted_alice = []
        self.sifted_bob = []
        for i in range(self.num_bits):
            if self.alice_bases[i] == self.bob_bases[i]:
                self.sifted_alice.append(
                    self.alice_bits[i]
                )
                self.sifted_bob.append(
                    self.bob_results[i]
                )
    def calculate_qber(self):
        errors = 0
        length = len(self.sifted_alice)
        if length == 0:
            self.qber = 0
            return
        for a, b in zip(
                self.sifted_alice,
                self.sifted_bob
        ):
            if a != b:
                errors += 1
        self.qber = errors / length
    def generate_secret_key(self):
        self.final_key = self.privacy.amplify(
        self.corrected_key
    )
    def run(self):
        self.transmit()
        self.sift_keys()
        self.calculate_qber()
        self.perform_error_correction()
        self.generate_secret_key()
        self.statistics.calculate(
            total_qubits=self.num_bits,
            sifted_key=self.sifted_alice,
            secret_key=self.final_key,
            qber=self.qber
        )
        return {
            "alice_bits": self.alice_bits,
            "alice_bases": self.alice_bases,
            "bob_bases": self.bob_bases,
            "bob_results": self.bob_results,
            "sifted_alice": self.sifted_alice,
            "sifted_bob": self.sifted_bob,
            "secret_key": self.final_key,
            "secret_key_length": len(self.final_key),
            "qber": round(self.qber, 4),
            "eve_enabled": self.eve,
            "noise_probability": self.channel.get_noise(),
            "eve_bases": self.eve_device.bases,
            "eve_results": self.eve_device.results,
            "corrected_key": self.corrected_key,
            "corrected_errors": self.error_correction.corrected_errors,
            "privacy_statistics": self.privacy.statistics(),
            "statistics": self.statistics.summary(),
        }
if __name__ == "__main__":
    simulator = BB84Simulator(
        num_bits=32,
        eve=True,
        noise_probability=0.03
    )
    result = simulator.run()
    print("\n========== BB84 Simulation ==========\n")
    for key, value in result.items():
        print(f"{key} : {value}")
    BB84Plots.plot_basis_distribution(
        simulator.alice_bases,
        simulator.bob_bases
    )
    BB84Plots.plot_key_lengths(
        simulator.num_bits,
        len(simulator.sifted_alice),
        len(simulator.corrected_key),
        len(simulator.final_key)
    )
    BB84Plots.plot_qber(simulator.qber)
    BB84Plots.plot_bit_comparison(
        simulator.sifted_alice,
        simulator.sifted_bob
    )
    if simulator.eve:
        BB84Plots.plot_eve_activity(
            simulator.eve_device.bases
        )