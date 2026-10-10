import matplotlib.pyplot as plt
class BB84Plots:
    @staticmethod
    def plot_basis_distribution(alice_bases, bob_bases):
        labels = ["+", "x"]
        alice = [
            alice_bases.count("+"),
            alice_bases.count("x")
        ]
        bob = [
            bob_bases.count("+"),
            bob_bases.count("x")
        ]
        x = range(len(labels))
        width = 0.35
        plt.figure(figsize=(6,5))
        plt.bar(
            [i-width/2 for i in x],
            alice,
            width,
            label="Alice"
        )
        plt.bar(
            [i+width/2 for i in x],
            bob,
            width,
            label="Bob"
        )
        plt.xticks(x, labels)
        plt.xlabel("Basis")
        plt.ylabel("Number of Qubits")
        plt.title("Alice vs Bob Basis Selection")
        plt.legend()
        plt.tight_layout()
        plt.show()
    @staticmethod
    def plot_key_lengths(total, sifted, corrected, secret):
        labels = [
            "Original",
            "Sifted",
            "Corrected",
            "Secret"
        ]
        values = [
            total,
            sifted,
            corrected,
            secret
        ]
        plt.figure(figsize=(7,5))
        plt.bar(labels, values)
        plt.ylabel("Bits")
        plt.title("Key Length Through BB84")
        plt.tight_layout()
        plt.show()
    @staticmethod
    def plot_qber(qber):
        plt.figure(figsize=(5,5))
        plt.bar(
            ["QBER"],
            [qber*100]
        )
        plt.ylim(0,100)
        plt.ylabel("Percentage")
        plt.title("Quantum Bit Error Rate")
        plt.tight_layout()
        plt.show()
    @staticmethod
    def plot_bit_comparison(alice, bob):
        plt.figure(figsize=(10,4))
        plt.plot(
            alice,
            marker='o',
            label="Alice"
        )
        plt.plot(
            bob,
            marker='x',
            label="Bob"
        )
        plt.xlabel("Bit Position")
        plt.ylabel("Bit Value")
        plt.title("Alice vs Bob Sifted Keys")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    @staticmethod
    def plot_eve_activity(eve_bases):
        plus = eve_bases.count("+")
        cross = eve_bases.count("x")
        plt.figure(figsize=(5,5))
        plt.pie(
            [plus, cross],
            labels=["+","x"],
            autopct="%1.1f%%"
        )
        plt.title("Eve Basis Selection")
        plt.tight_layout()
        plt.show()
if __name__ == "__main__":
    print("Testing BB84 plots...")
    alice_bases = ["+", "x", "+", "+", "x", "+", "x", "+"]
    bob_bases = ["+", "+", "x", "+", "x", "x", "x", "+"]
    sifted_alice = [1, 0, 1, 1, 0]
    sifted_bob = [1, 1, 1, 0, 0]
    eve_bases = ["+", "+", "x", "x", "+", "x", "+", "x"]
    BB84Plots.plot_basis_distribution(
        alice_bases,
        bob_bases
    )
    BB84Plots.plot_key_lengths(
        8,
        5,
        5,
        5
    )
    BB84Plots.plot_qber(0.12)
    BB84Plots.plot_bit_comparison(
        sifted_alice,
        sifted_bob
    )
    BB84Plots.plot_eve_activity(
        eve_bases
    )