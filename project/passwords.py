from engi1020.arduino.api import *
from random import choice, choices

class Passwords:
    def __init__(self, lcd_pins: list, btn_pins: list):
        self.btn_pins = btn_pins
        self.lcd_pins = lcd_pins

    def game_init(self):
        self.words = []
        self.letters = []

        self.generating_letters()

    def generating_letters(self):
        self.word = choice(self.words)
        
        self.letter_one = [self.word[0], i for i in choices(self.letters, 4)]
        self.letter_two = [self.word[1], i for i in choices(self.letters, 4)]
        self.letter_three=[self.word[2], i for i in choices(self.letters, 4)]
        self.letter_four =[self.word[3], i for i in choices(self.letters, 4)]
        self.letter_five =[self.word[4], i for i in choices(self.letters, 4)]

    def btn_press(self, letterx):
        
        letterx_1 = letterx[0]
        letterre = letterx[1:]
        letterre.append(letterx_1)

        return letterre
        
    def finish_cond(self):
        if digital_read(self.btn_pins[len(self.btn_pins)-1]):
            self.result = self.letter_one[0] + self.letter_two[0] + self.letter_three[0] + self.letter_four[0] + self.letter_five[0]
            if self.result == self.word:
                print("You Got It!")

            else:
                print("You Failed :(")

    def lcd_display(self):
        pass

    def game_loop(self):
        pass

