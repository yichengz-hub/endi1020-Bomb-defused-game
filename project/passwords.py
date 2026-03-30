from engi1020.arduino.api import *
from random import choice, choices, shuffle
import time

class Passwords:
    def __init__(self, btn_pins: list):
        # btn_pins should be [CycleLetter, SelectColumn, Submit]
        self.btn_pins = btn_pins
        self.current_column = 0
        
        # All valid words from the manual image
        self.all_words = [
            "about", "after", "again", "below", "could",
            "every", "first", "found", "great", "house",
            "large", "learn", "never", "other", "place",
            "plant", "point", "right", "small", "sound",
            "spell", "still", "study", "their", "there",
            "these", "thing", "think", "three", "water",
            "where", "which", "world", "would", "write"
        ]
        self.game_init()

    def game_init(self):
        # Pick the secret answer
        self.word = choice(self.all_words)
        
        # Generate the 5 lists of 6 letters each
        # We ensure the correct letter is at index 0 initially
        self.columns = []
        all_chars = "abcdefghijklmnopqrstuvwxyz"
        
        for i in range(5):
            col = [self.word[i]] + choices(all_chars, k=5)
            shuffle(col) # Shuffle so the answer isn't always at the start
            self.columns.append(col)

    def cycle_letter(self):
        # Rotate the list for the currently selected column
        col = self.columns[self.current_column]
        # Move first element to the end
        self.columns[self.current_column] = col[1:] + [col[0]]

    def lcd_display(self):
        # 1. Wipe the old junk off the screen
        rgb_lcd_clear() 
        
        # 2. Get the top letter of each column
        display_word = "".join([col[0] for col in self.columns])
        
        # 3. Print the word
        rgb_lcd_print(display_word, row=0, col=0)
        
        # 4. (Optional) Show a cursor or indicator for the current column
        # If current_column is 2, it puts a '^' under the 3rd letter
        cursor = " " * self.current_column + "^"
        rgb_lcd_print(cursor, row=1, col=0)
    
    

    def check_guess(self):
        # Combine the top letter of every column
        result = "".join([c[0] for c in self.columns])
        if result == self.word:
            rgb_lcd_print("DISARMED", "GOOD JOB")
            return True
        else:
            time.sleep(0.3)
            return False
        
    def finish_cond(self):
        # Calculate the current guess from the columns
        self.result = "".join([col[0] for col in self.columns])
        
        if self.result == self.word:
            print("CORRECT! Bomb Disarmed.")
            # Show a success message on the LCD
            rgb_lcd_clear()
            return True 
        else:
            print(f"WRONG: {self.result.upper()} is not the password.")
            # Visual feedback on the plain LCD
            rgb_lcd_clear()
            
            time.sleep(1.5) # Let them read the error
            self.lcd_display() # Put the letters back on screen
            return False

    def game_loop(self):
        self.lcd_display()
        print(self.word)
        
        while True:
            # BUTTON 1 (Index 0) - Working
            if digital_read(self.btn_pins[0]):
                self.cycle_letter()
                self.lcd_display()
                while digital_read(self.btn_pins[0]): time.sleep(0.01)

            # BUTTON 2 (Index 1) - Switch Column
            if digital_read(self.btn_pins[1]):
                self.current_column = (self.current_column + 1) % 5
                self.lcd_display()
                while digital_read(self.btn_pins[1]): time.sleep(0.01)

            # BUTTON 3 (Index 2) - Submit
            if digital_read(self.btn_pins[2]):
                if self.finish_cond():
                    break # Ends the game if they won
                while digital_read(self.btn_pins[2]): time.sleep(0.01)
            
            time.sleep(0.05)

if __name__ == '__main__':
    game = Passwords([8,9,10]) # Assuming buttons on pins 4, 5, 6
    time.sleep(2)
    game.game_loop()