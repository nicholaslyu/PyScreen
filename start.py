import sys
import tkinter
import tkinter.filedialog
import os
from PIL import ImageGrab
from time import sleep
from pynput import keyboard
from screenshot import ScreenShot










def lieten_keyboard():

    # The key combination to check
    COMBINATIONS_1 = [
        {keyboard.KeyCode(char='s'), keyboard.KeyCode(char='c'),keyboard.Key.shift}
    ]
    COMBINATIONS_2 = [
        {keyboard.KeyCode(char='s'), keyboard.KeyCode(char='c'),keyboard.KeyCode(char='e')}
    ]
    # The currently active modifiers
    current_keys = set()
    def on_press(key):

        if any([key in COMBO for COMBO in COMBINATIONS_2]):
            current_keys.add(key)
            if current_keys == COMBINATIONS_2[0]:
                sys.exit()

        if any([key in COMBO for COMBO in COMBINATIONS_1]):
            current_keys.add(key)
            if current_keys == COMBINATIONS_1[0]:
                screenShot = ScreenShot()
                screenShot.start()
                current_keys.clear()


    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == '__main__':
    lieten_keyboard()