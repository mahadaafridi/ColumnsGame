#has all the states for the cells
BLANK_CELL = 'BLANK CELL'
FILLED_CELL = 'FILLED CELL'
POSSIBLE_MATCH = 'POSSIBLE MATCH'
MATCHED = 'MATCHED'
FALLING_CELL = 'FALLING CELL'
ALREADY_MOVED_CELL = 'ALREADY MOVED CELL'
LANDED_CELL = 'LANDED CELL'

#Cell contents 
CELL_CONTENTS = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']
EMPTY = ' '

def sorter(piece_state_and_name):
    '''
    Creates the sorter for the gravity function
    '''
    return piece_state_and_name[0]

class GameState:
    def __init__(self, rows:int, columns: int):
        self._rows = rows
        self._columns = columns
        self._boardstate = []
        self._faller = Faller()
    
    def num_columns(self):
        '''
        Returns the num of columns
        '''
        return self._columns
    
    def num_rows(self):
        '''
        Returns the number of rows
        '''
        return self._rows 
    
    def return_boardstate(self) -> list:
        '''
        Returns the boardstate
        '''
        return self._boardstate

    def create_empty_field(self) -> list[list[tuple[str, str]]]:
        '''
        Creates an empty field then returns the board
        '''
        for col in range(self._columns):
            self._boardstate.append([])
            for row in range(self._rows):
                self._boardstate[-1].append((BLANK_CELL, EMPTY))

        return self._boardstate

    def create_contents_field(self, rows_by_columns_board: list[list[str]]) -> list[list[tuple[str, str]]]:
        '''
        Creates a field with contents in it based on its input. It then returns the boardstate
        '''
        for column in range(self.num_columns()):

            column_holder = []
            for row in range(self.num_rows()):
                if rows_by_columns_board[row][column] in CELL_CONTENTS:
                    column_holder.append((FILLED_CELL, rows_by_columns_board[row][column]))
                else:
                    column_holder.append((BLANK_CELL, EMPTY))
            self._boardstate.append(column_holder)

        return self._boardstate

    def gravity(self) -> 'None':
        '''
        This sorts the blank cells to the top of the column
        and pushes the filled cells to the bottom
        '''
        for column in self._boardstate:
            column.sort(key = sorter)
    
    def match_vert(self):
        '''
        Matches the pieces vertically. It does this by changing the piece state to possible match. If there are more
        than 3 possible matches in a row there will be a match.
        '''
        for column in self._boardstate:
            matches = 0
            for row in range(self.num_rows()):
                piece_name = column[row][1]
                piece_state = column[row][0]
                try:
                    next_piece_name = column[row + 1][1]
                except:
                    if matches < 2:
                        self._possible_matches_reset()
                        
                    else:
                        self._possible_matches_to_matches()
                    break
                if piece_state == FILLED_CELL or piece_state == POSSIBLE_MATCH:
                    
                    
                    if piece_name == next_piece_name:
                        column[row] = (POSSIBLE_MATCH, piece_name)
                        column[row + 1] = (POSSIBLE_MATCH, next_piece_name)
                        matches += 1
    
                    else:
                        if matches < 2:
                            self._possible_matches_reset()
                            matches = 0
                        else:
                            self._possible_matches_to_matches()

    def falling_to_landed(self):
        '''
        Changes the falling pieces to landed state
        '''
        for column in self._boardstate:
            for row in range(self.num_rows()):
                piece_state = column[row][0]
                piece_name = column[row][1]
                if piece_state == FALLING_CELL:
                    column[row] = (LANDED_CELL, piece_name)
        return self._boardstate

    def matches_to_empty(self):
        '''
        Changes the matched state pieces to empty state
        '''
        for column in self._boardstate:
            for row in range(self.num_rows()):
                piece_state = column[row][0]
                piece_name = column[row][1]
                if piece_state == MATCHED:
                    column[row] = (BLANK_CELL, EMPTY)
        return self._boardstate
    
    def active_faller(self) -> bool:
        '''
        Checks if there is an active faller in the board. Returns True if there is and False if there 
        isn't
        '''
        for column in self._boardstate:
                    for row in range(self.num_rows()):
                        piece_state = column[row][0]
                        if piece_state == FALLING_CELL or piece_state == LANDED_CELL:
                            return True
        return False

    def match_horizontal(self):
        '''
        Matches the pieces horizontally. It does this by changing the piece state to possible match. If there are more
        than 3 possible matches in a row there will be a match.'''
        board = self._boardstate

        for row in range(self.num_rows()):
            matches = 0

            for column in range(self.num_columns()):
                piece_name = board[column][row][1]
                piece_state = board[column][row][0]
                try:
                    next_piece_name = board[column + 1][row][1]
                    next_piece_state = board[column + 1][row][0]
                except:
                    if matches < 2:
                        self._possible_matches_reset()
                        
                    else:
                        self._possible_matches_to_matches()
                    break
                if piece_state == FILLED_CELL or piece_state == POSSIBLE_MATCH:
                    
                    
                    if piece_name == next_piece_name:
                        
                        board[column][row] = (POSSIBLE_MATCH, piece_name)
                        board[column + 1][row] = (POSSIBLE_MATCH, next_piece_name)
                        matches += 1
    
                    else:
                        if matches < 2:
                            self._possible_matches_reset()
                            matches = 0
                        else:
                            self._possible_matches_to_matches()
    
    def match_diagonal_down_right(self):
        '''
        Matches the pieces diagonally and down. It does this by changing the piece state to possible match. If there are more
        than 3 possible matches in a row there will be a match.
        '''
        board = self._boardstate
        
        for row in range(self.num_rows()):
            matches = 0

            for column in range(self.num_columns()):
                piece_name = board[column][row][1]
                piece_state = board[column][row][0]
                counter = 0
                while True:
                    try:
                        next_piece_name = board[column + counter + 1][row + counter + 1][1]
                        next_piece_state = board[column + counter + 1][row + counter + 1][0]
                    except:
                        if matches < 2:
                            self._possible_matches_reset()
                            
                        else:
                            self._possible_matches_to_matches()
                        matches = 0
                        break
                    if piece_state == FILLED_CELL or piece_state == POSSIBLE_MATCH:
                        
                        
                        if piece_name == next_piece_name:
                            
                            board[column + counter][row + counter] = (POSSIBLE_MATCH, piece_name)
                            board[column + counter + 1][row + counter + 1] = (POSSIBLE_MATCH, next_piece_name)
                            matches += 1
        
                        else:
                            if matches < 2:
                                self._possible_matches_reset()
                                matches = 0
                            else:
                                self._possible_matches_to_matches()
                            break
                    counter+=1

    def match_diagonal_up_right(self):
        '''
        Matches the pieces diagonally and up. It does this by changing the piece state to possible match. If there are more
        than 3 possible matches in a row there will be a match.
        '''
        board = self._boardstate
        row_counter = 0
        column_counter = 0
        for row in range(self.num_rows()):
            matches = 0

            for column in range(self.num_columns()):
                piece_name = board[column][row][1]
                piece_state = board[column][row][0]
                row_counter = 0
                column_counter = 0
                while True:
                    try:
                        next_piece_name = board[column + column_counter + 1][row + row_counter - 1][1]
                        next_piece_state = board[column + column_counter + 1][row + row_counter - 1][0]
                    except:
                        if matches < 2:
                            self._possible_matches_reset()
                            
                        else:
                            self._possible_matches_to_matches()
                        matches = 0
                        break
                    if piece_state == FILLED_CELL or piece_state == POSSIBLE_MATCH:
                        
                        
                        if piece_name == next_piece_name:
                            
                            board[column + column_counter][row + row_counter] = (POSSIBLE_MATCH, piece_name)
                            board[column + column_counter + 1][row + row_counter - 1] = (POSSIBLE_MATCH, next_piece_name)
                            matches += 1
        
                        else:
                            if matches < 2:
                                self._possible_matches_reset()
                                
                            else:
                                self._possible_matches_to_matches()
                            matches = 0
                            break
                    row_counter-=1
                    column_counter+=1

    def create_faller(self, user_faller : list[str, str, str]) -> None:
        '''
        Creates the faller based on the input and puts it into a list.
        '''
        self._faller.cells = []
        faller_column = user_faller[1]
        self._faller.set_column(faller_column)
        user_faller = user_faller[2:]

        for piece_name in user_faller:
            self._faller.cells.append((FALLING_CELL, piece_name))
        
    def can_place_faller(self) -> bool:
        '''
        Checks if the Faller can be placed down. Returns True if it can and False if it can't.
        '''
        faller_column = int(self._faller.current_column())
        if self._boardstate[faller_column - 1][0][0] == FILLED_CELL:
            return False
        else:
            return True
    
    def place_faller(self, faller_place : int) -> None:
        '''
        Places the faller in the board.
        '''
        faller_column = int(self._faller.current_column())
        self._boardstate[faller_column - 1][0] = self._faller.cells[2 - faller_place]
    
    def rotate_place_faller(self) -> None:
        '''
        This rotates the pieces on the board and changes the boardstate based on the rotation.
        '''
        counter = 0
        for column in self._boardstate:
            for row in range(self.num_rows(), -1, -1):
                piece_state = column[row - 1][0] 
                piece_name = column[row - 1][1]
                if piece_state == FALLING_CELL or piece_state == LANDED_CELL:
                    column[row - 1] = self._faller.cells[2 - counter]
                    counter += 1

    def can_apply_faller_gravity(self) -> bool:
        '''
        Checks if the faller can be moved down. Returns True if it can and False
        if it can't.
        '''
        for column in self._boardstate:
            for row in range(self.num_rows()):
                piece_state = column[row][0]
                piece_name = column[row][1]
                if piece_state == FALLING_CELL or piece_state == ALREADY_MOVED_CELL or piece_state == LANDED_CELL:
                    try:
                        if column[row + 1][0] == BLANK_CELL:
                            return True
                    except:
                        return False
        return False        

    def rotate_cell(self) -> None:
        '''
        Rotates the faller cell
        '''
        faller_cells = self._faller.cells
        self._faller.cells = [faller_cells[2], faller_cells[0], faller_cells[1]]
        
    def apply_faller_gravity(self) -> None:
        '''
        Moves the faller down on the boardstate.
        '''
        num_rows = self.num_rows()
        for column in self._boardstate:
            for row in range(num_rows):
                piece_state = column[num_rows - row - 1][0]
                piece_name = column[num_rows - row - 1][1]
                next_piece_state = column[num_rows - row - 2][0]
                next_piece_name = column[num_rows - row - 2][1]
                if next_piece_state == FALLING_CELL:
                    column[num_rows - row - 2] = (BLANK_CELL, EMPTY)
                    column[num_rows - row - 1] = (ALREADY_MOVED_CELL, next_piece_name)
    
    def has_landed_pieces(self) -> bool:
        '''
        Checks if there are any landed pieces on the board. If there are
        it will return True if not it will return False
        '''
        for column in self._boardstate:
            for row in range(self.num_rows()):
                piece_state = column[row][0]
                piece_name = column[row][1]
                if piece_state == LANDED_CELL:
                    return True
        return False

    def has_matched_pieces(self) -> bool:
        '''
        Checks if there are matches pieces on the board. Returns True if there are
        and False if ther aren't.
        '''
        for column in self._boardstate:
            for row in range(self.num_rows()):
                piece_state = column[row][0]
                piece_name = column[row][1]
                if piece_state == MATCHED:
                    return True
        return False

    def landed_pieces_to_filled(self) -> None:
        '''
        Makes the landed pieces to filled
        '''
        for column in self._boardstate:
            for row in range(self.num_rows()):
                piece_state = column[row][0]
                piece_name = column[row][1]
                if piece_state == LANDED_CELL:
                    column[row] = (FILLED_CELL, piece_name)

    def landed_pieces_to_falling(self) -> None:
        '''
        Makes the landed pieces to falling state
        '''
        for column in self._boardstate:
            for row in range(self.num_rows()):
                piece_state = column[row][0]
                piece_name = column[row][1]
                if piece_state == LANDED_CELL:
                    column[row] = (FALLING_CELL, piece_name)

        return self._boardstate
    
    def already_moved_cell_to_falling(self) -> None:
        '''
        Makes the already moved cells to falling state.
        '''
        for column in self._boardstate:
            for row in range(self.num_rows()):
                piece_state = column[row][0]
                piece_name = column[row][1]
                if piece_state == ALREADY_MOVED_CELL:
                    column[row] = (FALLING_CELL, piece_name)
        return self._boardstate        

    def already_moved_cell_to_landed(self) -> None:
        '''
        Changes the already moved cells state to landed state
        '''
        for column in self._boardstate:
            for row in range(self.num_rows()):
                piece_state = column[row][0]
                piece_name = column[row][1]
                if piece_state == ALREADY_MOVED_CELL:
                    column[row] = (LANDED_CELL, piece_name)
        return self._boardstate       

    def can_move_faller_right(self) -> bool:
        '''
        Checks if the faller can be moved right. If it can it returns True, if not
        it returns
        '''
        board = self._boardstate

        for row in range(self.num_rows()):

            for column in range(self.num_columns()):
                piece_name = board[column][row][1]
                piece_state = board[column][row][0]
                if piece_state == FALLING_CELL or piece_state == LANDED_CELL:
                    try:
                        next_piece_name = board[column + 1][row][1]
                        next_piece_state = board[column + 1][row][0]
                    except:
                        return False
                    
                    if not next_piece_state == BLANK_CELL:
                        return False     
        return True  

    def can_move_faller_left(self) -> bool:
            '''
            Checks if the faller can be moved left. If it can it returns True, if not it returns.
            '''
            board = self._boardstate

            if self._faller.current_column() == 1:
                return False

            for row in range(self.num_rows()):

                for column in range(self.num_columns()):
                    piece_name = board[column][row][1]
                    piece_state = board[column][row][0]
                    if piece_state == FALLING_CELL or piece_state == LANDED_CELL:
                        try:
                            next_piece_name = board[column - 1][row][1]
                            next_piece_state = board[column - 1][row][0]
                        except:
                            continue
                        
                        if not next_piece_state == BLANK_CELL:
                            return False     
            return True  
    
    def move_faller_left(self) -> None:
        '''
        This moves the faller to the left
        '''
    
        board = self._boardstate

        for row in range(self.num_rows()):

            for column in range(self.num_columns()):
                piece_name = board[column][row][1]
                piece_state = board[column][row][0]
                if piece_state == FALLING_CELL or piece_state == LANDED_CELL:
                    board[column - 1][row] = (ALREADY_MOVED_CELL, piece_name)
                    board[column][row] = (BLANK_CELL, EMPTY)
        self._faller.set_column(int(self._faller._column) - 1)
                      
    def move_faller_right(self) -> None:
        '''
        Checks if the faller can move to the right
        '''
        board = self._boardstate

        for row in range(self.num_rows()):

            for column in range(self.num_columns()):
                piece_name = board[column][row][1]
                piece_state = board[column][row][0]
                if piece_state == FALLING_CELL or piece_state == LANDED_CELL:
                    board[column + 1][row] = (ALREADY_MOVED_CELL, piece_name)
                    board[column][row] = (BLANK_CELL, EMPTY)
        self._faller.set_column(int(self._faller._column) + 1)
                      
    def end_game(self) -> None:
        '''
        Ends the game
        '''
        print('quit the program')

    def _possible_matches_reset(self):
        '''
        Changes the possible matches back to the filled cell state.
        '''
        for column in self._boardstate:
            for row in range(self.num_rows()):
                piece_state = column[row][0]
                piece_name = column[row][1]
                if piece_state == POSSIBLE_MATCH:
                    column[row] = (FILLED_CELL, piece_name)
        return self._boardstate

    def _possible_matches_to_matches(self):
        '''
        Changes the possible matches to the matched state.
        '''
        for column in self._boardstate:
            for row in range(self.num_rows()):
                piece_state = column[row][0]
                piece_name = column[row][1]
                if piece_state == POSSIBLE_MATCH:
                    column[row] = (MATCHED, piece_name)
        return self._boardstate

class Faller:
    def __init__(self):
        '''
        Initizlizes the faller class
        '''
        self.cells = []
        self._row = None
        self._column = None
    
    def set_column(self, column: int) -> None:
        '''
        Changes the column.
        '''
        self._column = column

    def set_row(self, row: int) -> None:
        '''
        Changes the row.
        '''
        self._row = row
    
    def current_row(self) -> int:
        '''
        Returns the current row.
        '''
        return self._row
    
    def current_column(self) -> int:
        '''
        Returns the column number.
        '''
        return self._column


