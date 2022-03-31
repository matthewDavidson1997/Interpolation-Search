import numpy as np
from numpy import random


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
    idx_top = len(array) - 1
    idx_bottom = 0
    val_top = array[idx_top]
    val_bottom = array[idx_bottom]
    search_count = 0

    while (
        key >= val_bottom
        and key <= val_top
        and val_top != val_bottom
    ):
        print(f'Key: {key} | Bottom: {idx_bottom} | Top: {idx_top} | v_bottom: {val_bottom} | v_top: {val_top}')

        idx_guess = ((idx_top - idx_bottom) * (key - val_bottom)) // (val_top - val_bottom) + idx_bottom
        search_count += 1
        # case if key is found at array index i
        if array[idx_guess] == key:
            print(f'Key: {key} found at index: {idx_guess} after {search_count} iteration(s)')
            break
        # case if key is greater than array index i
        if array[idx_guess] < key:
            print(f'Index guess: {idx_guess} value: {array[idx_guess]} too low. Key: {key} | iteration: {search_count}')
            array_elimination = (((idx_guess + 1) - idx_bottom) / ((idx_top + 1) - idx_bottom))
            print(f'Percentage of array eliminated: {array_elimination * 100}%')
            idx_bottom = (idx_guess + 1)
            val_bottom = array[idx_bottom]
            # if array_elimination < 0.25:
            #    idx_top, idx_bottom = binary_search(array, idx_top, idx_bottom, key)
        # case if key is less than array index i
        if array[idx_guess] > key:
            print(f'Index guess: {idx_guess} value: {array[idx_guess]} too high. Key: {key} | iteration: {search_count}')
            array_elimination = ((idx_top - (idx_guess - 1)) / ((idx_top + 1) - idx_bottom))
            print(f'Percentage of array eliminated: {array_elimination * 100}%')
            idx_top -= idx_top - (idx_guess - 1)
            val_top = array[idx_top]
            # if array_elimination < 0.25:
            #    idx_top, idx_bottom = binary_search(array, idx_top, idx_bottom, key)


def binary_search(array, key):
    idx_top = len(array) - 1
    idx_bottom = 0
    search_count = 0
    mid = ((idx_top - idx_bottom) // 2)
    print('mid = ', mid)

    while (
        key >= array[idx_bottom]
        and key <= array[idx_top]
        and array[idx_top] != array[idx_bottom]
    ):
        if array[mid] == key:
            search_count += 1
            print('Binary. key: ', key, ' | ', 'iteration: ', search_count)
        if array[mid] < key:
            search_count += 1
            print('Binary. Too low. Key: ', key, ' | ', 'iteration: ', search_count)
            idx_bottom = (mid + 1)

        if array[mid] > key:
            search_count += 1
            print('Binary. Too high. Key: ', key, ' | ', 'iteration: ', search_count)
            idx_top -= idx_top - (mid - 1)



if __name__ == '__main__':

    min_val = 1
    max_val = 10000
    array_length = 100
    search_array = generate_random_array(min_val, max_val, array_length)
    search_key = get_key_from_array(search_array)
    interpolation_search(search_array, search_key)
    # binary_search(search_array, search_key)
