"""
Requirements:
pygame
tkinter
py-sudoku


"""
import pygame, sys
# from sudoku import Sudoku
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import random
import sudoku

new_game = sudoku.Sudoku(3)

# wrong_sudoc = "/Users/progressive/Desktop/Projects/sudoku/Sudoku game/sudoc.txt"
# correct_sudoc = "/Users/progressive/Desktop/Projects/sudoku/Sudoku game/correct_sudoc.txt"


# settings

WIDTH = 600
HEIGHT = 600


#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (96, 216, 232)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
ASH = (225, 225, 237)
ORANGE = (200, 100, 50)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
TRANS = (1, 1, 1)
LOCKEDCELLCOLOUR = (189, 189, 189)
INCORRECTCELLCOLOUR = (195, 121, 121)
PURPLE = (128,0,128)

#Boards

finished_board = []
reset_board = []
reset_board_2 = None
grid2 = []
di = None
#positions and sizes
grid_pos = (75, 100)
cell_size = 50
grid_size = cell_size*9
past_time = 0
slider_val = 0.1
current_diff = 0.1
confirm_state = "reject"
recent_text = ""

#app_class



running = True
window = pygame.display.set_mode((WIDTH, HEIGHT))
# grid = test_board

selected = None
mouse_pos = None
state = 'playing'
incorrect_cells = []
playing_buttons = []
locked_cells = []
finished = False
cell_changed = False
current_text = "Welcome"
current_time = "00:00:00"




 

    


