import random

from numpy import array


class ArraySearcher:
    """A class for finding the position of an integer in a sorted array.
    The search method will use a combination of interpolation and binary search strategies.

    After the search() method has been called, the ArraySearcher's attributes can be explored to get information on the search.

    Post-search attributes:
        query_val:               The last value searched for in the array.
        search_strategy:         The search strategy used in the last search.
        interpolation_threshold: The interpolation threshold value used in the last search.
        query_val_idx:           The position found for the last query_val search.
        search_count:            The total number of search steps taken.
        interpolation_count:     The number of search steps that employed an interpolation search strategy.
        binary_count:            The number of search steps that employed a binary search strategy.
    """
    def __init__(self, array):
        """Initialise the ArraySearcher instance.

        Args:
            array (list): A list of integer values. This will get sorted.
        """
        self.array = sorted(array)

    def _print_info(self, idx_top, idx_bottom, comment):
        """Prints info about the last search iteration."""
        print(' | '.join(
            [
                f'Iteration: {self.search_count:>3}',
                f'{comment:<20}',
                f'Query value: {self.query_val}',
                f'Bottom index: {idx_bottom:>{len(str(idx_top))}}',
                f'Top index: {idx_top:>{len(str(idx_top))}}',
                f'Bottom value: {self.array[idx_bottom]:>{len(str(self.array[idx_top]))}}',
                f'Top value: {self.array[idx_top]:>{len(str(self.array[idx_top]))}}'
            ]
        ))

    def _calc_array_elimination(self, idx_guess, idx_top, idx_bottom, mode, verbose=False):
        """Calculates the fraction of the array that can be removed.

        Args:
            idx_guess (int): The current guess for the index of query_val.
            idx_top (int): The array index for the top of the current search space.
            idx_bottom (int): The array index for the bottom of the current search space.
            mode (str): 'low' if the idx_guess was too low.  'high' if the idx_guess was too high.

        Returns:
            float: The fraction of the current array search space that is removed by knowing idx_guess
                   is too low or too high.
        """
        if mode == 'low':
            array_elimination = (((idx_guess + 1) - idx_bottom) / ((idx_top + 1) - idx_bottom))
        elif mode == 'high':
            array_elimination = ((idx_top - (idx_guess - 1)) / ((idx_top + 1) - idx_bottom))

        if verbose:
            print(f'Index guess {idx_guess} value ({self.array[idx_guess]}) is too {mode}.')
            print(f'Percentage of array eliminated: {array_elimination:.0%}')
        return array_elimination

    def _idx_guess(self, idx_top, idx_bottom, search_mode, verbose=False):
        """Guess the index of query_val.

        Args:
            idx_top (int): The array index for the top of the current search space.
            idx_bottom (int): The array index for the bottom of the current search space.
            search_mode (str): 'interpolation' - an interpolation search strategy.
                               'binary' - a binary search strategy.
        """
        if search_mode == 'interpolation':
            self.interpolation_count += 1
            idx_guess = ((idx_top - idx_bottom) * (self.query_val - self.array[idx_bottom])) // (self.array[idx_top] - self.array[idx_bottom]) + idx_bottom
        elif search_mode == 'binary':
            self.binary_count += 1
            idx_guess = idx_bottom + (idx_top - idx_bottom) // 2
        self.search_count += 1
        if verbose:
            self._print_info(idx_top, idx_bottom, comment=f'{search_mode.capitalize()} search')
        return idx_guess

    def _set_search_mode(self, array_elimination_fraction, search_mode):
        """Method that checks and sets the search_mode based on simple rules."""
        # If we are running in mixed mode, make a decision about which search strategy to use next
        if search_mode == 'binary':
            # If we ran a binary search, then always try interpolation next
            return 'interpolation'
        elif array_elimination_fraction < self.interpolation_threshold:
            # If the last interpolation iteration did a poor job of reducing the search space,
            # swap to a binary search
            return 'binary'
        else:
            return search_mode

    def search(self, query_val, interpolation_threshold=0.25, search_strategy='mixed', verbose=False):
        """Search for the position of query_val in the array.

        Args:
            query_val (int): An integer value to find in the array.
            interpolation_threshold (float, optional): If an interpolation search step removes less than this fraction
                                                       of the search space then the next step will employ a binary
                                                       search strategy. Defaults to 0.25.
            search_strategy (str): 'mixed' (default) - starts with an interpolation search strategy, but will run one
                                                       step of binary search if an interpolation search step fails to
                                                       remove enough search space.
                                     'interpolation' - exclusively run interpolation search steps.
                                            'binary' - exclusively run binary search steps.

        Raises:
            ValueError: If query_val is outside of the range of the array.

        Returns:
            int: The index of query_val
        """
        # Initialise instance search attributes
        self.query_val = query_val
        self.search_strategy = search_strategy
        self.interpolation_threshold = interpolation_threshold
        self.query_val_idx = None
        self.search_count = 0
        self.interpolation_count = 0
        self.binary_count = 0

        # Initialise idx_top and idx_bottom
        idx_top = len(self.array) - 1
        idx_bottom = 0

        # Raise an error if the query_val is outside of the array range
        if not (query_val >= self.array[idx_bottom] and query_val <= self.array[idx_top]):
            raise ValueError(f'The query value ({query_val}) is outside of the array range ({self.array[0] - self.array[-1]}).')

        if verbose:
            # Print the initial status
            self._print_info(idx_top, idx_bottom, comment='Starting info')

        # Search loop
        if search_strategy in ['mixed', 'interpolation']:
            search_mode = 'interpolation'
        elif search_strategy == 'binary':
            search_mode = 'binary'
            interpolation_threshold = 1.0

        while self.query_val_idx is None:

            # This could be the case even before any search steps - so check before first guess
            if self.array[idx_top] == self.array[idx_bottom]:
                self.query_val_idx = idx_bottom
                break

            # Make a guess of the query_val index
            idx_guess = self._idx_guess(idx_top, idx_bottom, search_mode)

            # If query_val is found at array index 'idx_guess'
            if self.array[idx_guess] == query_val:
                self.query_val_idx = idx_guess
                break

            # If query_val is greater than the values at array index 'idx_guess'
            elif self.array[idx_guess] < query_val:
                array_elimination_fraction = self._calc_array_elimination(idx_guess, idx_top, idx_bottom, mode='low')
                # Set the new lowest index for guessing to one above the index guess we just made
                idx_bottom = idx_guess + 1
                if search_strategy == 'mixed':
                    search_mode = self._set_search_mode(array_elimination_fraction, search_mode)

            # If query_val is less than the values at array index 'idx_guess'
            elif self.array[idx_guess] > query_val:
                array_elimination_fraction = self._calc_array_elimination(idx_guess, idx_top, idx_bottom, mode='high')
                # Set the new highest index for guessing to one below the index guess we just made
                idx_top = idx_guess - 1
                if search_strategy == 'mixed':
                    search_mode = self._set_search_mode(array_elimination_fraction, search_mode)

        if verbose:
            print(f'The query value ({query_val}) was found at index {idx_guess} (of the sorted array) after {self.search_count} iteration(s)')
        return self.query_val_idx

    def compare_methods(self, query_val, mixed_thresholds=None, verbose=False):
        """Runs interpolation, mixed, and binary search methods and returns a dictionary of method names against
        iteration count for finding the query_val in the array.

        Args:
            query_val (int): The value we are looking for in the array.
            mixed_thresholds (list[ints], optional): If provided, this will not simply run the mixed mode with the
                                                     default threshold, but will compare using the provided values.
                                                     Defaults to None.
            verbose (bool, optional): Print information about the searching. Defaults to False.

        Returns:
            dict: A dictionary of search method names and search iterations.
        """
        performance_dict = {}

        for strategy in ['interpolation', 'mixed', 'binary']:
            args_list = [{'search_strategy': strategy}]
            if strategy == 'mixed' and mixed_thresholds is not None:
                args_list = [{'search_strategy': strategy, 'interpolation_threshold': t} for t in mixed_thresholds]

            for args_dict in args_list:
                threshold = args_dict.get('interpolation_threshold')
                if threshold:
                    strategy_name = f'{strategy}-{threshold}'
                else:
                    strategy_name = strategy
                self.search(query_val, **args_dict, verbose=verbose)
                performance_dict[strategy_name] = self.search_count

            if verbose:
                print(f'With {strategy_name} method it took {self.search_count} search step(s) to find the query value.')
        return performance_dict

    def get_random_array_item(self):
        """Chooses a random item from the array.

        Returns:
            int: The random array item.
        """
        return self.array[random.randrange(0, len(self.array))]


