import hashlib


def hash_function(data, num_bits=4):
    sha1_hash = hashlib.sha1(data.encode('utf-8')).hexdigest()
    # print(sha1_hash)
    num_bits -= 2
    truncated_hash = int(sha1_hash[:num_bits], 16)
    return truncated_hash


"""
h1 = hash_function("test", 3)
print(h1)
h2 = hash_function("test", 4)
print(h2)
h3 = hash_function("test", 6)
print(h3)
h4 = hash_function("test", 128)
print(h4)
"""