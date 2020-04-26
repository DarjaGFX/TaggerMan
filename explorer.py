#!/usr/bin/python3.8
import os
import re
import sys
import curses
# import mongoengine

screen = curses.initscr()
curses.curs_set(False)
curses.noecho()
curses.cbreak()
screen.keypad(True)


def childir(path):
    res = []
    for i in os.scandir(path):
        if os.DirEntry.is_dir(i):
            res.append(i.name)
    return res


def childfiles(path):
    res = []
    for i in os.scandir(path):
        if os.DirEntry.is_file(i):
            res.append(i.name)
    return res


def parentdir(path):
    if path == '/':
        return path
    return re.findall(r'(.*/)\w+', path)[0]


DONT_SHOW_HIDDEN = True


def draw(letter, selectedIndex=0):
    screen.clear()
    screen.addstr(0, 0, '-'*82)
    screen.addstr(1, 0, f"[ ]{letter[0]['text']}\t[ ]{letter[1]['text']}\t[ ]{letter[2]['text']}\t[ ]{letter[3]['text']}\t[ ]{letter[4]['text']}")
    screen.addstr(2, 0, '-'*82)
    screen.addstr(3, 0, f"[ :>] {letter[5]['text']}")
    screen.addstr(4, 0, '-'*82)
    screen.addstr(5, 0, f"[ >] {letter[6]['text']}")
    for i in range(7, len(letter)):
        if letter[i]['type'] == 'directory':
            screen.addstr(letter[i]['posx'], 0, f"[ >] {letter[i]['text']}/")
        elif letter[i]['type'] == 'file':
            screen.addstr(letter[i]['posx'], 0, f"[ >] {letter[i]['text']}")
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    for i in range(len(letter)):
        if letter[i]['selected']:
            screen.addstr(
                            letter[i]['posx'],
                            letter[i]['posy'],
                            "#",
                            curses.color_pair(2)
                         )
    screen.addstr(
                    letter[selectedIndex]['posx'],
                    letter[selectedIndex]['posy'],
                    "#",
                    curses.color_pair(1)
                 )
    screen.refresh()


def exlpore(pwd=None):
    # curses.start_color()
    # curses.use_default_colors()
    selectedIndex = 6
    CWD = os.getcwd()
    if pwd is None:
        pwd = CWD
    objs = {
            0: {'text': 'Insert tag', 'posx': 1, 'posy': 1, 'type': 'command', 'selected': False},
            1: {'text': 'Remove tag', 'posx': 1, 'posy': 17, 'type': 'command', 'selected': False},
            2: {'text': 'Modify tag', 'posx': 1, 'posy': 33, 'type': 'command', 'selected': False},
            3: {'text': 'Search by tag', 'posx': 1, 'posy': 49, 'type': 'command', 'selected': False},
            4: {'text': 'Exit', 'posx': 1, 'posy': 73, 'type': 'command', 'selected': False},
            5: {'text': pwd, 'posx': 3, 'posy': 1, 'type': 'directory', 'selected': False},
            6: {'text': '..', 'posx': 5, 'posy': 1, 'type': 'directory', 'selected': False},
           }
    indx = 6
    for d in childir(pwd):
        if DONT_SHOW_HIDDEN and d[0] == '.':
            continue
        objs.update({len(objs): {'text': d, 'posx': indx, 'posy': 1, 'type': 'directory', 'selected': False}})
        indx += 1
    for f in childfiles(pwd):
        if DONT_SHOW_HIDDEN and f[0] == '.':
            continue
        objs.update({len(objs): {'text': f, 'posx': indx, 'posy': 1, 'type': 'file', 'selected': False}})
        indx += 1
    draw(objs, selectedIndex)
    try:
        while True:
            char = screen.getch()
            if char == ord('x') or char == ord('X'):
                break
            elif char == curses.KEY_RIGHT or char == curses.KEY_DOWN:
                if selectedIndex == len(objs)-1:
                    selectedIndex = 0
                    draw(objs, selectedIndex)
                else:
                    selectedIndex += 1
                    draw(objs, selectedIndex)
            elif char == curses.KEY_LEFT or char == curses.KEY_UP:
                if selectedIndex == 0:
                    selectedIndex = len(objs)-1
                    draw(objs, selectedIndex)
                else:
                    selectedIndex -= 1
                    draw(objs, selectedIndex)
            elif char == 10:  # Enter
                if objs[selectedIndex]['type'] == 'directory':
                    if objs[selectedIndex]['text'] == '..':
                        return exlpore(pwd=parentdir(objs[5]['text']))
                    return exlpore(pwd=os.path.join(pwd, objs[selectedIndex]['text']))
            elif char == 32:  # Space
                objs[selectedIndex]['selected'] = not objs[selectedIndex]['selected']
    except PermissionError:
        exlpore(pwd=pwd)
    except:
        pass
    finally:
        # shut down cleanly
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()


if __name__ == "__main__":
    try:
        os.chdir(os.path.abspath(sys.argv[1]))
    except:
        pass
    exlpore()
