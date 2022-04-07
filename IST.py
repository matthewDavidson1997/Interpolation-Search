import random


def generate_random_int_array(min_val, max_val, array_length):
    """Generates a random list of (potentially repeating) integers.

    Args:
        min_val (int): The minimum integer value to consider.
        max_val (int): The maximum integer value to consider.
        array_length (int): The number of integers in the array.

    Returns:
        list: A list of integers.
    """
    return [random.randint(min_val, max_val) for _ in range(array_length)]


def get_random_array_item(array):
    """Chooses a random item from a list.

    Args:
        array (list): A list.

    Returns:
        Any: The random item.
    """
    return array[random.randrange(0, len(array))]


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

    def _calc_array_elimination(self, idx_guess, idx_top, idx_bottom, mode):
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

        print(f'Index guess {idx_guess} value ({self.array[idx_guess]}) is too {mode}.')
        print(f'Percentage of array eliminated: {array_elimination:.0%}')
        return array_elimination

    def _idx_guess(self, idx_top, idx_bottom, search_mode):
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
        self._print_info(idx_top, idx_bottom, comment=f'{search_mode.capitalize()} search')
        return idx_guess

    def _set_search_mode(self, array_elimination_fraction, search_mode):
        # TODO - write doc-string

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

    def search(self, query_val, interpolation_threshold=0.25, search_strategy='mixed'):
        """Search for the position of query_val in the array.

        TODO - explain the search strategy here

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
                continue

            # If query_val is less than the values at array index 'idx_guess'
            elif self.array[idx_guess] > query_val:
                array_elimination_fraction = self._calc_array_elimination(idx_guess, idx_top, idx_bottom, mode='high')
                # Set the new highest index for guessing to one below the index guess we just made
                idx_top = idx_guess - 1
                if search_strategy == 'mixed':
                    search_mode = self._set_search_mode(array_elimination_fraction, search_mode)
                continue

        print(f'The query value ({query_val}) was found at index {idx_guess} (of the sorted array) after {self.search_count} iteration(s)')
        return self.query_val_idx


if __name__ == '__main__':

    min_val = -10000
    max_val = 100000000
    array_length = 10000
    search_array = generate_random_int_array(min_val, max_val, array_length)
    query_val = get_random_array_item(search_array)
    searcher = ArraySearcher(search_array)

    search_counts = []
    methods = []
    strategies = ['interpolation', 'binary']
    for strategy in strategies:
        searcher.search(query_val, search_strategy=strategy)
        search_counts.append(searcher.search_count)
        methods.append(strategy)

    thresholds = [0.1, 0.25, 0.5, 0.75]
    for threshold in thresholds:
        searcher.search(query_val, interpolation_threshold=threshold)
        search_counts.append(searcher.search_count)
        methods.append(f'mixed ({threshold} threshold)')

    for method, search_count in zip(methods, search_counts):
        print(f'With {method} method it took {search_count} search steps to find the query value.')
