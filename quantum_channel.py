#Preparation of Quantum Channel for communication between Alice and Bob
import random
class QuantumChannel:
    def __init__(self, noise_probability=0.0):
        self.noise_probability = noise_probability
    def transmit(self, bit):
        if random.random() < self.noise_probability:
            return 1 - bit
        return bit
    def transmit_sequence(self, bits):
        return [self.transmit(bit) for bit in bits]
    def set_noise(self, probability):
        if probability < 0 or probability > 1:
            raise ValueError(
                "Noise probability must be between 0 and 1."
            )
        self.noise_probability = probability
    def get_noise(self):
        return self.noise_probability
    def statistics(self):
        return {
            "noise_probability": self.noise_probability,
            "channel": "Quantum Channel"
        }
if __name__ == "__main__":
    channel = QuantumChannel(
        noise_probability=0.20
    )
    bits = [0, 1, 1, 0, 0, 1, 1, 0]
    print("Original Bits")
    print(bits)
    transmitted = channel.transmit_sequence(bits)
    print()
    print("Received Bits")
    print(transmitted)
    print()
    print(channel.statistics())