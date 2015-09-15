import numpy
import random


# Checking rows and columns of a given grid.
def valid_rows_columns(grid):
    # Create a list to compare each row column with.
    list_of_numbers = set(range(0, 10))

    # Testing the rows of the grid.
    for i in range(9):
        row = list(grid[i, :])
        if any(row.count(x) > 1 for x in range(1, 10)) or not set(row).issubset(list_of_numbers):
            return False
    # Testing the columns of the grid.
    for j in range(9):
        column = list(grid[:, j].T)
        if any(column.count(x) > 1 for x in range(1, 10)) or not set(column).issubset(list_of_numbers):
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

    list_of_numbers = set(range(0, 10))
    # List containing 9 squares each is a also a list of size 9 with coordinate entries.

    squares = square_groupings()

    for i in range(9):
        y = list([grid[x[0], x[1]] for x in squares[i]])
        if any(y.count(x) > 1 for x in y) or not set(y).issubset(list_of_numbers):
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

    if list(grid[i]).count(grid[i][j]) > 1 or count_column > 1:
        return False
    else:
    	return True

def possible_values(grid,i,j):
    values = []
    for l in range(9):
        grid_copy = list(grid)
        grid_copy[i][j] = l+1
        if valid_entry(grid_copy,i,j):
            values.append(l+1)
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

test_grid = numpy.array([[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],
                         [1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],
                         [1,2,3,4,5,6,7,8,9]])

# Backtracking algorithm for solving a Sudoku.
def backtracking(grid):
    grid_copy = list(grid)
    empty_indices = []
    pv = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                empty_indices.append([i,j])
                pv.append(possible_values(grid,i,j))
                
    original_copy_pv = list(pv) 

    print pv

    current_index = 0
    while count_zeroes >= 1:
        values = pv[current_index]
        while values != []:
            i = empty_indices[current_index][0]
            j = empty_indices[current_index][1]
            grid[i][j] = values.pop([0])
            
            if valid_entry(grid,i,j):
                current_index += 1
                print_grid(grid)
                continue
            else:
                grid[i,j] = 0
        if values == []:
            pv[current_index] = list(original_copy_pv[current_index])
            current_index -= 1
            i_1 = empty_indices[current_index][0]
            j_1 = empty_indices[current_index][1]

            grid[i_1][j_1] = 0

    print_grid(grid)
    return grid

backtracking(sudoku)
# simulated_annealing(sudoku)