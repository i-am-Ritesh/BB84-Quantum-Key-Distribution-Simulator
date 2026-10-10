class ErrorCorrection:
    def __init__(self, block_size=4):
        self.block_size = block_size
        self.corrected_key = []
        self.corrected_errors = 0
    def parity(self, block):
        return sum(block) % 2
    def reconcile(self, alice_key, bob_key):
        self.corrected_key = bob_key.copy()
        self.corrected_errors = 0
        n = len(alice_key)
        for start in range(0, n, self.block_size):
            end = min(start + self.block_size, n)
            alice_block = alice_key[start:end]
            bob_block = self.corrected_key[start:end]
            if self.parity(alice_block) != self.parity(bob_block):
                for i in range(len(alice_block)):
                    if alice_block[i] != bob_block[i]:
                        self.corrected_key[start + i] = alice_block[i]
                        self.corrected_errors += 1
        return self.corrected_key
    def statistics(self):
        return {
            "block_size": self.block_size,
            "corrected_errors": self.corrected_errors
        }
if __name__ == "__main__":
    alice = [1, 0, 1, 1, 0, 0, 1, 0]
    bob = [1, 1, 1, 1, 0, 1, 1, 0]
    ec = ErrorCorrection(block_size=4)
    corrected = ec.reconcile(alice, bob)
    print("Alice     :", alice)
    print("Bob       :", bob)
    print("Corrected :", corrected)
    print(ec.statistics())