import pygame
from client import *
import time

pygame.init()
pygame.font.init()

WIDTH = 500
HEIGHT = 500
winTimer = 60

texts = []
buttons = []

sent = False

pick = "Waiting..."
opponent_pick = "Waiting..."
winner = ""

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.orignal_color = color
        self.hover = False
        self.hover_color = (128, 128, 0)

    def draw(self, win, outline=None):
        if self.hover: self.color = self.hover_color
        else: self.color = self.orignal_color
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y -
                             2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y,
                         self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render(self.text, False, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                     self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

font = pygame.font.SysFont("comicsans", 50)

rock_button = button((255, 0, 0), 30, 300, 125, 63, "Rock")
paper_button = button((0, 255, 0), 175, 300, 125, 63, "Paper")
scissors_button = button((0, 0, 255), 320, 300, 160, 63, "Scissors")

buttons = [rock_button, paper_button, scissors_button]

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Online Rock Paper Scissors")

def active_window():
    win.fill((255, 255, 255))
    texts = [(font.render("Your Pick", False, (255, 0, 0)), (50, 50)),
              (font.render("Opponent", False, (255, 0, 0)), (250, 50)),
              (font.render(str(pick), False, (0, 255, 0)), (50, 150)),
        (font.render(str(opponent_pick), False, (0, 255, 0)), (265, 150))]
    
    winnerText = (font.render(str(winner), False, (255, 140, 0)), (150, 200))

    if winner == "":
        for text in texts: win.blit(text[0], text[1])
        for button in buttons: button.draw(win)
    else: 
        win.fill((128, 128, 128))
        win.blit(winnerText[0], winnerText[1])
    pygame.display.flip()

def win_check():
    global winTimer
    global winner

    if winTimer <= 0:
        if pick == opponent_pick: winner = "Tie !"
        elif pick == "Rock" and opponent_pick == "Scissors": winner = "You Won !"
        elif pick == "Scissors" and opponent_pick == "Paper": winner = "You Won !"
        elif pick == "Paper" and opponent_pick == "Rock": winner = "You Won !"
        else: winner = "You Lost !"
    
    else: winTimer -= 1

    # font = pygame.font.SysFont("comicsans", 50)
    

main_run = True
clock = pygame.time.Clock()

c = client()

while main_run:
    clock.tick(60)
    active_window()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            main_run = False

        if event.type == pygame.MOUSEBUTTONDOWN and pick == "Waiting...":
            for button in buttons:
                if button.isOver(pygame.mouse.get_pos()): pick = button.text
        
        if event.type == pygame.MOUSEMOTION:
            for button in buttons:
                if button.isOver(pygame.mouse.get_pos()): button.hover = True
                else: button.hover  = False

    c.send("check")

    if pick != "Waiting..." and sent == False:
        c.send(pick)
        sent = True
    
    if c.recieved_message != "Message Recieved !":
        if len(c.recieved_message.split(",")) < 2:
            if pick == "Waiting...": opponent_pick = "Locked"
        else:
            picks = c.recieved_message.split(",")
            if picks[0] == picks[1]: opponent_pick = pick
            else:
                if picks[0] == pick: opponent_pick = picks[1]
                if picks[1] == pick: opponent_pick = picks[0]

    if pick != "Waiting..." and opponent_pick != "Waiting...": win_check()

c.send(c.DISCONNECT_MESSAGE)

