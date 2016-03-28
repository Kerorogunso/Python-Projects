from __future__ import division
from collections import defaultdict
import numpy, random, copy


# Checking rows and columns of a given grid.
def valid_rows_columns(grid):
    # Testing the rows of the grid.
    for i in range(9):
        row = [x for x in grid[i] if x != 0]
        if len(set(row)) != len(row):
            return False 
    # Testing the columns of the grid.
    for j in range(9):
        column = [grid[i][j] for i in range(9) if grid[i][j] != 0]
        if len(set(column)) != len(column):
            return False
    return True


# Takes a sudoku grid and groups entries by the square they lie in.
def square_groupings():
    squares = []
    # List containing top left coordinate of each square.
    top_left = [[0, 0], [3, 0], [6, 0], [3, 0], [3, 3], [3, 6], [6, 0], [6, 3], [6, 6]]
    for coord in top_left:
        coordinates = []
        for i in range(3):
            for j in range(3):
                coordinates.append([coord[0]+i, coord[1]+j])
        squares.append(coordinates)

    return squares


# Checking if the 3x3 squares of a given grid is valid.
def valid_squares(grid):

    # List containing 9 squares each is a also a list of size 9 with coordinate entries.

    squares = square_groupings()

    for i in range(9):
        y = [grid[x[0]][x[1]] for x in squares[i] if grid[x[0]][x[1]] != 0]
        if len(set(y)) != len(y):
            return False

    return True


# Function testing whether or not a sudoku grid is valid.
def valid_grid(grid):
    if valid_rows_columns(grid) and valid_squares(grid):
        return True
    else:
        return False


# Function to quantify the amount of error in a sudoku grid.
def error(grid):

    total_error = 0
    squares = square_groupings()

    for i in range(9):
        row = list(grid[i, :])
        column = list(grid[:, i].T)
        square = squares[i]

        if any(row.count(x) > 1 for x in range(1, 10)):
            total_error += 1
        if any(column.count(x) > 1 for x in range(1, 10)):
            total_error += 1
        if any(square.count(x) > 1 for x in range(1, 10)):
            total_error += 1

    return total_error


# Temperature function for simulated annealing.
def temperature(num, k):
    return num * (0.99 ** k)


# Takes a grid and finds a random 'neighbour'. Crude start: swap two numbers in a grid.
def neighbour(grid, starting_grid):
    x_1 = random.randint(0, 8)
    x_2 = random.randint(0, 8)
    y_1 = random.randint(0, 8)
    y_2 = random.randint(0, 8)

    # Ensures that no two squares of the original sudoku are not switched.
    while starting_grid[x_1, x_2] != 0 or starting_grid[y_1, y_2] != 0 or [x_1, x_2] == [y_1, y_2] or valid_entry(grid, x_1, x_2) or valid_entry(grid, y_1, y_2):
        x_1 = random.randint(0, 8)
        x_2 = random.randint(0, 8)
        y_1 = random.randint(0, 8)
        y_2 = random.randint(0, 8)

    swapped_grid = numpy.copy(grid)
    swapped_grid[x_1, x_2] = int(grid[y_1, y_2])
    swapped_grid[y_1, y_2] = int(grid[x_1, x_2])

    return swapped_grid


# Acceptance probability function from the Metropolis-Hastings algorithm.
def acceptance_prob(error1, error2, temp):
    if error2 < error1:
        return 1
    else:
        return numpy.exp((error2 - error1)/temp)

# Counts the number of missing entries in the Sudoku grid.
def count_zeroes(grid):
    counter = sum(grid[k].count(0) for k in range(9))

    return counter

# Checks if the entry repeats has a duplicate in the column or row.
def valid_entry(grid,i,j):

    count_column = 0
    for k in range(9):
        if grid[k][j] == grid[i][j]:
            count_column += 1

    if grid[i].count(grid[i][j]) > 1 or count_column > 1:
        return False
    else:
    	return True

def possible_values(grid,i,j):
    values = []
    # find i0, the y coordinate of the top left of the square the referenced value lies in
    if i % 3 == 0:
        i0 = i
    elif i % 3 == 1:
        i0 = i - 1
    else:
        i0 = i - 2
    # find j0, the x coordinate of the top left of the square the referenced value lies in
    if j % 3 == 0:
        j0 = j
    elif j % 3 == 1:
        j0 = j - 1
    else:
        j0 = j - 2

    # existing values in that square
    values_in_square = [grid[i0 + k][j0 + l] for k in range (3) for l in range(3) if grid[i0 + k][j0 + l] != 0]

    
    # get all the non-zero values in the row/column.
    filled_already = set([grid[i][n] for n in range(9) if grid[i][n] != 0] + 
                         [grid[m][j] for m in range(9) if grid[m][j] != 0])
    values = [i+1 for i in range(9) if i+1 not in filled_already and (i+1) != grid[i][j] and (i + 1) not in values_in_square]

    return values

