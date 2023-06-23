import curses
import time 



# print("init curses ")
stdscr = curses.initscr()

stdscr.addstr(10, 0, "Current mode: Typing mode",
              curses.A_REVERSE)
stdscr.refresh()

time.sleep(1)

pad = curses.newpad(100, 100)
# These loops fill the pad with letters; addch() is
# explained in the next section
for y in range(0, 99):
    for x in range(0, 99):
        pad.addch(y,x, "1")

# Displays a section of the pad in the middle of the screen.
# (0,0) : coordinate of upper-left corner of pad area to display.
# (5,5) : coordinate of upper-left corner of window area to be filled
#         with pad content.
# (20, 75) : coordinate of lower-right corner of window area to be
#          : filled with pad content.
pad.refresh( 0,0, 5,5, 20,75)

time.sleep(1)


"""
https://docs.python.org/3/howto/curses.html
https://github.com/gravmatt/py-term/blob/master/term.py
https://stackoverflow.com/questions/45294134/python-curses-terminal-resize-issue

"""