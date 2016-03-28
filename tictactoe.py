from copy import copy

empty_grid = [[' ', ' ', ' '], [' ',' ', ' '], [' ', ' ', ' ']]

def win_condition(grid):
    """checks the grid for a winner"""

    # go through each column and row
    for i in range(3):
        if grid[i][0] == grid[i][1] and grid[i][0] == grid[i][2] and grid[i][0] != ' ':
            return grid[i][0]
        if grid[0][i] == grid[1][i] and grid[0][i] == grid[2][i] and grid[0][i] != ' ':
            return grid[0][i]

    # go through the diagonals
    if grid[0][0] == grid[1][1] and grid[0][0] == grid[2][2] and grid[0][0] != ' ':
        return grid[0][0]
    elif grid[2][0] == grid[1][1] == grid[0][2] and grid[2][0] != ' ':
        return grid[2][0]
    else:
        return False

def complete_grid(grid):
    """determines if the grid is complete or not"""
    return not any(' ' in x for x in grid)

def print_grid(grid):
    """prints the tic tac toe grid into something presentable"""
    for i in range(3):
        print grid[i][0] + ' | ' + grid[i][1] + ' | ' + grid[i][2] 
        if i < 2:
            print '---------'


def tictactoe():
    """tic tac toe game"""
    # turn marker, use i modulo 2
    i = 0
    markers = ['X','O']
    the_grid = [[' ', ' ', ' '], [' ',' ', ' '], [' ', ' ', ' ']]

    # continue the game until someone wins or a tie
    while not (win_condition(the_grid) or complete_grid(the_grid)):
        turn = raw_input("It is %s's turn: " % str(markers[i%2]))
        try:
            x , y = [int(turn.split(' ')[0]), int(turn.split(' ')[1])]
        except (ValueError, IndexError):
            print "Invalid move. Please enter a valid coordinate."
            continue

        if x not in [0, 1, 2] or y not in [0, 1, 2]:
            print "Invalid move. Please enter a valid coordinate."""
            continue
        elif the_grid[x][y] in markers:
            print """Invalid move. Please select an empty coordinate."""
            continue
        else:
            the_grid[x][y] = copy(markers[i%2])
            i += 1
            print_grid(the_grid)

    # either a win or tie
    if win_condition(the_grid):
        print win_condition(the_grid) + " has won the game!"
    else:
        print "It's a tie!"

while True:
    tictactoe()
    decision = raw_input("Do you want to play again?").lower()
    if decision.lower() in ['n', 'no']:
        break
    else:
        continue

        
