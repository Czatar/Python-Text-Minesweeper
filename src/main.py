import random as rnd

# Instantiates global variables.
displayed_board = []
hidden_board = []
win_condition = True

difficulty = "Intermediate"
num_rows, num_columns, num_mines = 13, 15, 50
symbols = {'covered': '\u2593', 'uncovered': '\u2591', 'flag': '\u2690',
           'mine': '\u263C', 'set mine': '\u2620', 'numbers': [1, 2, 3, 4, 5, 6, 7, 8]}


def get_valid_input(first, second, menu=False):
    """
    This function:
    Ensures that an input can be converted to an int and that it falls between a range.
    Or
    Ensures that the desired minesweeper input is valid.
    :param menu: If menu = True, the function refers to the main menu inputs. Otherwise, it refers to
    the minesweeper inputs.
    :param first: Enter a lower parameter to ensure the input is no less than lower.
    :param second: Enter an upper parameter to ensure the input is no greater than upper.
    :return: The desired adjusted number.
    """

    # If you're in the main menu, it restricts your input to lower and upper integer values.
    if menu:
        try:
            number = int(input("Enter a number from {} to {} inclusive: ".format(first, second)))
            if not (first <= number <= second):
                raise ValueError("Make sure your number ranges from {} to {}.".format(first, second))
        except ValueError as e:
            print(e, '\n')
            number = get_valid_input(first, second, True)
        return number

    # If you're in the game, it restricts your input to the correct input format.
    else:
        try:
            string = input("Input your move: ")
            print()
            # First makes sure the input isn't to exit to the main menu.
            if string == "exit":
                return False

            # Count the number of spaces
            num_spaces = 0
            for i in string:
                if i == " ":
                    num_spaces += 1

            # Checks to see if the input is in the correct format.
            if num_spaces not in [1, 2]:
                raise ValueError("Your input was invalid. Make sure it's in the format 'r c f' or 'r c'")
            elif num_spaces == 2 and string[-1] != "f":
                raise ValueError("Make sure that you place a flag with the lowercase letter 'f'")
            else:
                inputs = string.split(" ")
                for i in range(2):
                    inputs[i] = int(inputs[i])
                if inputs[-1] == 'f':
                    inputs[-1] = True
                else:
                    inputs.append(False)

            # Checks to see if the first two inputs are in the correct range.
            if not ((1 <= inputs[0] <= first) and (1 <= inputs[1] <= second)):
                raise ValueError("There are {} rows and {} columns. Enter positive integers.".format(first, second))

            inputs[0] -= 1
            inputs[1] -= 1

        # If any of the above doesn't work, it asks you for another input.
        except ValueError as e:
            print(e, '\n')
            print("If you are trying to exit, type 'exit'")
            inputs = get_valid_input(first, second)

        return inputs


