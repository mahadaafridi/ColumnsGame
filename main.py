import gamerules as gamerules
import random 
import pygame 

#The rows and columns for the game 
ROWS = 13
COLUMNS = 6

#initial witth and height of the game
_INITIAL_WIDTH = 600
_INITIAL_HEIGHT = 600

#the frame rate of the game 
_FRAME_RATE = 30

#the background color of the game 
_BACKGROUND_COLOR = (220, 220, 220)

def get_color(letter : str) -> tuple[int, int, int]:
    '''
    Gets the color of the cell based on the letter of it
    '''
    if letter == 'S':
        return (255, 0 , 0)
    if letter == 'T':
        return (255, 128, 0)
    if letter == 'V':
        return (255, 255, 0)
    if letter == 'W':
        return (0, 255, 0)
    if letter == 'X':
        return (0, 255, 255)
    if letter == 'Y':
        return (0, 0, 255)
    if letter == 'Z':
        return (127, 128, 255)

class ColumnsGame:
    def __init__(self):
        self._state = gamerules.GameState(ROWS, COLUMNS)
        self._state.create_empty_field()
        self.tik_rate = 0
        self._running = True
        self._faller_row = 0
        self._faller_num = 0
        self._column_list = [1, 2, 3, 4, 5, 6]

    def run(self) -> None:
        '''
        Runs the program. It continues to run until the game is quit or the game is over.
        '''
        pygame.init()

        try:
            clock = pygame.time.Clock()
            self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))
        
            while self._running:

                clock.tick(_FRAME_RATE)
                self.tik_rate += 1 
                self._handle_events()

                if self.tik_rate > _FRAME_RATE:
                    self._time()
                    self.tik_rate = 0

                self._draw_frame()
        finally:
            pygame.quit()

    def _create_surface(self, size: tuple[int, int]) -> None:
        '''
        Creates the surface for the program.
        '''
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)

    def _draw_game_outline(self) -> None:
        '''
        Draws the game outline.
        '''
        self._grid_outline()
    
    def _jewel_size(self) -> tuple[int, int]:
        '''
        Calculates the jewel size in the x direction and the y direction. Returns the jewels x size and the
        jewel y size as a tuple. 
        '''
        window_x, window_y = self._surface.get_size()
        jewel_x_size = window_x / 6
        jewel_y_size = window_y / 13
        return jewel_x_size, jewel_y_size

    def _grid_outline(self) -> None:
        '''
        Draws the grid and the cells inside of the game. This calculates the jewel size of the game. It also centers the grid so that
        it will always be in the center of the program. If the cell is matched, landed, filled, or empty it will display differently on 
        the board. 
        '''
        for row in range(self._state.num_rows()):

            for column in range(self._state.num_columns()):
                
                jewel_size = None

                jewel_x_size, jewel_y_size = self._jewel_size()
                
                #finds the jewel_size that should be used in the program
                if jewel_x_size > jewel_y_size:
                    jewel_size = jewel_y_size
                else:
                    jewel_size = jewel_x_size
                

                window_x, window_y = self._surface.get_size()

                #The center of the window
                center_x = window_x / 2
                center_y = window_y / 2

                #the locaiton where the grid should be drawn
                grid_starting_x = center_x - (jewel_size * 6) / 2
                grid_starting_y = center_y - (jewel_size * 13) / 2

                #the location where the specific cell should be drawn
                cell_x_coor = grid_starting_x + (column * jewel_size)
                cell_y_coor = grid_starting_y + (row * jewel_size)

                
                cell_rect = pygame.Rect(
                    cell_x_coor, cell_y_coor, 
                    jewel_size, jewel_size
                )

                cell_content = self._state._boardstate[column][row][1]
                cell_state = self._state._boardstate[column][row][0]
                
                #changes the border and the color of the cell based on the state of the cell or the contents of the cell
                color = (255, 255, 255)
                border = 1
                if cell_state == gamerules.MATCHED:
                    color = (255, 255, 255)
                    border = 0
                elif cell_state == gamerules.LANDED_CELL:
                    color = (0, 0, 0)
                    border = 0
                elif cell_content in gamerules.CELL_CONTENTS:
                    color = get_color(cell_content)
                    border = 0

                #draws the cells or the borders 
                pygame.draw.rect(self._surface, color, cell_rect, border)
                if border == 0:
                    pygame.draw.rect(self._surface, (0, 0, 0), cell_rect, 1)

    def _create_faller(self) -> None:
        '''
        This creates the faller and places it down. If the faller can't be placed because the column is filled
        it will be put into a different column. If all the columns are full, the game will end. 
        '''
        self._faller_num = 0
        self._faller_row = 0
        while True:
            
            if len(self._column_list) == 0:
                exit()

            column = str(random.choice(self._column_list))
            self._state.create_faller(['F', column , random.choice(gamerules.CELL_CONTENTS), 
            random.choice(gamerules.CELL_CONTENTS), random.choice(gamerules.CELL_CONTENTS)]
            )
            if self._state.can_place_faller():
                self._state.place_faller(self._faller_num)
                break
            else:
                self._column_list.remove(int(column))

    def _time(self) -> None:
        '''
        Function that shows what happens as time passes.
        If there are any matched pieces, they will go away and gravity will be applied. If there is no faller the faller
        will be created. If the faller can go down, it will. If the faller is in landed state, it will go to frozen state. Also if the faller
        doesn't go on the board because the column is filled the game will end. 
        '''

        #changes the matched pieces to to empty and applies gravity
        if self._state.has_matched_pieces():
            self._state.matches_to_empty()
            self._state.gravity()
            self._state.apply_faller_gravity()

        #if there is no faller it will create one
        if not self._state.active_faller():
            self._create_faller()
        
        #if the faller can go down this will occur
        elif self._state.can_apply_faller_gravity():

            self._faller_num += 1
            self._faller_row += 1
            self._state.apply_faller_gravity()
            self._state.already_moved_cell_to_falling()
            #places the faller pieces if all of them are not on the board yet
            if self._faller_num < 3:
                self._state.place_faller(self._faller_num)
            #if the faller can't go down anymore, the state will change to landed
            if not self._state.can_apply_faller_gravity():    
                self._state.falling_to_landed()  

        #if the faller is in landed state, the state will change to frozen and match
        elif self._state.has_landed_pieces():

            self._state.landed_pieces_to_filled()
            if not self._state.active_faller():
                self._state.match_diagonal_down_right()
                self._state.match_diagonal_up_right()
                self._state.match_vert()
                self._state.match_horizontal()     

        #ends the game if the faller can't go all the way on the board
        elif not self._state.can_apply_faller_gravity():
            if self._faller_num < 3:
                exit()
        
    def _handle_events(self) -> None:
        '''
        Handles the events in the program
        '''
        for event in pygame.event.get():
            self._handle_event(event)

    def _handle_event(self, event) -> None:
        '''
        Handles the events of exiting the program and pressing keys.
        If the right arrow is pressed, faller goes to the right. If the left arrow is 
        pressed, the faller goes to the left. If spacebar is pressed the faller will rotate.
        '''
        if event.type == pygame.QUIT:
            self._stop_running()
        elif event.type == pygame.VIDEORESIZE:
            self._create_surface(event.size)
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                self._move_faller_to_left()

            if event.key == pygame.K_RIGHT:
                self._move_faller_to_right()

            if event.key == pygame.K_SPACE:
                self._rotate_faller()     
  
    def _rotate_faller(self) -> None:
        '''
        Rotates the faller.
        '''
        self._state.rotate_cell()
        self._state.rotate_place_faller()    
        if not self._state.can_apply_faller_gravity():
            self._state.falling_to_landed()          

    def _move_faller_to_right(self) -> None:
        '''
        Moves the faller to the right. It is unable to move to the right, nothing will happen. If the faller
        is moved from a landed state and is moved over an empty space, the faller state will change to falling.
        '''
        has_landed_pieces = self._state.has_landed_pieces()    
        #checks if the faller can be moved to the right  
        if self._state.can_move_faller_right():
            self._state.move_faller_right()
            #if there is empty space under the faller, it will be changed into falling state
            if self._state.can_apply_faller_gravity():
                self._state.already_moved_cell_to_falling()
                self._state.landed_pieces_to_falling()
                
            else:
                if has_landed_pieces:
                    self._state.already_moved_cell_to_landed()
                else:
                    self._state.already_moved_cell_to_falling()        

    def _move_faller_to_left(self) -> None:
        '''
        Moves the faller to the left. It is unable to move to the left, nothing will happen. If the faller
        is moved from a landed state and is moved over an empty space, the faller state will change to falling.
        '''
        has_landed_pieces = self._state.has_landed_pieces()
        #checks if the faller can be moved to the left
        if self._state.can_move_faller_left():
            self._state.move_faller_left()
            #if there is empty space under the faller, it will be changed into falling state
            if self._state.can_apply_faller_gravity():
                self._state.already_moved_cell_to_falling()
                self._state.landed_pieces_to_falling()
            else:
                if has_landed_pieces:
                    self._state.already_moved_cell_to_landed()
                else:
                    self._state.already_moved_cell_to_falling()

    def _stop_running(self) -> None:
        '''
        Stops the program from running.
        '''
        self._running = False

    def _draw_frame(self) -> None:
        '''
        Draws the surface and flips it over so the user can see.
        '''
        self._surface.fill(_BACKGROUND_COLOR)
        self._draw_game_outline()

        pygame.display.flip()

if __name__ == '__main__':
    ColumnsGame().run()