# Takes an incomplete sudoku grid and attempts to solve it via the method of simulated annealing.
def simulated_annealing(grid):
    # List of missing values to be added to the grid
    values = []
    grid = numpy.array(grid)
    start = numpy.copy(grid)
    for i in range(9):
        # Converting the sudoku grid into a list of lists.
        the_grid = list(grid)
        list_grid = [list(a) for a in the_grid]

        # Number of missing occurrences of i.
        count_i = 9 - sum([list_grid[k].count(i+1) for k in range(9)])

        # Form list of missing values.
        for j in range(count_i):
            values.append(i+1)

    # Fill in the grid with random numbers from the list of missing numbers.
    for i in range(9):
        for j in range(9):
            if grid[i, j] == 0:
                n = random.randint(0, len(values) - 1)
                grid[i, j] = values.pop(n)

    test = numpy.copy(grid)
    test_error = error(test)
    best = numpy.copy(test)
    best_error = error(best)

    n_max = int(1e5)
    for n in range(n_max):
        t = temperature(100 *(1 - (n * 1.0/n_max)),1)
        new = neighbour(test, start)
        new_error = int(error(new))

        # If the sudoku is correct, return it.
        if new_error == 0:
            return new

        if acceptance_prob(test_error, new_error, t) > numpy.random.uniform():
            test = numpy.copy(new)
            test_error = int(new_error)

        # New 'best' solution.
        if new_error < best_error:
            best = numpy.copy(new)
            print_grid(new)
            best_error = int(new_error)
            print("Current best error: %s" % best_error)

    return best


# Prints a sudoku grid.
def print_grid(grid):
    print "-"*19
    for i in range(9):
        row = grid[i]
        print "|" + " ".join((map(str,row[0:3]))) + "|" + " ".join((map(str,row[3:6]))) + "|" + " ".join((map(str,row[6:9]))) + "|"
        if (i+1)%3 == 0:
            print "-" * 19

sudoku = [[2, 7, 0, 0, 0, 1, 0, 0, 0], 
          [0, 0, 9, 0, 0, 0, 0, 5, 0],
          [5, 3, 0, 0, 7, 0, 0, 0, 0],
          [0, 8, 0, 0, 0, 0, 0, 0, 0], 
          [9, 0, 0, 2, 5, 0, 0, 0, 0], 
          [0, 0, 0, 0, 9, 3, 0, 0, 0],
          [3, 1, 0, 0, 0, 0, 0, 9, 8], 
          [7, 0, 8, 0, 0, 6, 0, 0, 0], 
          [0, 5, 0, 0, 0, 7, 0, 3, 0]]

medium_sudoku = [[6,0,0,0,0,0,0,1,5],
                 [0,0,5,7,0,0,0,3,0],
                 [0,2,0,0,0,8,7,0,0],
                 [2,0,0,0,4,0,6,5,0],
                 [0,0,6,9,8,0,0,0,4],
                 [0,0,0,0,0,6,0,8,0],
                 [0,0,3,0,0,1,0,0,9],
                 [0,6,2,0,0,0,0,0,0],
                 [0,0,0,8,2,9,0,0,0]]

hard_sudoku = [[8, 0, 5, 0, 0, 1, 0, 3, 0], 
               [0, 3, 0, 9, 0, 0, 0, 0, 0],
               [4, 0, 6, 0, 3, 0, 0, 0, 0],
               [6, 0, 0, 0, 1, 0, 9, 0, 0],
               [0, 5, 0, 3, 0, 8, 0, 7, 0], 
               [0, 0, 9, 0, 4, 0, 0, 0, 1], 
               [0, 0, 0, 0, 2, 0, 3, 0, 8],
               [0, 0, 0, 0, 0, 9, 0, 2, 0], 
               [0, 7, 0, 0, 0, 0, 5, 0, 4]]

def backtrack(grid):
    """solves sudoku via backtracing"""

    # create copy of grid, get all empty indices, get all their possible values
    grid_copy = copy.copy(grid)
    empty_indices = [[i, j] for i in range(9) for j in range(9) if grid[i][j] == 0]
    possibles = [possible_values(grid, x[0], x[1]) for x in empty_indices]

    # index for empty_indices
    current_index = 0
    values = possibles[current_index]

    # while grid is still incomplete
    while count_zeroes(grid_copy) > 0:
        x = empty_indices[current_index][0]
        y = empty_indices[current_index][1]
        # we have ran out of values, so need to backtrack
        if values == []:
            grid_copy[x][y] = 0
            current_index -= 1
            x = empty_indices[current_index][0]
            y = empty_indices[current_index][1]
            # set the previous value back to zero, and remove the value 
            grid[x][y] = 0
            values = possibles[current_index]

            continue

        # try a value
        grid_copy[x][y] = values.pop(0)

        # if its complete return the grid, if its valid move to next iteration
        # otherwise, set the value back to zero and try another value
        if valid_grid(grid_copy) and count_zeroes(grid_copy) == 0:
            return grid_copy
        elif valid_grid(grid_copy):
            current_index += 1
            x, y = empty_indices[current_index]
            possibles[current_index] = possible_values(grid_copy, x, y)
            values = possibles[current_index]
        else:
            grid_copy[x][y] = 0

#print_grid(backtrack(sudoku))
print_grid(backtrack(medium_sudoku))
# print_grid(backtrack(hard_sudoku))