def main_menu(option=0):
    """
    Prints the main menu options and asks the user what they would like to do.
    It reads rules and instructions, sets difficulty, starts a game, and quits.
    :param option: The default value is to let the user choose which option they want.
    :return: Nothing; it works by calling on itself unless the player wants to quit.
    """

    # Gets global variables.
    global difficulty, num_rows, num_columns, num_mines

    # Prints out your selections.
    if option == 0:
        print("-----------------------------")
        print("1: Read rules")
        print("2: Learn how inputs work")
        print("3: Options")
        print("4: Start game")
        print("5: Quit")
        print("What would you like to do?", end='   ')
        main_menu(get_valid_input(1, 5, True))

    # Prints out the game instructions.
    elif option == 1:
        print("----------------------------")
        print("\nHow to play Minesweeper:\n")
        print("     The objective of the game is to clear every space without setting off a mine.")
        print("Starting off with a fully covered board, your first move will not set off a mine.")
        print("For every move, you will either uncover an area of empty space or a number.\n")
        print("     This number represents the number of mines that are hidden in any of the 8 spaces around it.")
        print("You can place a flag where you think there is a mine. This helps you keep track of where the mines are.")
        print("You can only open a space or place a flag once per turn.")
        print("If a number has as many flags as it shows around it, you can chord it and clear the other empty spaces.")
        print("For more information, see #2.\n")
        main_menu()

    # Prints out how I wrote the game to work.
    elif option == 2:
        print("---------------------------")
        print("\nHow my version works:\n")
        print("     This text-based version is different than the point-and-click version you may be used to.")
        print("Each input will either be in the (row column) or (row column flag) format.")
        print("The three values should be separated by spaces, like so:")
        print("'3 4 f'")
        print("which places a flag at row 3 and column 4.")
        print("If you want to place a flag, the third character has to be 'f'.")
        print("Otherwise, the two values should be separated by a space, like so:")
        print("'5 7'")
        print("which opens up the space at row 5 and column 7.\n")
        print("To chord a number, input the row and column of the desired number.")
        print("     If at any point you wish to quit the game, your input should be 'exit'.")
        print("This will show the complete uncovered board and take you back to the main menu.\n")
        main_menu()

    # Changes difficulty.
    elif option == 3:
        print("-------------------------")
        print("\nCurrent difficulty: {}\n".format(difficulty))
        print("Select new difficulty:")
        print("1: Easy (9 x 9 grid with 10 mines)")
        print("2: Intermediate (13 x 15 grid with 40 mines")
        print("3: Expert (16 x 30 grid with 99 mines)")
        print("\nSelect a new difficulty.")

        new_difficulty = get_valid_input(1, 3, True)
        if new_difficulty == 1:
            difficulty = "Easy"
            num_rows, num_columns, num_mines = 9, 9, 10
        elif new_difficulty == 2:
            difficulty = "Intermediate"
            num_rows, num_columns, num_mines = 13, 15, 40
        else:
            difficulty = "Expert"
            num_rows, num_columns, num_mines = 16, 30, 99

        print("\nDifficulty set to {}.\n".format(difficulty))
        main_menu()

    # Starts a game.
    elif option == 4:
        print("---------------------------------")
        print("\nGood luck! Make a first move.\n")
        run_game(num_rows, num_columns, num_mines)

    # Quits and prints out credits.
    else:
        print("----------------------------")
        print("\nThank you for playing!")
        print("Original game created by Curt Johnson (1992) and recreated by me (2020).")


def print_board(board):
    """
    This function prints a given board along with the rows and columns on the sides.
    :param board: Takes in the board to print out.
    :return: Nothing; the function prints the board.
    """

    # Prints out the column numbers and spacers.
    print("   ", end='')

    for i in range(1, len(board[0]) + 1):
        if len(str(i)) == 1:
            print("0", end='')
        print(i, end=' ')

    print("\n   ", end='')
    for i in range(len(board[0])):
        print(" - ", end='')
    print()

    # Prints out the row number and the rows.
    for i in range(1, len(board) + 1):
        if len(str(i)) == 1:
            print("0", end='')
        print(str(i) + "| ", end='')
        for j in range(len(board[i - 1])):
            print(board[i - 1][j], end='  ')
        print("\n")


def create_new_board(r, c, m, unicodes, hidden=False, first_row=0, first_column=0):
    """
    This function is used to create both the standard display board and the hidden game board.
    :param r: The total number of rows in the desired board.
    :param c: The total number of columns in the desired board.
    :param m: The total number of mines in the desired board.
    :param unicodes: The dictionary of unicode characters.
    :param hidden: If the user wants to create a hidden board, they must specify this as True and fill in the rest.
    :param first_row: The user's first row input. The board creation will avoid placing a mine here.
    :param first_column: The user's first column input. The board creation will avoid placing a mine here.
    :return: The completed board ready for use.
    """

    # Creates the unicode characters
    covered = unicodes['covered']
    uncovered = unicodes['uncovered']
    mine = unicodes['mine']

    # Creates a new board of specified size.
    board = []

    for i in range(r):
        board.append([])
        for j in range(c):
            board[i].append(covered)

    # Creates the board used to play the game.
    if hidden:
        # Set mines
        # It temporarily places a mine where the first user input was and then removes it at the end.
        # This guarantees that there isn't a mine when the user inputs their first location.
        board[first_row][first_column] = mine
        for i in range(m):
            rand_row = rnd.randint(0, r - 1)
            rand_col = rnd.randint(0, c - 1)
            while board[rand_row][rand_col] != covered:
                rand_row = rnd.randint(0, r - 1)
                rand_col = rnd.randint(0, c - 1)

            board[rand_row][rand_col] = mine
        board[first_row][first_column] = covered

        # Set numbers
        for i in range(r):
            for j in range(c):
                if board[i][j] != mine:
                    adjacent_mines = count_adjacent_symbols(i, j, board, mine)
                    if adjacent_mines:
                        board[i][j] = adjacent_mines
                    else:
                        board[i][j] = uncovered
                        pass

    return board


