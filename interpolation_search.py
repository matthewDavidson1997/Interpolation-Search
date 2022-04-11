import random

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from tqdm import tqdm


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


def generate_random_array(cardinality,
                          space='arithmetic',
                          start_range=(1, 1000),
                          step_range=(1, 1000),
                          sample_space_scale=None):
    """Generate an array sampled from a random arithmetic or geometric progression.

    Args:
        cardinality (int): Length of the returned array.
        space (str, optional): Space of the progression being sampled from ('arithmetic' or
                               'geometric'). Defaults to 'arithmetic'.
        start_range (tuple[ints], optional): Min and max values for the progression start.
                                             Defaults to (1, 1000).
        step_range (tuple[ints], optional): Min and max values for the progression step.
                                            Defaults to (1, 1000).
        sample_space_scale (None or int, optional): If None, then the returned array will be
                                                    a true progression.
                                                    If int, then this is how 'fold-bigger' the
                                                    sampled progression is vs the returned array.
                                                    Defaults to None.

    Returns:
        list[ints]: The array.
    """
    start = random.randint(*start_range)
    step = random.randint(*step_range)

    if sample_space_scale is None:
        factor = 1
    else:
        factor = sample_space_scale

    if space == 'arithmetic':
        series = [start + (i * step) for i in range(cardinality * factor)]
    elif space == 'geometric':
        series = [start * (step**i) for i in range(cardinality * factor)]
    
    if sample_space_scale is None:
        return series
    else:
        return [series[random.randrange(0, cardinality * factor)] for _ in range(cardinality)]


def run_cardinality_tests(space='arithmetic', repeats=1000, top_power=10):
    """Runs repeated tests on a series of doubling cardinality values.
    
    A new progression is generated for each repeat, and all 3 splitting methods are compared.

    Args:
        space (str, optional): Whether to test 'arithmetic' or 'geometric' progressions.
                               Defaults to 'arithmetic'.
        repeats (int, optional): Number of repeats. Defaults to 1000.
        top_power (int, optional): Final value to use for the doubling progression (2**top_power).

    Returns:
        list[dicts]: A list of dictionaries of length 'repeats'.
                     Keys are the method names, plus 'cardinality'.
                     Values are the method absolute subset differences, plus cardinality
    """
    testing_results = []
    for cardinality in [2**n for n in range(top_power + 1)]:
        for _ in tqdm(range(repeats)):
            array = generate_random_array(cardinality=cardinality, space=space)
            searcher = ArraySearcher(array)
            query_val = searcher.get_random_array_item()
            results = searcher.compare_methods(query_val)
            results['cardinality'] = cardinality
            testing_results.append(results)

    return testing_results


def plot_cardinality_tests(results, title=None, figsize=(12, 9), facecolor='white', confidence_interval=95):
    """Generate a Seaborn plot of the results data.

    Args:
        results (list[dicts]): A list of results dictionaries - one dictionary per test run.
        title (str, optional): The plot title. Defaults to None.
        figsize (tuple, optional): The figure dimensions in inches. Defaults to (12, 9).
        facecolor (str, optional): The figure background colour. Defaults to 'white'.
        confidence_interval (int or str, optional): Confidence interval percent value to use in the plot.
                                                    Alternatively, if 'sd' the standard deviation will be shown.
                                                    Defaults to 95.

    Returns:
        matplotlib.figure.Figure: The figure.
    """
    # Make a dataframe from the list of dictionaries
    testing_df = pd.DataFrame(results)
    # Unpivot all columns not specified in the id_vars list
    tall_df = pd.melt(testing_df, id_vars=['cardinality'], var_name='method', value_name='iterations')
    # Make the plot
    fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)
    ax = sns.lineplot(data=tall_df, x='cardinality', y='iterations', hue='method', ci=confidence_interval)
    ax.set_xlabel('progression cardinality')
    ax.set_xscale('log', base=2)
    ax.set_ylabel('mean number of iterations')
    # Title
    if title:
        # Get repeats (just check the value for the first method/cardinality group)
        repeats = tall_df.groupby(['method', 'cardinality']).agg('size')[0]
        # Underscore assignment to supress Text object output
        _ = ax.set_title(f'{title} ({repeats} repeats)')
    return fig


