import os
import sys
import pygame
from generate import *

from colorama import init
from termcolor import colored
pygame.init()

#constant definitions
CELL_SIZE = 10
IMAGE_SCALE = 3
BOX_SIZE = CELL_SIZE * IMAGE_SCALE #size of a single qr cell
MARGIN = 8  #offset of the drawn part of the qr given in cells from the top right corner
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SUPPORT_FILE_NAME = 'code.png'
DATA = sys.argv[1]

#game definitions

code = generate_code(DATA) #generate the code
code.save(SUPPORT_FILE_NAME) #temporarily save the code
answer_size = (code.size[0] / CELL_SIZE) - 2*MARGIN
outer = generate_outer(SUPPORT_FILE_NAME)
answ = generate_answers(answwer_sheet=SUPPORT_FILE_NAME, offset=80) #generate the answer sheet
os.remove(SUPPORT_FILE_NAME)

user_answ = []
size = len(answ) #how many cells in the scene
for i in range(size):
    row = []
    for j in range(size):
        row.append(0)
    user_answ.append(row)
        
back = pygame.image.load('generated_outer.jpg')

width , height = back.get_size()
screen = pygame.display.set_mode((width, height))
game_name = pygame.display.set_caption("Solve the code")




def draw_scene(screen):
    global back
    screen.fill(WHITE)
    back = back.convert()

    #draw the outer part of the puzzle
    screen.blit(back,(0,0))
    for row in range(size):
        for col in range(size):
            #define the grid of the playable part
            rect = pygame.Rect((MARGIN + row)*BOX_SIZE,(MARGIN+col)*BOX_SIZE, BOX_SIZE, BOX_SIZE)
            #draw the grid
            pygame.draw.rect(screen, BLACK, rect, 1)

            #draw the cells that have been clicked
            if user_answ[row][col]:
                pygame.draw.rect(screen, BLACK, ((MARGIN + col) * BOX_SIZE, (MARGIN + row)*BOX_SIZE, BOX_SIZE, BOX_SIZE))

def validate_answer(answers, correct_answers):   
    #initialize the color thingy
    init()
    for i in range(len(answers)):
        if answers[i] == correct_answers[i]:
            msg = f'Line {i + 1} is {colored("correct", "green")}'
            print("-" * len(msg))
            print(msg)
            print("-" * len(msg))

def main():
    print(f"""
    Hello, welcome to the game!
    If you are reading this, most likely someone made a game for you using my software!
    I am glad and excited that someone gets to play they game. Here's some idea about the "gameplay":
        -I designed the game to check for answers by line, so it will show "Line x correct" whenver you get a line correct
        -The game will not tell you when all of the lines have been sovled, you need to scan and see for yourself. If it doesn't work there might be a problem with your answers or with the provided link given for the creation of the game
        -You can press the {colored('Left Ctrl', 'red')} button to get all the answers if you wish but that kinda ruins the fun, doesn't it? =))) ( also you can easily cheat on the game, I made it so that all the inner workings are in plain sight but again, in my opinion this take away from the fun of the game and if you really need to see the inner workings that is for good reason, maybe that's your thing, maybe you just want to cheat. Whatever it is, you are welcome to do it )

        That's it, have fun...or maybe star my {colored('Github','blue')} project if you will lol =))
        Have fun!
    """)

    print(f"The game has {colored(size, 'green')} lines to be solved")

    draw_scene(screen)
    stopped = False
    while not stopped:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stopped = True
            #get the location of the cell in terms of tiles where the mouse was clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                x = pos[1] // BOX_SIZE - MARGIN
                y = pos[0] // BOX_SIZE - MARGIN

                if ( x >= 0 and y >= 0 ) and ( x <= answer_size and y <= answer_size):
                    user_answ[x][y] = 0 if user_answ[x][y] else 1
                    validate_answer(user_answ, answ)
                    draw_scene(screen)
                else:
                    print("You have to select a cell within the grid")
            elif event.type == pygame.KEYDOWN:
                #press left ctrl to show all the answers
                if event.key == pygame.K_LCTRL:
                    for i,ans in enumerate(answ):
                        user_answ[i] = ans
                        draw_scene(screen)
                    
                
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
