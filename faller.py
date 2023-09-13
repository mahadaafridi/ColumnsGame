import gamerules as gamerules

def _user_input_rows() -> int:
    '''
    User input for rows.
    '''
    user_input = input('')
    user_input = int(user_input)
    return user_input

def _user_input_columns() -> int:
    '''
    User input for columns
    '''
    user_input = input('')
    user_input = int(user_input)
    return user_input

def _user_input_setup() -> str:
    '''
    Asks for the users input for the setup which is either 
    "EMPTY" or "CONTENTS"
    '''
    user_input = input('')
    return user_input

def _user_input_contents_setup() -> list[str]:
    '''
    This is for the users inputs for what contents they want to input on the board to begin with
    This will ask for an input and split each character of the users input individually in a list.
    '''
    char_list = []
    user_input = input('')
    for char in user_input:
        char_list.append(char)
    return char_list

def _user_input_move() -> list[str]:
    '''
    Asks for the users input for what move they want to make
    '''
    user_input = input('')
    return user_input

def _contents_rows_by_columns_setup(rows: int) -> list[list[str]]:
    '''
    This takes the users inputs that they want to have on the board into a 2D list
    This list is in rows by columns and is returned.
    '''
    rows_by_columns_board = []
    for num in range(rows):
        rows_by_columns_board.append(_user_input_contents_setup())
    return rows_by_columns_board

def _print_board(game_state : gamerules.GameState) -> None:
    '''
    Prints the board given the gamestate
    '''
    rows = game_state.num_rows()
    columns = game_state.num_columns()
    board = game_state.return_boardstate()

    for row in range(0, rows):
        print('|', end = '')
        for column in range(0, columns):
                if board[column][row][0] == 'BLANK CELL':
                    str = (f' {board[column][row][1]} ')
                    print(str, end = '')    
                elif board[column][row][0] == 'FILLED CELL':
                    str = (f' {board[column][row][1]} ')
                    print(str, end = '')
                elif board[column][row][0] == 'MATCHED':
                    str = (f'*{board[column][row][1]}*')
                    print(str, end = '')
                elif board[column][row][0] == 'FALLING CELL':
                    str = (f'[{board[column][row][1]}]')
                    print(str, end = '')
                elif board[column][row][0] == 'LANDED CELL':
                    str = (f'|{board[column][row][1]}|')
                    print(str, end = '')
                
        print('|', end = '')
        print('')
    print(' ', end='')
    for column in range(0, columns * 3):
        print('-', end ='')
    print(' ', end='')
    print()
    
def _all_matches(game_state: gamerules.GameState) -> None:
    '''
    Combines all the match functions from GameState.
    '''
    game_state.match_diagonal_down_right()
    game_state.match_diagonal_up_right()
    game_state.match_vert()
    game_state.match_horizontal()  

def _board_setup(rows: int, columns: int, setup: str) -> gamerules.GameState:
    '''
    Sets up the initial board depending on the users inputs. It creates the board and 
    returns the gamestate
    '''
    gamestate = gamerules.GameState(rows, columns)
    if setup == 'EMPTY':
        gamestate.create_empty_field()
    elif setup == 'CONTENTS':
        board = _contents_rows_by_columns_setup(rows)
        gamestate.create_contents_field(board)
    
    gamestate.gravity()
    _all_matches(gamestate)  
    _print_board(gamestate)
    return (gamestate)

def _time(gamestate: gamerules.GameState, num_cells_in_faller : int, faller_row: int) -> tuple[int, int]:
    '''
    Given how many fallers there are and the row the faller is on it passes the time on the board.
    If the board has matched pieces, it will make the matched pieces go away and replace them with empty pieces.
    If there is a faller it will make the faller go down a row. Also if the faller is in landed state, it will make it
    into frozen state. Also if the faller can't fall down it will end the game. 

    It then returns the number of cells of the faller that are on the board and what row the faller is on as a tuple.
    '''
    
    #makes the matches pieces into empty pieces
    if gamestate.has_matched_pieces():

        gamestate.matches_to_empty()
        gamestate.gravity()

    #if the faller can go down it will go down
    if gamestate.can_apply_faller_gravity():

        num_cells_in_faller += 1
        faller_row += 1
        gamestate.apply_faller_gravity()
        gamestate.already_moved_cell_to_falling()
        #if all the faller pieces aren't on the board, it will drop the next piece
        if num_cells_in_faller < 3:
            gamestate.place_faller(num_cells_in_faller)
        if not gamestate.can_apply_faller_gravity():    

            gamestate.falling_to_landed()  
        _print_board(gamestate)
    
    #if there are landed pieces, it will put them into the frozen state
    elif gamestate.has_landed_pieces():

        gamestate.landed_pieces_to_filled()
        if not gamestate.active_faller():
            _all_matches(gamestate)
                    


        _print_board(gamestate)
        #if the faller can't go down, it will end the game
        if num_cells_in_faller < 2:
            print('GAME OVER')
            _end_program() 
    else:
        gamestate.falling_to_landed()
        _print_board(gamestate)  
    return num_cells_in_faller, faller_row