def count_adjacent_symbols(row, column, board, check_symbol, get_checks=False):
    """
    This function counts how many of a certain symbol are present around a given location.
    :param get_checks: If the user wants to get the check locations, it would return check list.
    :param row: The desired row position of the location.
    :param column: The desired column position of the location.
    :param board: The given board to check the location.
    :param check_symbol: Checks to see if the locations around the space are equal to this symbol.
    :return: The number of symbols around the given location on a given board or the check list.
    """

    # Starts with a set of locations to look through.
    count = 0
    check = [[row-1, column-1], [row-1, column], [row-1, column+1], [row, column-1],
             [row, column+1], [row+1, column-1], [row+1, column], [row+1, column+1]]

    # If the location is an edge case, remove the locations to check that would cause an error.
    if row == 0 and column == 0:
        check = check[4:]
        check.pop(1)
    elif row == 0 and column == num_columns - 1:
        check = check[3:7]
        check.pop(1)
    elif row == num_rows - 1 and column == 0:
        check = check[1:5]
        check.pop(2)
    elif row == num_rows - 1 and column == num_columns - 1:
        check = check[:4]
        check.pop(2)
    elif row == 0:
        check = check[3:]
    elif row == num_rows - 1:
        check = check[:5]
    elif column == 0:
        check.pop(0)
        check.pop(2)
        check.pop(3)
    elif column == num_columns - 1:
        check.pop(2)
        check.pop(3)
        check.pop(5)

    # Loops through the locations to check and increments the number of bombs.
    for i in check:
        if board[i[0]][i[1]] == check_symbol:
            count += 1

    # If the user wants checks, it returns that list. Otherwise, it returns a count.
    if not get_checks:
        return count
    else:
        return check


def run_game(rows, columns, mines):
    """
    Uses a while loop to continue running the game until the user wins, loses, or quits.
    This function calls other sub-functions to print and change both the hidden and displayed board.
    :param rows: The number of rows the current board has.
    :param columns: The number of columns the current board has.
    :param mines: The number of mines the current board has.
    :return: Nothing, it just runs the game.
    """

    global displayed_board
    global hidden_board

    displayed_board = []
    hidden_board = []

    # Takes in the first user inputs and makes sure the first uncovered space isn't a mine.
    displayed_board = create_new_board(rows, columns, mines, symbols)
    print_board(displayed_board)
    inputs = get_valid_input(rows, columns)

    # If the first user input is to exit, it skips the while loop.
    start = True
    # if statements interpret lists as True booleans.
    if not inputs:
        print("Quit to main menu.")
        start = False
    else:
        hidden_board = create_new_board(rows, columns, mines, symbols, True, inputs[0], inputs[1])

    # Continues running until it breaks
    while start:
        # Makes sure the user hasn't won or lost the game before continuing.
        # Otherwise, it prints the condition and breaks.
        action = which_input(inputs[0], inputs[1], inputs[2], symbols)

        if action == 'lose':
            print_board(hidden_board)
            print("Game over. You set off a mine!")
            break
        elif action == 'win':
            print_board(displayed_board)
            print("You cleared the board. Nice job!")
            break

        print_board(displayed_board)

        # Gets the input and makes sure the player doesn't want to exit.
        inputs = get_valid_input(rows, columns)
        if not inputs:
            print("Quit to main menu.")
            break

    main_menu()


