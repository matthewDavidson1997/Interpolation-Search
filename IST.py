import numpy as np
from numpy import random


def generate_random_array(min_val, max_val, array_length):
    search_array = random.randint(min_val, max_val, size=(array_length))
    np.sort(search_array)
    print(search_array)
    return search_array


generate_random_array(1, 10, 10)
