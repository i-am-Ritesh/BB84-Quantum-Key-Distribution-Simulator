class Statistics:
    def __init__(self):
        self.total_qubits = 0
        self.sifted_key_length = 0
        self.secret_key_length = 0
        self.qber = 0.0
        self.transmission_efficiency = 0.0
        self.key_generation_rate = 0.0
    def calculate(
        self,
        total_qubits,
        sifted_key,
        secret_key,
        qber
    ):
        self.total_qubits = total_qubits
        self.sifted_key_length = len(sifted_key)
        if isinstance(secret_key, str):
            self.secret_key_length = len(secret_key)
        else:
            self.secret_key_length = len(secret_key)
        self.qber = qber
        if self.total_qubits > 0:
            self.transmission_efficiency = (
                self.sifted_key_length
                / self.total_qubits
            ) * 100
            self.key_generation_rate = (
                self.secret_key_length
                / self.total_qubits
            ) * 100
        else:
            self.transmission_efficiency = 0
            self.key_generation_rate = 0
    def summary(self):
        return {
            "total_qubits": self.total_qubits,
            "sifted_key_length": self.sifted_key_length,
            "secret_key_length": self.secret_key_length,
            "qber": round(self.qber, 4),
            "transmission_efficiency": round(
                self.transmission_efficiency,
                2
            ),
            "key_generation_rate": round(
                self.key_generation_rate,
                2
            )
        }
if __name__ == "__main__":
    stats = Statistics()
    stats.calculate(
        total_qubits=32,
        sifted_key=[1] * 18,
        secret_key="1010010110011010",
        qber=0.0625
    )
    print(stats.summary())