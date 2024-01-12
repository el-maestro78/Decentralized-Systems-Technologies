import hashlib


def hash_function(data, num_bits=4):
    data = str(data)
    sha1_hash = hashlib.sha1(data.encode('utf-8')).hexdigest()
    # print(sha1_hash)
    num_bits -= 2
    truncated_hash = int(sha1_hash[:num_bits], 16)
    return truncated_hash
