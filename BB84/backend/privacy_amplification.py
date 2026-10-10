import hashlib
class PrivacyAmplification:
    def __init__(self):
        self.original_key = []
        self.secret_key = ""
    def amplify(self, corrected_key):
        self.original_key = corrected_key.copy()
        if len(corrected_key) == 0:
            self.secret_key = ""
            return self.secret_key
        # Convert list of bits into a string
        bit_string = "".join(str(bit) for bit in corrected_key)
        # Compute SHA-256 hash
        digest = hashlib.sha256(
            bit_string.encode()
        ).hexdigest()
        # Convert hexadecimal hash to binary
        binary_hash = bin(
            int(digest, 16)
        )[2:].zfill(256)
        # Output key length equals corrected key length
        output_length = min(
            len(corrected_key),
            len(binary_hash)
        )
        self.secret_key = binary_hash[:output_length]
        return self.secret_key
    def statistics(self):
        return {
            "input_length": len(self.original_key),
            "output_length": len(self.secret_key)
        }
if __name__ == "__main__":
    corrected_key = [
        1,0,1,1,0,0,1,0,
        1,1,0,0,1,0,1,1
    ]
    pa = PrivacyAmplification()
    key = pa.amplify(corrected_key)
    print("Corrected Key")
    print(corrected_key)
    print()
    print("Secret Key")
    print(key)
    print()
    print(pa.statistics())