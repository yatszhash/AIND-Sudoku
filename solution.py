assignments = []

# add existing function
ROWS = 'ABCDEFGHI'
COLS = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    #add existing util functions

    return [s + t for s in A for t in B]

# module variables
boxes = cross(ROWS, COLS)
row_units = [cross(r, COLS) for r in ROWS]
column_units = [cross(ROWS, c) for c in COLS]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[row + col for row, col in zip(ROWS, COLS)], [row + col for row, col in zip(ROWS, reversed(COLS))]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.

       expanded to the naked Ns strategy (eg. triplets, quadruplet... septuplet)
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    for unit in unitlist:
        undetermined_boxes = list(filter(lambda x: len(values[x]) > 1, unit))

        if not undetermined_boxes:
            continue

        max_value_len_box = max(undetermined_boxes, key=lambda x: len(values[x]))
        max_value_len = len(values[max_value_len_box])

        undecided_num = len(undetermined_boxes)

        # it's impossible there are 8 possible values in a box and 9 possible values aren't informative.
        if max_value_len > 7:
            continue

        for n in range(max_value_len - 1, 1, -1):
            if undecided_num <= n:
                continue

            n_len_boxes = list(filter(lambda x: len(values[x]) == n, undetermined_boxes))

            if not n_len_boxes:
                continue

            first_value = values[n_len_boxes[0]]
            if len(n_len_boxes) == n and all(values[box] == first_value for box in n_len_boxes):
                boxes_larger = list(filter(lambda x: len(values[x]) > n, undetermined_boxes))

                for ch in first_value:
                    for box_larger in boxes_larger:
                        if ch in values[box_larger]:
                            values = assign_value(values, box_larger, values[box_larger].replace(ch, ''))

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    #added existing util functions
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in ROWS:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    # add existing function
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)

    return values

def reduce_puzzle(values):
    """
    reduce possible values with the eliminate strategy, use the only choice strategy and the naked twins strategy
    :param values:
    :return values:
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)

        # Use the naked twins strategy
        values = naked_twins(values)

        # Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    '''
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    :param values: The sudoku in dictionary form
    :return: values: searched sudoku in dictionary form. If
    '''

    reduced = reduce_puzzle(values)

    if not reduced:
        return reduced

    if all(len(reduced[box]) == 1 for box in reduced):
        return values

    fewest = min(filter(lambda x: len(x[1]) > 1, reduced.items()), key=lambda x: len(x[1]))

    for possible in fewest[1]:
        tentative_values = values.copy()
        tentative_values[fewest[0]] = possible

        attempt = search(tentative_values)

        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)

    if values:
        return values
    return False

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
