#Performing Eavesdropping Attack on BB84 Protocol
import random
class Eve:
    def __init__(self):
        self.bases = []
        self.results = []
    def choose_basis(self):
        return random.choice(["+", "x"])
    def clear(self):
        self.bases.clear()
        self.results.clear()
    def statistics(self):
        return {
            "attack": "Intercept-Resend",
            "measurements": len(self.results),
            "bases": self.bases,
            "results": self.results
        }
if __name__ == "__main__":
    eve = Eve()
    print("Testing Eve Module\n")
    for i in range(10):
        basis = eve.choose_basis()
        result = random.randint(0, 1)
        eve.bases.append(basis)
        eve.results.append(result)
        print(f"Qubit {i+1}: Basis = {basis}, Result = {result}")
    print("\nStatistics:")
    print(eve.statistics())