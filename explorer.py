import os
import re
from termcolor import colored
import mongoengine
import curses

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)


CWD = os.getcwd()
childir = lambda x:os.walk(x).next()[1]
childfiles = lambda x:os.walk(x).next()[2]
parentdir = lambda x:re.findall(r'(.*/)\w+', x)[0]

def show(pwd = None, mod = 0, selectedIndex = 0):
    ### CLEAR SCREEN
    #os.system('clear')
    checkmark = '*'#colored('*','red',attrs=['bold'])
    opts = [' ']*6
    if pwd == None:
        pwd = CWD
    screen.addstr(0,0,'---------------------------------------------------------------------------------')
    screen.addstr(1,0,"[{}]Insert tag\t[{}]Remove tag\t[{}]Modify tag\t[{}]Search by tag\t[{}]Exit".format(opts[0], opts[1], opts[2], opts[3], opts[4]))
    screen.addstr(2,0,'---------------------------------------------------------------------------------')
    screen.addstr(3,0,"[{}:>] {}".format(opts[5], pwd))
    screen.addstr(4,0,'---------------------------------------------------------------------------------')
    if mod == 0:
        opts.append(' ')
        screen.addstr(5,0,"[{}>] {}".format(opts[6], '..'))
        opts.append(' ')
        screen.addstr(6,0,"[{}>] {}".format(opts[7], childir(pwd)))
        opts.append(' ')
        screen.addstr(7,0,"[{}>] {}".format(opts[8], childfiles(pwd)))
    else:
        if mod == 1:
            lst = childir(pwd)
        else:
            lst = childfiles(pwd)
        for i in range(len(lst)):
            opts.append(' ')
            print("[{}>] {}".format(opts[6+i], lst[i]))
    curses.start_color()
    curses.use_default_colors()
    screen.addstr(selectedIndex,1,'#', curses.color_pair(197))
    opts[selectedIndex] = checkmark
    try:
        while True:
            char = screen.getch()
            if char == ord('x') or char == ord('X') :
                break
            elif char == curses.KEY_RIGHT or char == curses.KEY_DOWN:
                if selectedIndex == len(opts)-1:
                    return show(pwd, mod, 0)
                else:
                    return show(pwd, mod, selectedIndex+1)
            elif char == curses.KEY_LEFT or char == curses.KEY_UP:
                if selectedIndex == 0:
                    return show(pwd, mod, 0)
                else:
                    return show(pwd, mod, selectedIndex-1)
            elif char == curses.KEY_ENTER:
                pass
    finally:
        # shut down cleanly
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()

# try:
#     show()
# except:
#     pass
