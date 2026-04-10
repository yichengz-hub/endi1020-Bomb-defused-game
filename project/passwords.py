from engi1020.arduino.api import *
from random import choice, choices, shuffle
from time import sleep
import asyncio

class Passwords:
    def __init__(self, cycle_btn, column_btn, submit_btn):
        self.cycle_btn = cycle_btn
        self.column_btn = column_btn
        self.submit_btn = submit_btn
        self.current_col = 0
        
        self.all_words = [

            "about", "after", "again", "below", "could",
            "every", "first", "found", "great", "house",
            "large", "learn", "never", "other", "place",
            "plant", "point", "right", "small", "sound",
            "spell", "still", "study", "their", "there",
            "these", "thing", "think", "three", "water",
            "where", "which", "world", "would", "write"
        ]

        self.start()


    def start(self):
        all_chars = "abcdefghijklmnopqrstuvwxyz"
        self.word = choice(self.all_words)
        redo = True
        
        while redo:
            columns = []
            for i in range(5):
                col = [self.word[i]] + choices(all_chars, k=5)
                shuffle(col)
                columns.append(col)

            # Check if any other word is possible, if it is, remake the random word and try again.
            redo = False
            for word in self.all_words:
                if word == self.word:
                    continue
                
                can_make = True
                for i in range(5):
                    if word[i] not in columns[i]:
                        can_make = False
                        break

                if can_make == True:
                    redo = True
                    break

        self.columns = columns


    def cycle_letter(self):
        col = self.columns[self.current_col]
        new_col = col[1:] + [col[0]]
        self.columns[self.current_col] = new_col


    def display_all(self): 
        assert self.current_col == 0, 'this is only used to initialize the game, the current column must be zero!'
        rgb_lcd_clear()
        display_word = "".join([col[0] for col in self.columns])
        rgb_lcd_print(display_word, row=0, col=0)
        rgb_lcd_print('^', row=1, col=0)


    def display_new_cursor(self):
        if self.current_col == 0:
            old_col = 4
        else:
            old_col = self.current_col - 1
        rgb_lcd_print(' ', row=1, col=old_col)
        rgb_lcd_print('^', row=1, col=self.current_col)


    def display_new_letter(self):
        col = self.columns[self.current_col]
        new_letter = col[0]
        rgb_lcd_print(new_letter, row=0, col=self.current_col)


    def check_guess(self):
        result = "".join([col[0] for col in self.columns])
        if result == self.word:
            rgb_lcd_clear()
            rgb_lcd_print("    DISARMED", row=0, col=0)
            return True
        else:
            rgb_lcd_clear()
            rgb_lcd_print("      BOOM", row=0, col=0)
            return False
        

    def finish_cond(self):
        self.result = "".join([col[0] for col in self.columns])

        if self.result == self.word:
            print("CORRECT! Bomb Disarmed.")
            rgb_lcd_clear()
            return "WIN"

        else:
            print(f"WRONG: {self.result.upper()} is not the password.")
            rgb_lcd_clear()
            return "LOSE"


    async def main(self):
        self.display_all()
        print(f'[DEBUG]: The answer is: {self.word}')
        
        while True:
            if digital_read(self.cycle_btn):
                self.cycle_letter()
                self.display_new_letter()
                while digital_read(self.cycle_btn): 
                    await asyncio.sleep(0.1)

            if digital_read(self.column_btn):
                if self.current_col == 4:
                    self.current_col = 0
                else:
                    self.current_col += 1
                self.display_new_cursor()
                while digital_read(self.column_btn):
                    await asyncio.sleep(0.1)

            if digital_read(self.submit_btn):
                result = self.finish_cond()
                while digital_read(self.submit_btn):
                    await asyncio.sleep(0.1)
 
                return result
            
            await asyncio.sleep(0.01)


if __name__ == '__main__':
    digital_write(4, False)
    digital_write(7, False)
    game = Passwords(8,9,10)
    sleep(1)
    game.main()
