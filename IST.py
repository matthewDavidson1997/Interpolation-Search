import numpy as np
from numpy import random
import math


def generate_random_array(min_val, max_val, array_length):
    search_array = random.randint(min_val, max_val, size=(array_length))
    sorted_search_array = np.sort(search_array,)
    print(sorted_search_array)
    return sorted_search_array


def get_key_from_array(array):
    random_key = random.choice(array)
    print(random_key)
    return random_key


def interpolation_search(array, key):
    top = len(array) - 1
    bottom = 0
    v_top = array[top]
    v_bottom = array[bottom]
    search_count = 0
    i = 0

    while (array[i] != key & key >= v_bottom & key <= v_top & v_top != v_bottom):
        print('Key: ', key, ' | Top: ', top, ' | Bottom: ', bottom, ' | v_bottom: ', v_bottom, ' | v_top: ', v_top)
        search_count += 1
        i = math.floor(((top - bottom) * (key - v_bottom)) / (v_top - v_bottom)) + bottom
        print(i)
        # case if key is found at array index i
        if array[i] == key:
            print('key: ', key, ' | iteration: ', search_count)
        # case if key is greater than array index i
        if array[i] < key:
            print('Too low. Key: ', key, ' | iteration: ', search_count)
            array_elimination = (((i + 1) - bottom) / len(array))
            bottom += (i + 1)
            if array_elimination < 0.25:
                binary_search(array, top, bottom, key)
        # case if key is less than array index i
        if array[i] > key:
            print('Too high. Key: ', key, ' | iteration: ', search_count)
            array_elimination = ((top - (i - 1)) / len(array))
            top -= top - (i - 1)
            #print(new_top)
            if array_elimination < 0.25:
                binary_search(array, top, bottom, key)


def binary_search(array, top, bottom, key):
    search_count = 0
    i = 0
    mid = ((top - bottom) // 2)
    print('mid = ', mid)

    if array[mid] == key:
        search_count += 1
        print('Binary. key: ', key, ' | ', 'iteration: ', search_count)
    if array[mid] < key:
        search_count += 1
        print('Binary. Too low. Key: ', key, ' | ', 'iteration: ', search_count)
        bottom += (mid + 1)
        return bottom
    if array[mid] > key:
        search_count += 1
        print('Binary. Too high. Key: ', key, ' | ', 'iteration: ', search_count)
        top -= top - (i - 1)
        return top

if __name__ == '__main__':

    min_val = 1
    max_val = 100000
    array_length = 100
    search_array = generate_random_array(min_val, max_val, array_length)
    search_key = get_key_from_array(search_array)
    interpolation_search(search_array, search_key)
l¾