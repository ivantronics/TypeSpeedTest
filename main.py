import curses
from curses import wrapper
import time
import random


# Welcoming screen with rules
def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(
        "Test your typing speed with this little program. You will be given a "
        "sentence to type.")
    stdscr.addstr("\nYou will have to correctly type what you see. ")
    stdscr.addstr("If you make a mistake, it will be highlited with red color.")
    stdscr.addstr(
        "\nCorrect it before you continue. Timer starts as soon as you press "
        "SPACE.")
    stdscr.addstr(
        "\nUse ESC to quit during test. Press any other key now to quit")
    stdscr.refresh()
    key = stdscr.getkey()
    if key == ' ':  # Starting the test if spacebar is pressed
        start_typing_test(stdscr)


# Display logic for currently inputed text
def display_text(stdscr, target_text, user_typed_text, wpm, cpm, error_rate,
                 keystrokes, errors):
    stdscr.addstr(target_text)
    wpm = "n/a" if wpm == 0 else f"{wpm:.2f}"
    cpm = "n/a" if cpm == 0 else f"{cpm:.0f}"
    stdscr.addstr(3, 2,
                  f"Words per minute = {wpm}, characters per minute = {cpm}")
    stdscr.addstr(4, 2, f"Your error rate is {error_rate:.2f}%")
    stdscr.addstr(5, 2, f"{keystrokes = } {errors = }")
    for idx, key_pressed in enumerate(user_typed_text):
        color = curses.color_pair(2)
        if idx < len(target_text):
            if key_pressed == target_text[idx]:
                color = curses.color_pair(1)
        stdscr.addstr(0, idx, key_pressed, color)


# Checking for current mistakes
def count_equal_chars(target, current):
    correct_chars = 0
    for i, j in zip(target, current):
        if i == j:
            correct_chars += 1
    return correct_chars


# Commencing the test itself
def start_typing_test(stdscr):
    target_text = get_text()
    user_typed_text = []
    time_start = time.time()
    stdscr.nodelay(True)
    keystrokes = 0
    error_inputs = 0

    while True:
        # Handling time and counting words per minute
        time_current = max(time.time() - time_start, 1)
        correct_inputs = count_equal_chars(target_text, user_typed_text)
        cpm = correct_inputs / (time_current / 60)
        wpm = cpm / 5
        error_rate = error_inputs / keystrokes * 100 if keystrokes > 0 else 0

        # Displaying current user input
        stdscr.clear()
        display_text(stdscr, target_text, user_typed_text, wpm, cpm, error_rate,
                     keystrokes, error_inputs)
        stdscr.refresh()

        if "".join(user_typed_text) == target_text:
            break

        try:
            user_keyinput = stdscr.getkey()  # Getting user input
        except:
            continue

        if ord(user_keyinput) == 27:  # Qutting if we get ESC
            exit()
        if user_keyinput in (
        "KEY_BACKSPACE", "\b", "\x7f"):  # Handling Backspace button
            if user_typed_text:
                user_typed_text.pop()
        else:
            keystrokes += 1
            user_typed_text.append(
                user_keyinput)  # Putting pressed key into the list
            if len(user_typed_text) <= len(target_text):
                if user_keyinput != target_text[len(user_typed_text) - 1]:
                    error_inputs += 1
            else:
                error_inputs += 1

    stdscr.nodelay(False)
    stdscr.addstr(7, 2,
                  "Sucess! Press spacebar if you would like to try again, "
                  "any other key to quit")
    user_input = stdscr.getkey()
    if user_input == " ":
        start_typing_test(stdscr)


# Generating random phrase from Moby Dick and stripping it from punctuation
def get_text():
    with open("mobydick.txt", encoding="utf8") as f:
        lines = f.readlines()
        line = list(random.choice(lines).strip())
        new_line = "".join([i for i in line if i.isalpha() or i.isspace()])
        return new_line


def main(stdscr):
    # Initializing color pairs
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Executing welcome screen
    start_screen(stdscr)


if __name__ == '__main__':
    wrapper(main)