def init():
    global font, slider_font
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Sophia's Sudoku")
    font = pygame.font.SysFont('Comic Sans MS', cell_size//1)
    slider_font = pygame.font.SysFont('Verdana', 10, bold=1)
    get_puzzle()
    load()
    run()
    

 
timer = pygame.time.Clock()
time = 0




def run():
    global current_time, time, current_text
    while running:
        if state == 'playing':
            playing_events()
            playing_update()
            playing_draw()
        ticks=pygame.time.get_ticks()
        ticks = ticks - past_time
        millis=ticks%1000
        seconds=int(ticks/1000 % 60)
        minutes=int(ticks/60000 % 60)
        hours = int(ticks/3600000 % 24)
        current_time=f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    pygame.quit()
    sys.exit()
    
    

###### PLAYING STATE FUNCTIONS ######
def playing_events():
    global slider_val, slider_maxi, slider_mini, slider_xpos, slider_ypos, slider_hit
    global slider_surf, slider_button_surf, slider_button_rect
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False

        #User Clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            select = mouse_on_grid()
            global selected
            if select: 
                selected = select

            else:
                selected = None
                if button_highlighted:
                    button_click()
                # if button2_highlighted:
                #     button2_click()
                # if button3_highlighted:
                #     button3_click()
                # if button4_highlighted:
                #     button4_click()
                if button5_highlighted:
                    button5_click()
                if button6_highlighted:
                    button6_click()
                if button7_highlighted:
                    button7_click()
                if button8_highlighted:
                    button8_click()
                if button9_highlighted:
                    button9_click()
                if button10_highlighted:
                    button10_click()
                if button11_highlighted:
                    button11_click()   
            pos = pygame.mouse.get_pos()
            if slider_button_rect.collidepoint(pos):
                slider_hit = True
        elif event.type == pygame.MOUSEBUTTONUP:
                slider_hit = False
            
        #User Types a key
        if event.type == pygame.KEYDOWN:
            if selected and selected not in locked_cells:
                if is_int(event.unicode):
                    grid2[selected[1]][selected[0]] = int(event.unicode)
                    global cell_changed
                    cell_changed = True
        if slider_hit:
            slider_move()


def playing_update():
    global mouse_pos
    mouse_pos = pygame.mouse.get_pos()
    button_update(mouse_pos)
    # button2_update(mouse_pos)
    # button3_update(mouse_pos)
    # button4_update(mouse_pos)
    button5_update(mouse_pos)
    button6_update(mouse_pos)
    button7_update(mouse_pos)
    button8_update(mouse_pos)
    button9_update(mouse_pos)
    button10_update(mouse_pos)
    button11_update(mouse_pos)

    if cell_changed:
        global incorrect_cells
        incorrect_cells = []
        if all_cells_done():
            #check if board correct
            check_all_cells()
            if len(incorrect_cells) == 0:
                global finished
                finished = True
            


def playing_draw():
    window.fill(WHITE)

    button_draw(window)
    # button2_draw(window)
    # button3_draw(window)
    # button4_draw(window)
    button5_draw(window)
    button6_draw(window)
    button7_draw(window)
    button8_draw(window)
    button9_draw(window)

    slider_draw(window)
    print_text(current_text, 100, 560)
    print_time(current_time)

    if confirm_state == "confirm":
        button10_draw(window)
        button11_draw(window)

    if selected:
        draw_selection(window, selected)

    shade_locked_cells(window, locked_cells)
    shade_incorrect_cells(window, incorrect_cells)

    draw_numbers(window)
    draw_grid(window)
    pygame.display.update()
    global cell_changed
    cell_changed = False



###### PLAYING STATE FUNCTIONS ######


###### BOARD CHECKING FUNCTIONS #####

def all_cells_done():
    global finished
    for row in grid2:
        for number in row:
            if number == None:
                finished = False
                return False
    finished =True
    return True 

def check_all_cells():
    global current_text
    # check_rows()
    # check_cols()
    # check_small_grid()
    real_checker()
    if incorrect_cells == []:
        current_text = 'Congratulations You solved it'
    else:
        current_text = f'Not Solved Yet, {len(incorrect_cells)} cells left'





###### BOARD CHECKING FUNCTIONS #####


###### HELPER FUNCTIONS ######

def draw_numbers(wind):
    for yidx, row in enumerate(grid2):
        for xidx, num in enumerate(row):
            if num:
                pos = [(xidx*cell_size)+grid_pos[0], (yidx*cell_size)+grid_pos[1]]
                text_to_screen(str(num), pos, wind)


def draw_selection(wind, pos):
    pygame.draw.rect(wind, LIGHTBLUE, ((pos[0]*cell_size)+grid_pos[0], (pos[1]*cell_size)+grid_pos[1], cell_size, cell_size))

def draw_grid(wind):
    pygame.draw.rect(wind, PURPLE, (grid_pos[0], grid_pos[1], WIDTH-150, HEIGHT-150), 4)
    for x in range(9):
        pygame.draw.line(wind, PURPLE if x%3 == 0 else BLACK, (grid_pos[0]+(x*cell_size), grid_pos[1]), (grid_pos[0]+(x*cell_size), grid_pos[1]+450), 4 if x%3 == 0 else 1)
        pygame.draw.line(wind, PURPLE if x%3 == 0 else BLACK, (grid_pos[0], grid_pos[1]+(x*cell_size)), (grid_pos[0]+450, grid_pos[1]+(x*cell_size)), 4 if x%3 == 0 else 1)

def mouse_on_grid():
    if mouse_pos[0] < grid_pos[0] or mouse_pos[1] < grid_pos[1]:
        return False 
    if mouse_pos[0] > grid_pos[0]+grid_size or mouse_pos[1] > grid_pos[1]+grid_size:
        return False
    return ((mouse_pos[0] - grid_pos[0])//cell_size, (mouse_pos[1]-grid_pos[1])//cell_size)

def slider_move():
    global slider_val, slider_maxi, slider_mini, slider_xpos, slider_ypos, slider_hit
    global slider_surf, slider_button_surf, current_diff
    """
    The dynamic part; reacts to movement of the slider button.
    """
    slider_val = (pygame.mouse.get_pos()[0] - slider_xpos - 10) / 180 * (slider_maxi - slider_mini) + slider_mini
    if slider_val < slider_mini:
        slider_val = slider_mini
    if slider_val > slider_maxi:
        slider_val = slider_maxi
    current_diff = slider_val

def button10_init(x, y, width, height, text= None, colour=(73,73,73), highlighted_colour = (189,189,189), function=None, params=None):
    global button10_image, button10_pos, button10_rect, button10_text, button10_colour, button10_highlighted_colour
    global button10_function, button10_params, button10_highlighted, button10_width, button10_height
    button10_image = pygame.Surface((width, height))
    button10_pos = (x,y)
    button10_rect = button10_image.get_rect()
    button10_rect.topleft = button10_pos
    button10_text = text
    button10_colour = colour
    button10_highlighted_colour = highlighted_colour
    button10_function = function
    button10_params = params
    button10_highlighted = False
    button10_width = width
    button10_height = height

def load_buttons():
    global slider_val, current_diff
    button_init(20, 50, WIDTH//8, 30, 
                function=check_all_cells,
                colour=(225, 225, 237),
                text='Check'
    )
    # button2_init(100, 50, WIDTH//8, 30, 
    #             function=get_puzzle,
    #             colour=(225, 225, 237),
    #             params=0.2,
    #             text='Easy'
    # )
    # button3_init(180, 50, WIDTH//8, 30, 
    #             function=get_puzzle,
    #             colour=(225, 225, 237),
    #             params=0.4,
    #             text='Medium'
    # )
    # button4_init(WIDTH//2-(WIDTH//7)//2, 50, WIDTH//8, 30, 
    #             function=get_puzzle,
    #             colour=(225, 225, 237),
    #             params=0.6,
    #             text='Hard'
    # )
    button5_init(340, 50, WIDTH//8, 30, 
                function=confirm,
                colour=(225, 225, 237),
                text='Start'
    )
    button6_init(420, 50, WIDTH//8, 30, 
                function=show_solution,
                colour=(225, 225, 237),
                text='Solution'
    )
    button7_init(500, 50, WIDTH//8, 30, 
                function=hint,
                colour=(225, 225, 237),
                text='Hint'
    )

    button8_init(200, 10, WIDTH//8, 30, 
                function=reset,
                colour=(225, 225, 237),
                text='Reset'
    )

    button9_init(400, 10, WIDTH//8, 30, 
                function=get_puzzle_from_file,
                colour=(225, 225, 237),
                text='Load File'
    )

    button10_init(420, 560, WIDTH//8, 30, 
                function=get_puzzle,
                colour=(225, 225, 237),
                text='Yes'
    )
    button11_init(500, 560, WIDTH//8, 30, 
                function=reject,
                colour=(225, 225, 237),
                text='No'
    )
    slider_init("shit", current_diff, 0.9, 0.1, 100)
def load():
    global locked_cells, incorrect_cells, finished
    load_buttons()
    locked_cells = []
    incorrect_cells = []
    finished = False


    #setting locked cells from original board
    for yidx, row in enumerate(grid2):
        for xidx, num in enumerate(row):
            if num:
                locked_cells.append((xidx, yidx))
  

def text_to_screen(text, pos, wind):
    global font
    text_font = font.render(text, False, BLACK)
    font_width = text_font.get_width()
    font_height = text_font.get_height()

    pos[0]+= (cell_size - font_width)//2
    pos[1]+= (cell_size - font_height)//2
    wind.blit(text_font, pos)

def shade_incorrect_cells(window, incorrect):
    for cell in incorrect:
        pygame.draw.rect(window, INCORRECTCELLCOLOUR, ((cell[0]*cell_size)+grid_pos[0], (cell[1]*cell_size)+grid_pos[1], cell_size, cell_size))

def shade_locked_cells(window, locked):
    for cell in locked:
        pygame.draw.rect(window, LOCKEDCELLCOLOUR, ((cell[0]*cell_size)+grid_pos[0], (cell[1]*cell_size)+grid_pos[1], cell_size, cell_size))


def is_int(string):
    try:
        int(string)
        return True
    except:
        return False

def get_puzzle():
    global grid2, finished_board, current_text, past_time, di, puzzle_file, confirm_state
    global recent_text, reset_board_2
    diff = round(current_diff, 1)
    print(diff)
    puzzle = new_game.difficulty(diff)
    di= diff
    finished_board = puzzle.solve().board
    reset_board_2 = puzzle._copy_board(puzzle.board)
    grid2 = []
    grid2 = puzzle.board
    current_text=f"New Puzzle: Difficulty: {diff}"
    recent_text = current_text
    puzzle_file = False
    past_time = pygame.time.get_ticks()
    confirm_state = "reject"
    load()

def confirm():
    global current_text, confirm_state
    print(reset_board_2)
    current_text="Are you sure you want to start a new game?"
    confirm_state = "confirm"

def reject():
    global confirm_state, current_text, recent_text
    confirm_state = "reject"
    current_text = recent_text




def reset(): 
    global grid2, reset_board, past_time, cell_changed, di
    if puzzle_file:
        grid2 = reset_board
    else:
        grid2 = []
        grid2 = reset_board_2
    past_time = pygame.time.get_ticks()
    load()



def get_puzzle_from_file():
    global grid2, finished_board, current_text, past_time, puzzle_file, reset_board

    Tk().withdraw() 
    filename = askopenfilename()

    with open(str(filename)) as f:
        lines = f.readlines()
    board = []
    for line in lines:
        row = []
        for number in range(9):
            value = int(line[number])
            if value != 0:
                row.append(value)
            else:
                row.append(None)
        board.append(row)
    puzzle = sudoku.Sudoku(3, 3, board=board)
    valid_board = False
    finished_board = puzzle.solve().board
    for x in range(9):
        for y in range(9):
            if finished_board[x][y] != None:
                valid_board = True
    
    if valid_board:
        grid2 = puzzle.board
        current_text="Puzzle Loaded Succesfully"
        puzzle_file = True
        reset_board = puzzle.board
        
    else:
        current_text="Invalid Puzzle"
        grid2 = finished_board

    past_time = pygame.time.get_ticks() 
    load()
    run()

def show_solution():
    global finished_board, grid2, finished
    grid2 = finished_board
    finished = True
    load()

def show_hint():
    global finished_board, grid2

    x = random.randint(0,8)
    y = random.randint(0,8)
    if (y, x) not in locked_cells:
        grid2[x][y] = finished_board[x][y] 
        locked_cells.append((y,x))  
    else:
        show_hint()
def hint():
    global incorrect_cells, current_text
    current_text = "New Hint"
    try:
        show_hint()

    except RecursionError:
        current_text = "Cell Filled Already"
    incorrect_cells = []
    


    


def real_checker():
    global incorrect_cells
    incorrect_cells = []
    for x in range(9):
        for y in range(9):
            if finished_board[x][y] != grid2[x][y]:
                incorrect_cells.append([y, x])
   
def print_text(text, x , y ):
    text_width = 300
    text_height = 30
    text_image = pygame.Surface((text_width, text_height))
    text_pos = (x, y)
    text_rect = text_image.get_rect()
    text_rect.topleft = text_pos
    
    text_image.fill((255,255,255))
    font = pygame.font.SysFont('arial', 13, bold=1)
    textt = font.render(text, False, (0,0,0))
    width, height = textt.get_size()

    x = (text_width-width)//2
    y = (text_height-height)//2
    text_image.blit(textt, (x, y))
    window.blit(text_image, text_pos)

def print_time(text):
    time_width = 70
    time_height = 30
    time_image = pygame.Surface((time_width, time_height))
    time_pos = (500, 10)
    time_rect = time_image.get_rect()
    time_rect.topleft = time_pos
    
    time_image.fill((255,255,255))
    font = pygame.font.SysFont('arial', 15, bold=1)
    textt = font.render(text, False, (0,0,0))
    width, height = textt.get_size()

    x = (time_width-width)//2
    y = (time_height-height)//2
    time_image.blit(textt, (x, y))
    window.blit(time_image, time_pos)

    

###### HELPER FUNCTIONS ######



###### BUTTON 1 ######
def button_init(x, y, width, height, text= None, colour=(73,73,73), highlighted_colour = (189,189,189), function=None, params=None):
    global button_image, button_pos, button_rect, button_text, button_colour, button_highlighted_colour
    global button_function, button_params, button_highlighted, button_width, button_height
    button_image = pygame.Surface((width, height))
    button_pos = (x,y)
    button_rect = button_image.get_rect()
    button_rect.topleft = button_pos
    button_text = text
    button_colour = colour
    button_highlighted_colour = highlighted_colour
    button_function = function
    button_params = params
    button_highlighted = False
    button_width = width
    button_height = height

def button_update(mouse):
    global button_highlighted
    if button_rect.collidepoint(mouse):
        button_highlighted = True
    else:
        button_highlighted = False

def button_draw(wind):
    global button_image
    button_image.fill(button_highlighted_colour if button_highlighted else button_colour)
    if button_text:
        button_draw_text(button_text)
    wind.blit(button_image, button_pos)

def button_click():
    if button_params:
        button_function(button_params)
    else:
        button_function()

def button_draw_text(text):
    global button_image
    font = pygame.font.SysFont('arial', 20, bold=1)
    text = font.render(text, False, (0,0,0))
    width, height = text.get_size()
    x = (button_width-width)//2
    y = (button_height-height)//2
    button_image.blit(text, (x, y))

    

##### BUTTON 1 ######



##### BUTTON 2 ######

def button2_init(x, y, width, height, text= None, colour=(73,73,73), highlighted_colour = (189,189,189), function=None, params=None):
    global button2_image, button2_pos, button2_rect, button2_text, button2_colour, button2_highlighted_colour
    global button2_function, button2_params, button2_highlighted, button2_width, button2_height
    button2_image = pygame.Surface((width, height))
    button2_pos = (x,y)
    button2_rect = button2_image.get_rect()
    button2_rect.topleft = button2_pos
    button2_text = text
    button2_colour = colour
    button2_highlighted_colour = highlighted_colour
    button2_function = function
    button2_params = params
    button2_highlighted = False
    button2_width = width
    button2_height = height

def button2_update(mouse):
    global button2_highlighted
    if button2_rect.collidepoint(mouse):
        button2_highlighted = True
    else:
        button2_highlighted = False

def button2_draw(wind):
    global button2_image
    button2_image.fill(button2_highlighted_colour if button2_highlighted else button2_colour)
    if button2_text:
        button2_draw_text(button2_text)
    wind.blit(button2_image, button2_pos)

def button2_click():
    if button2_params:
        button2_function(button2_params)
    else:
        button2_function()

def button2_draw_text(text):
    global button2_image
    font = pygame.font.SysFont('arial', 10, bold=1)
    text = font.render(text, False, (0,0,0))
    width, height = text.get_size()
    x = (button2_width-width)//2
    y = (button2_height-height)//2
    button2_image.blit(text, (x, y))
##### BUTTON 2 ######



##### BUTTON 3 ######


def button3_init(x, y, width, height, text= None, colour=(73,73,73), highlighted_colour = (189,189,189), function=None, params=None):
    global button3_image, button3_pos, button3_rect, button3_text, button3_colour, button3_highlighted_colour
    global button3_function, button3_params, button3_highlighted, button3_width, button3_height
    button3_image = pygame.Surface((width, height))
    button3_pos = (x,y)
    button3_rect = button3_image.get_rect()
    button3_rect.topleft = button3_pos
    button3_text = text
    button3_colour = colour
    button3_highlighted_colour = highlighted_colour
    button3_function = function
    button3_params = params
    button3_highlighted = False
    button3_width = width
    button3_height = height

def button3_update(mouse):
    global button3_highlighted
    if button3_rect.collidepoint(mouse):
        button3_highlighted = True
    else:
        button3_highlighted = False

def button3_draw(wind):
    global button3_image
    button3_image.fill(button3_highlighted_colour if button3_highlighted else button3_colour)
    if button3_text:
        button3_draw_text(button3_text)
    wind.blit(button3_image, button3_pos)

def button3_click():
    if button3_params:
        button3_function(button3_params)
    else:
        button3_function()

def button3_draw_text(text):
    global button3_image
    font = pygame.font.SysFont('arial', 10, bold=1)
    text = font.render(text, False, (0,0,0))
    width, height = text.get_size()
    x = (button3_width-width)//2
    y = (button3_height-height)//2
    button3_image.blit(text, (x, y))



##### BUTTON 3 ######



##### BUTTON 4 ######


def button4_init(x, y, width, height, text= None, colour=(73,73,73), highlighted_colour = (189,189,189), function=None, params=None):
    global button4_image, button4_pos, button4_rect, button4_text, button4_colour, button4_highlighted_colour
    global button4_function, button4_params, button4_highlighted, button4_width, button4_height
    button4_image = pygame.Surface((width, height))
    button4_pos = (x,y)
    button4_rect = button4_image.get_rect()
    button4_rect.topleft = button4_pos
    button4_text = text
    button4_colour = colour
    button4_highlighted_colour = highlighted_colour
    button4_function = function
    button4_params = params
    button4_highlighted = False
    button4_width = width
    button4_height = height

def button4_update(mouse):
    global button4_highlighted
    if button4_rect.collidepoint(mouse):
        button4_highlighted = True
    else:
        button4_highlighted = False

def button4_draw(wind):
    global button4_image
    button4_image.fill(button4_highlighted_colour if button4_highlighted else button4_colour)
    if button4_text:
        button4_draw_text(button4_text)
    wind.blit(button4_image, button4_pos)

def button4_click():
    if button4_params:
        button4_function(button4_params)
    else:
        button4_function()

def button4_draw_text(text):
    global button4_image
    font = pygame.font.SysFont('arial', 10, bold=1)
    text = font.render(text, False, (0,0,0))
    width, height = text.get_size()
    x = (button4_width-width)//2
    y = (button4_height-height)//2
    button4_image.blit(text, (x, y))


##### BUTTON 4 ######




##### BUTTON 5 ######


def button5_init(x, y, width, height, text= None, colour=(73,73,73), highlighted_colour = (189,189,189), function=None, params=None):
    global button5_image, button5_pos, button5_rect, button5_text, button5_colour, button5_highlighted_colour
    global button5_function, button5_params, button5_highlighted, button5_width, button5_height
    button5_image = pygame.Surface((width, height))
    button5_pos = (x,y)
    button5_rect = button5_image.get_rect()
    button5_rect.topleft = button5_pos
    button5_text = text
    button5_colour = colour
    button5_highlighted_colour = highlighted_colour
    button5_function = function
    button5_params = params
    button5_highlighted = False
    button5_width = width
    button5_height = height

def button5_update(mouse):
    global button5_highlighted
    if button5_rect.collidepoint(mouse):
        button5_highlighted = True
    else:
        button5_highlighted = False

def button5_draw(wind):
    global button5_image
    button5_image.fill(button5_highlighted_colour if button5_highlighted else button5_colour)
    if button5_text:
        button5_draw_text(button5_text)
    wind.blit(button5_image, button5_pos)

def button5_click():
    if button5_params:
        button5_function(button5_params)
    else:
        button5_function()

def button5_draw_text(text):
    global button5_image
    font = pygame.font.SysFont('arial', 10, bold=1)
    text = font.render(text, False, (0,0,0))
    width, height = text.get_size()
    x = (button5_width-width)//2
    y = (button5_height-height)//2
    button5_image.blit(text, (x, y))


##### BUTTON 5 ######

##### BUTTON 6 ######

def button6_init(x, y, width, height, text= None, colour=(73,73,73), highlighted_colour = (189,189,189), function=None, params=None):
    global button6_image, button6_pos, button6_rect, button6_text, button6_colour, button6_highlighted_colour
    global button6_function, button6_params, button6_highlighted, button6_width, button6_height
    button6_image = pygame.Surface((width, height))
    button6_pos = (x,y)
    button6_rect = button6_image.get_rect()
    button6_rect.topleft = button6_pos
    button6_text = text
    button6_colour = colour
    button6_highlighted_colour = highlighted_colour
    button6_function = function
    button6_params = params
    button6_highlighted = False
    button6_width = width
    button6_height = height

def button6_update(mouse):
    global button6_highlighted
    if button6_rect.collidepoint(mouse):
        button6_highlighted = True
    else:
        button6_highlighted = False

def button6_draw(wind):
    global button6_image
    button6_image.fill(button6_highlighted_colour if button6_highlighted else button6_colour)
    if button6_text:
        button6_draw_text(button6_text)
    wind.blit(button6_image, button6_pos)

def button6_click():
    if button6_params:
        button6_function(button6_params)
    else:
        button6_function()

def button6_draw_text(text):
    global button6_image
    font = pygame.font.SysFont('arial', 10, bold=1)
    text = font.render(text, False, (0,0,0))
    width, height = text.get_size()
    x = (button6_width-width)//2
    y = (button6_height-height)//2
    button6_image.blit(text, (x, y))


##### BUTTON 6 ######

##### BUTTON 7 ######

def button7_init(x, y, width, height, text= None, colour=(73,73,73), highlighted_colour = (189,189,189), function=None, params=None):
    global button7_image, button7_pos, button7_rect, button7_text, button7_colour, button7_highlighted_colour
    global button7_function, button7_params, button7_highlighted, button7_width, button7_height
    button7_image = pygame.Surface((width, height))
    button7_pos = (x,y)
    button7_rect = button7_image.get_rect()
    button7_rect.topleft = button7_pos
    button7_text = text
    button7_colour = colour
    button7_highlighted_colour = highlighted_colour
    button7_function = function
    button7_params = params
    button7_highlighted = False
    button7_width = width
    button7_height = height

def button7_update(mouse):
    global button7_highlighted
    if button7_rect.collidepoint(mouse):
        button7_highlighted = True
    else:
        button7_highlighted = False

def button7_draw(wind):
    global button7_image
    button7_image.fill(button7_highlighted_colour if button7_highlighted else button7_colour)
    if button7_text:
        button7_draw_text(button7_text)
    wind.blit(button7_image, button7_pos)

def button7_click():
    if button7_params:
        button7_function(button7_params)
    else:
        button7_function()

def button7_draw_text(text):
    global button7_image
    font = pygame.font.SysFont('arial', 10, bold=1)
    text = font.render(text, False, (0,0,0))
    width, height = text.get_size()
    x = (button7_width-width)//2
    y = (button7_height-height)//2
    button7_image.blit(text, (x, y))


##### BUTTON 7 ######

##### BUTTON 8 ######

def button8_init(x, y, width, height, text= None, colour=(73,73,73), highlighted_colour = (189,189,189), function=None, params=None):
    global button8_image, button8_pos, button8_rect, button8_text, button8_colour, button8_highlighted_colour
    global button8_function, button8_params, button8_highlighted, button8_width, button8_height
    button8_image = pygame.Surface((width, height))
    button8_pos = (x,y)
    button8_rect = button8_image.get_rect()
    button8_rect.topleft = button8_pos
    button8_text = text
    button8_colour = colour
    button8_highlighted_colour = highlighted_colour
    button8_function = function
    button8_params = params
    button8_highlighted = False
    button8_width = width
    button8_height = height

def button8_update(mouse):
    global button8_highlighted
    if button8_rect.collidepoint(mouse):
        button8_highlighted = True
    else:
        button8_highlighted = False

def button8_draw(wind):
    global button8_image
    button8_image.fill(button8_highlighted_colour if button8_highlighted else button8_colour)
    if button8_text:
        button8_draw_text(button8_text)
    wind.blit(button8_image, button8_pos)

def button8_click():
    if button8_params:
        button8_function(button8_params)
    else:
        button8_function()

def button8_draw_text(text):
    global button8_image
    font = pygame.font.SysFont('arial', 10, bold=1)
    text = font.render(text, False, (0,0,0))
    width, height = text.get_size()
    x = (button8_width-width)//2
    y = (button8_height-height)//2
    button8_image.blit(text, (x, y))



##### BUTTON 8 ######

##### BUTTON 9 ######

def button9_init(x, y, width, height, text= None, colour=(73,73,73), highlighted_colour = (189,189,189), function=None, params=None):
    global button9_image, button9_pos, button9_rect, button9_text, button9_colour, button9_highlighted_colour
    global button9_function, button9_params, button9_highlighted, button9_width, button9_height
    button9_image = pygame.Surface((width, height))
    button9_pos = (x,y)
    button9_rect = button9_image.get_rect()
    button9_rect.topleft = button9_pos
    button9_text = text
    button9_colour = colour
    button9_highlighted_colour = highlighted_colour
    button9_function = function
    button9_params = params
    button9_highlighted = False
    button9_width = width
    button9_height = height

def button9_update(mouse):
    global button9_highlighted
    if button9_rect.collidepoint(mouse):
        button9_highlighted = True
    else:
        button9_highlighted = False

def button9_draw(wind):
    global button9_image
    button9_image.fill(button9_highlighted_colour if button9_highlighted else button9_colour)
    if button9_text:
        button9_draw_text(button9_text)
    wind.blit(button9_image, button9_pos)

def button9_click():
    if button9_params:
        button9_function(button9_params)
    else:
        button9_function()

def button9_draw_text(text):
    global button9_image
    font = pygame.font.SysFont('arial', 10, bold=1)
    text = font.render(text, False, (0,0,0))
    width, height = text.get_size()
    x = (button9_width-width)//2
    y = (button9_height-height)//2
    button9_image.blit(text, (x, y))


##### BUTTON 9 ######



##### BUTTON 10 #####



def button10_update(mouse):
    global button10_highlighted
    if button10_rect.collidepoint(mouse):
        button10_highlighted = True
    else:
        button10_highlighted = False

def button10_draw(wind):
    global button10_image
    button10_image.fill(button10_highlighted_colour if button10_highlighted else button10_colour)
    if button10_text:
        button10_draw_text(button10_text)
    wind.blit(button10_image, button10_pos)

def button10_click():
    if button10_params:
        button10_function(button10_params)
    else:
        button10_function()

def button10_draw_text(text):
    global button10_image
    font = pygame.font.SysFont('arial', 10, bold=1)
    text = font.render(text, False, (0,0,0))
    width, height = text.get_size()
    x = (button10_width-width)//2
    y = (button10_height-height)//2
    button10_image.blit(text, (x, y))

##### BUTTON 10 #####




##### BUTTON 11 #####

def button11_init(x, y, width, height, text= None, colour=(73,73,73), highlighted_colour = (189,189,189), function=None, params=None):
    global button11_image, button11_pos, button11_rect, button11_text, button11_colour, button11_highlighted_colour
    global button11_function, button11_params, button11_highlighted, button11_width, button11_height
    button11_image = pygame.Surface((width, height))
    button11_pos = (x,y)
    button11_rect = button11_image.get_rect()
    button11_rect.topleft = button11_pos
    button11_text = text
    button11_colour = colour
    button11_highlighted_colour = highlighted_colour
    button11_function = function
    button11_params = params
    button11_highlighted = False
    button11_width = width
    button11_height = height

def button11_update(mouse):
    global button11_highlighted
    if button11_rect.collidepoint(mouse):
        button11_highlighted = True
    else:
        button11_highlighted = False

def button11_draw(wind):
    global button11_image
    button11_image.fill(button11_highlighted_colour if button11_highlighted else button11_colour)
    if button11_text:
        button11_draw_text(button11_text)
    wind.blit(button11_image, button11_pos)

def button11_click():
    if button11_params:
        button11_function(button11_params)
    else:
        button11_function()

def button11_draw_text(text):
    global button11_image
    font = pygame.font.SysFont('arial', 10, bold=1)
    text = font.render(text, False, (0,0,0))
    width, height = text.get_size()
    x = (button11_width-width)//2
    y = (button11_height-height)//2
    button11_image.blit(text, (x, y))

##### BUTTON 11 #####


##### SLIDER ########

def slider_init(name, val, maxi, mini, pos):

    global slider_val, slider_maxi, slider_mini, slider_xpos, slider_ypos, slider_hit
    global slider_surf, slider_button_surf, slider_font
    slider_val = val  # start value
    slider_maxi = maxi  # maximum at slider position right
    slider_mini = mini  # minimum at slider position left
    slider_xpos = pos  # x-location on screen
    slider_ypos = 45
    slider_surf = pygame.surface.Surface((200, 50))
    slider_hit = False  # the hit attribute indicates slider movement due to mouse interaction
    font = pygame.font.SysFont('Verdana', 10, bold=1)
    slider_txt_surf = font.render("Easy", False, BLACK)
    slider_txt_surf2 = font.render("Hard", False, BLACK)

    # Static graphics - slider background #
    slider_surf.fill(ASH)
    pygame.draw.rect(slider_surf, GREY, [0, 0, 200, 50], 3)
    # pygame.draw.rect(slider_surf, ORANGE, [10, 10, 180, 10], 0)
    pygame.draw.rect(slider_surf, WHITE, [10, 30, 180, 5], 0)

    slider_surf.blit(slider_txt_surf, (10, 10)) 
    slider_surf.blit(slider_txt_surf2, (160, 10)) # this surface never changes

    # dynamic graphics - button surface #
    slider_button_surf = pygame.surface.Surface((20, 20))
    slider_button_surf.fill(ASH)
    slider_button_surf.set_colorkey(ASH)
    pygame.draw.circle(slider_button_surf, WHITE, (10, 10), 6, 0)
    pygame.draw.circle(slider_button_surf, BLACK, (10, 10), 4, 0)

def slider_draw(window):
    global slider_val, slider_maxi, slider_mini, slider_xpos, slider_ypos, slider_hit
    global slider_surf, slider_button_surf, slider_button_rect
    """ Combination of static and dynamic graphics in a copy of
    the basic slide surface
    """
    # static
    surf = slider_surf.copy()

    # dynamic
    pos = (10+int((slider_val-slider_mini)/(slider_maxi-slider_mini)*180), 33)
    slider_button_rect = slider_button_surf.get_rect(center=pos)
    surf.blit(slider_button_surf, slider_button_rect)
    slider_button_rect.move_ip(slider_xpos, slider_ypos)  # move of button box to correct screen position

    # screen
    window.blit(surf, (slider_xpos, slider_ypos))


    


##### SLIDER #########


# MAIN 

if __name__ == "__main__":
    init()