def _faller_create(gamestate: gamerules.GameState, num_cells_in_faller : int, faller_row: int, user_move : str) -> tuple[int, int]:
    '''
    Creates the faller depending on the user input. If there is an active faller it will have no effect. If the faller is 
    attempted to be placed in a full column it will end the game. 
    It then returns the number of cells of the of the faller on the board and the row the faller is on as a tuple.
    '''

    if not gamestate.active_faller():
        num_cells_in_faller = 0
        faller_row = 0
        gamestate.create_faller(user_move)
        if gamestate.can_place_faller():
            gamestate.place_faller(num_cells_in_faller)
            _print_board(gamestate)
        else:
            pass
            print('GAME OVER')
            _end_program()
    #if there is an active faller, this will do nothing
    else:
        pass
    return num_cells_in_faller, faller_row

def _move_right(gamestate: gamerules.GameState) -> None:
    '''
    Moves the faller right. If there is no active faller or the faller can't be moved right this does nothing. 
    If the faller is moved from from being on top of a filled cell to an being on top of an empty cell it will change 
    the state of the faller from landed to falling. It also does the vise versa. 
    '''

    if gamestate.active_faller():
        #checks if the faller is in landed state or falling state
        has_landed_pieces = gamestate.has_landed_pieces()    
        #checks if the faller can be moved to the right  
        if gamestate.can_move_faller_right():
            gamestate.move_faller_right()
            #if there is empty space under the faller, it will be changed into falling state
            if gamestate.can_apply_faller_gravity():
                gamestate.already_moved_cell_to_falling()
                gamestate.landed_pieces_to_falling()
                
            else:
                if has_landed_pieces:
                    gamestate.already_moved_cell_to_landed()
                else:
                    gamestate.already_moved_cell_to_falling()
                
            _print_board(gamestate)
        else:
            _print_board(gamestate)
    else:
        _print_board(gamestate)

def _move_left(gamestate: gamerules.GameState) -> None:
    '''
    Moves the faller left. If there is no active faller or the faller can't be moved right this does nothing. 
    If the faller is moved from from being on top of a filled cell to an being on top of an empty cell it will change 
    the state of the faller from landed to falling. It also does the vise versa. 
    '''
    if gamestate.active_faller():
        #checks if the faller is in landed state or falling state
        has_landed_pieces = gamestate.has_landed_pieces()
        #checks if the faller can be moved to the left
        if gamestate.can_move_faller_left():
            gamestate.move_faller_left()
            #if there is empty space under the faller, it will be changed into falling state
            if gamestate.can_apply_faller_gravity():
                gamestate.already_moved_cell_to_falling()
                gamestate.landed_pieces_to_falling()
            else:
                if has_landed_pieces:
                    gamestate.already_moved_cell_to_landed()
                else:
                    gamestate.already_moved_cell_to_falling()
            _print_board(gamestate)
        else:
            _print_board(gamestate)
            
    else:
        _print_board(gamestate)

def _rotate(gamestate: gamerules.GameState) -> None:
    '''
    This rotates the faller. It also changes what is displayed on the board according to the
    faller that rotated. If there is no faller it does nothing.
    '''
    #checks if there is a faller
    if gamestate.active_faller():
        #rotates the faller
        gamestate.rotate_cell()
        gamestate.rotate_place_faller()
        #depending on what is underneath it it will be in landed or falling state
        if not gamestate.can_apply_faller_gravity():
            gamestate.falling_to_landed()

        _print_board(gamestate)
    else:
        _print_board(gamestate)

def _end_program() -> None:
    '''
    Ends the program
    '''
    exit()

def run():
    '''
    Runs the program. Asks for the initial user input. It then continues to loop and ask for user moves
    until there is a game over or the user quits with "Q"
    '''
    rows = _user_input_rows()
    columns = _user_input_columns()
    setup = _user_input_setup()
    gamestate = _board_setup(rows, columns, setup)

    num_cells_in_faller = 0
    faller_row = 0
    while True:
        
        user_move = _user_input_move()

        #depending on the users move, it will do the various outputs
        if user_move == '':
            num_cells_and_faller_row = _time(gamestate, num_cells_in_faller, faller_row)
            num_cells_in_faller = num_cells_and_faller_row[0]
            faller_row = num_cells_and_faller_row[1]
                        
        else:
            user_move = user_move.split()
            if user_move[0] == 'F':
                num_cells_and_faller_row = _faller_create(gamestate, num_cells_in_faller, faller_row, user_move)
                num_cells_in_faller = num_cells_and_faller_row[0]
                faller_row = num_cells_and_faller_row[1]

            if user_move[0] == 'Q':
                _end_program()

            if user_move[0] == '>':
                _move_right(gamestate)

            if user_move[0] == '<':
                _move_left(gamestate)

            if user_move[0] == 'R':
                _rotate(gamestate)

if __name__ == '__main__':
    run()
