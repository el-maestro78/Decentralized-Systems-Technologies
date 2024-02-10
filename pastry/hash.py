import hashlib
import random
from datetime import datetime

hashed_id_list = []


def hash_function(data, num_bits=4):
    """Calculate the hashed value for the key.
            :param str data: The key or node we want to hash
            :param int num_bits: Equal to Pastry's m
            :return: Hashed value of data.
            :rtype: int"""
    data = str(data)
    sha1_hash = hashlib.sha1(data.encode('utf-8')).hexdigest()
    # print(sha1_hash)
    num_bits -= 2
    truncated_hash = int(sha1_hash[:num_bits], 16)
    # truncated_hash = fix_prefix(truncated_hash, num_bits)
    # truncated_hash = check_hash(truncated_hash, num_bits)
    hashed_id_list.append(truncated_hash)
    return truncated_hash


def check_hash(truncated_hash, num_bits, repetitions=1):
    """Check if the hashed value already exists.
            :param truncated_hash: Hashed key we want to check
            :param int num_bits: Equal to Pastry's m
            :param int repetitions: How many times we have repeated this function
            :return: New hashed value.
            :rtype: int"""
    if truncated_hash in hashed_id_list:
        random.seed(random.randint(repetitions * 100, 1000 * repetitions))
        exp = random.randint(1, 50)
        current_time = datetime.now()
        timestamp = int(current_time.timestamp() * repetitions)
        random.seed(timestamp * repetitions)

        truncated_hash = str(random.randint(1, truncated_hash**exp+3))
        sha1_hash = hashlib.sha1(truncated_hash.encode('utf-8')).hexdigest()
        truncated_hash = int(sha1_hash[:num_bits], 16)
        truncated_hash = fix_prefix(truncated_hash, num_bits)
        if truncated_hash in hashed_id_list:
            check_hash(truncated_hash, num_bits, (repetitions * random.randint(1, 100)))
    return truncated_hash


def fix_prefix(hashed_value, num_bits):
    """The first bit should be on of the bits.
                :param hashed_value: Hashed key we want to check
                :param int num_bits: Equal to Pastry's m
                :return: Hashed value with fix prefix.
                :rtype: int"""
    previous_pre = 0
    random.seed()
    prefix = random.randint(1, num_bits)
    if prefix == previous_pre:
        if (prefix+1) == num_bits:
            prefix -= 1
        else:
            prefix += 1
    return int(str(prefix).join(str(hashed_value)))