def plot_progression_comparison(arithmetic_results, geometric_results, cardinality, title=None, figsize=(12, 9), facecolor='white'):
    # Make a dataframe from the list of dictionaries
    arithmetic_df = pd.DataFrame(arithmetic_results)
    arithmetic_df['space'] = ['arithmetic' for _ in range(len(arithmetic_df))]
    geometric_df = pd.DataFrame(geometric_results)
    geometric_df['space'] = ['geometric' for _ in range(len(geometric_df))]
    space_testing_df = pd.concat([arithmetic_df, geometric_df])
    space_testing_df = space_testing_df[space_testing_df.cardinality == cardinality]
    # Unpivot all columns not specified in the id_vars list
    tall_df = pd.melt(space_testing_df, id_vars=['space', 'cardinality'], var_name='method', value_name='iterations')
    # Make the plot
    fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)
    ax = sns.barplot(data=tall_df, x='space', y='iterations', hue='method')
    ax.set_xlabel('array space')
    ax.set_yscale('log', base=10)
    ax.set_ylabel('log(mean number of iterations)')
    # Title
    if title:
        # Underscore assignment to supress Text object output
        _ = ax.set_title(f'{title} (cardinality {cardinality})')
    return fig

def main():
    # SETUP
    # Pandas and seaborn options
    pd.set_option('display.max_rows', 10)
    sns.set_context('talk') 
    # Make sure we have a folder to write results to
    import os
    if not os.path.isdir('results'):
        os.mkdir('results')


    # WALKTHROUGH EXAMPLE
    # Input parameters
    CARDINALITY = 50
    SPACE = 'arithmetic'
    START_RANGE = (1, 10000)
    STEP_RANGE = (1, 10000)
    # Generate a random progression
    array = generate_random_array(cardinality=CARDINALITY, space=SPACE, start_range=START_RANGE, step_range=STEP_RANGE)
    print(array)
    # Make a searcher object
    searcher = ArraySearcher(array)
    query_val = searcher.get_random_array_item()
    print(query_val)
    # Compare the different search methods
    results = searcher.compare_methods(query_val, verbose=True)
    print(results)


    # ARITHMETIC SERIS TESTS
    # Run tests for arithmetic series of cardinalities 2**0 - 2**10 (1000 repeats)
    REPEATS = 1000
    SPACE = 'arithmetic'
    TOP_POWER = 10
    arithmetic_results = run_cardinality_tests(space=SPACE, repeats=REPEATS, top_power=TOP_POWER)
    # Export results as CSV
    arithmetic_df = pd.DataFrame(arithmetic_results)
    arithmetic_df.to_csv('results/arithmetic_results.csv')
    # Make seaborn plot
    fig = plot_cardinality_tests(arithmetic_results, title='Arithmetic comparison')
    fig.savefig('results/arithmetic_comparison.png')


    # GEOMETRIC SERIS TESTS
    # Run tests for geometric series of cardinalities 2**0 - 2**10 (1000 repeats)
    SPACE = 'geometric'
    geometric_results = run_cardinality_tests(space=SPACE, repeats=REPEATS, top_power=TOP_POWER)
    # Export results as CSV
    geometric_df = pd.DataFrame(geometric_results)
    geometric_df.to_csv('results/geometric_results.csv')
    # Make seaborn plot
    fig = plot_cardinality_tests(geometric_results, title='Arithmetic comparison')
    fig.savefig('results/geometric_comparison.png')


    # COMPARE ARITHMETIC AND GEOMETRIC PERFORMANCE
    # Input parameters
    CARDINALITY = 1024
    # Make seaborn plot
    fig = plot_progression_comparison(arithmetic_results=arithmetic_results,
                                      geometric_results=geometric_results,
                                      cardinality=CARDINALITY,
                                      title='Comparison of arithmetic vs geometric progressions')
    fig.savefig('results/progression_space_comparison.png')

if __name__ == '__main__':
    main()