def which_input(row, column, flag, unicodes):
    """
    This function checks the input's location on each board and decides what action to take.
    :param row: The user's row input.
    :param column: The user's column input.
    :param flag: Whether the user wants to place a flag or not.
    :param unicodes: The dictionary of game symbols.
    :return: The game's condition. Either 'lose' or 'win,' and 0 continues the game.
    """

    # Create variables for convenience
    h_location = hidden_board[row][column]
    d_location = displayed_board[row][column]
    global win_condition
    win_condition = True

    # If you are not placing a flag.
    if not flag:
        # If you set off a mine.
        if h_location == unicodes['mine'] and d_location in [unicodes['covered'], unicodes['flag']]:
            hidden_board[row][column] = unicodes['set mine']
            return 'lose'
        # If you select a number to chord it.
        elif d_location in unicodes['numbers']:
            chord(row, column, unicodes)
            if not win_condition:
                return 'lose'
        # If you are only uncovering space.
        elif d_location in [unicodes['covered'], unicodes['flag']]:
            open_space(row, column, unicodes)
            win_condition = False
        # If no spaces are covered, win_condition stays as True.
        for i in range(num_rows):
            for j in range(num_columns):
                if displayed_board[i][j] == unicodes['covered']:
                    win_condition = False

    # If you are placing a flag.
    else:
        if d_location in [unicodes['covered'], unicodes['flag']]:
            if displayed_board[row][column] == unicodes['flag']:
                displayed_board[row][column] = unicodes['covered']
            else:
                displayed_board[row][column] = unicodes['flag']
        win_condition = False

    # If win_condition is True, you won the game.
    if win_condition:
        return 'win'
    else:
        return 0


def chord(r, c, unicodes):
    """
    This function counts how many flags there are around a number. If the condition to chord is met,
    the remaining open spaces will open up around the number. However, if a mine isn't covered
    by a flag, the game is lost.
    :param r: The number's row location.
    :param c: The number's column location.
    :param unicodes: The dictionary of unicodes.
    :return: Nothing. It just sets spaces equal to the hidden board.
    """

    global win_condition

    # Counts the number of flags around a number
    num_flags = count_adjacent_symbols(r, c, displayed_board, unicodes['flag'])
    check = count_adjacent_symbols(r, c, displayed_board, unicodes['flag'], True)

    # If the chord condition is met, it chords.
    if displayed_board[r][c] == num_flags:
        for i in check:
            if hidden_board[i[0]][i[1]] == unicodes['mine'] and not (displayed_board[i[0]][i[1]] == unicodes['flag']):
                hidden_board[i[0]][i[1]] = unicodes['set mine']
                win_condition = False
            elif displayed_board[i[0]][i[1]] == unicodes['covered']:
                open_space(i[0], i[1], unicodes)


def open_space(r, c, unicodes):
    """
    This function makes a desired displayed board equal to the hidden board at that location.
    As long as the opened space ends up being a blank space, if will check all valid adjacent locations.
    :param r: The desired row location.
    :param c: The desired column location.
    :param unicodes: The list of unicodes.
    :return: Nothing, it just sets displayed board equal to hidden board at a location.
    """

    check = count_adjacent_symbols(r, c, displayed_board, unicodes['covered'], True)

    # First checks to see if the location is a number.
    if hidden_board[r][c] in unicodes['numbers']:
        displayed_board[r][c] = hidden_board[r][c]

    # Otherwise, if it isn't a flag, it calls on itself for the valid surrounding areas.
    elif hidden_board[r][c] == unicodes['uncovered'] and displayed_board[r][c] == unicodes['covered']:
        displayed_board[r][c] = unicodes['uncovered']
        for i in check:
            open_space(i[0], i[1], unicodes)


print("\nWelcome to my text-based version of minesweeper!\n")
print("It is recommended to drag this tab all the way up to play this game.\n")
wait_for_player = input("Input anything when ready: ")
main_menu()
