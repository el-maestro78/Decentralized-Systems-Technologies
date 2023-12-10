import hashlib


def hash_function(data, num_bits=4):
    # Compute SHA-1 hash
    sha1_hash = hashlib.sha1(data.encode('utf-8')).hexdigest()
    print(sha1_hash)
    # Take the first `num_bits` bits and convert to an integer
    truncated_hash = int(sha1_hash[:num_bits], 16)

    # Return the result
    return truncated_hash


# Example usage:
data_to_hash = "example_data"
hash_result = hash_function(data_to_hash, num_bits=4)

print(f"Original Data: {data_to_hash}")
print(f"Hash Result (4 bits): {hash_result}")