def generate_random_array(min_val, max_val, cardinality):
    """Generates an array (multiset) of random integers.

    Args:
        min_val (int): The minimum integer value to include in the array.
        max_val (int): The maximum integer value to include in the array.
        cardinality (str): The cardinality (length) of the array.

    Returns:
        list[ints]: A list of random integers.
    """
    return [random.randint(min_val, max_val) for _ in range(cardinality)]


def run_tests(start_cardinality, growth_mode, growth_factor, growth_steps, repeats, min_array_val, max_val_factor):
    """Runs repeated tests on each provided cardinality, generating a random array
    each time and comparing each splitting method on that array.

    Args:
        start_cardinality (int): The cardinality to start with.
        growth_mode (str): Whether to grow the cardinality arithmetically ('arithmetic'), or
                           geometrically ('geometric').
        growth_factor (int): The amount to grow the cardinality by on each step.
        growth_steps (int): The number of times to grow the cardinality.
        repeats (int): Number of repeats.
        min_array_val (int): Minimum possible value in the array.
        max_val_factor (int): Scaling factor to set the maximum possible
                              value in the array by multiplying by the cardinality.

    Returns:
        list[dicts]: A list of dictionaries of length 'repeats'.
                     Keys are the method names, plus 'cardinality'.
                     Values are the method absolute subset differences, plus cardinality
    """
    testing_results = []
    for _ in range(repeats):
        cardinality = start_cardinality
        for step in range(growth_steps):
            if growth_mode == 'arithmetic':
                cardinality = cardinality + (step * growth_factor)
            elif growth_mode == 'geometric':
                cardinality = cardinality * (step * growth_factor)

            array = generate_random_array(min_val=min_array_val, max_val=max_val_factor * cardinality,
                                          cardinality=cardinality)

            searcher = ArraySearcher(array)
            query_val = searcher.get_random_array_item()
            results = searcher.compare_methods(query_val)
            results['cardinality'] = cardinality
            testing_results.append(results)
    return testing_results


def main():
    MIN_ARRAY_VAL = 1
    START_CARDINALITY = 100
    MAX_VAL_FACTOR = 10
    GROWTH_STEPS = 100
    GROWTH_MODE = 'arithmetic'
    GROWTH_FACTOR = 2
    REPEATS = 10

    test_results = run_tests(start_cardinality=START_CARDINALITY, growth_mode=GROWTH_MODE, growth_factor=GROWTH_FACTOR,
                             repeats=REPEATS, min_array_val=MIN_ARRAY_VAL, max_val_factor=MAX_VAL_FACTOR)


if __name__ == '__main__':
    main()
