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
    res.sort()
    return res


def childfiles(path):
    res = []
    for i in os.scandir(path):
        if os.DirEntry.is_file(i):
            res.append(i.name)
    res.sort()
    return res


def parentdir(path):
    if path == '/':
        return path
    return re.findall(r'(.*/).?\w+', path)[0]


DONT_SHOW_HIDDEN = True


def draw(menu, directories, files, selectedIndex, PrintStartIndex=0):
    y, x = screen.getmaxyx()
    screen.clear()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    menuformat = [
        '-'*x,
        f"[ ]{menu[0]['text']}\t[ ]{menu[1]['text']}\t[ ]{menu[2]['text']}\t[ ]{menu[3]['text']}\t[ ]{menu[4]['text']}",
        '-'*x,
        f"[ :>] {menu[5]['text']}",
        '-'*x,
        f"[ >] {menu[6]['text']}"
                 ]

    if PrintStartIndex <= len(menuformat):
        for i in range(len(menuformat)):
            try:
                screen.addstr(i-PrintStartIndex, 0, menuformat[i])
            except:
                pass
    for i in range(len(directories)):
        try:
            screen.move(directories[i]['posx']-PrintStartIndex, 0)
            screen.addstr(
                        directories[i]['posx']-PrintStartIndex,
                        0,
                        f"[ >] {directories[i]['text']}/",
                        curses.color_pair(3)
                     )
        except:
            pass
    for i in range(len(files)):
        try:
            screen.move(files[i]['posx']-PrintStartIndex, 0)
            screen.addstr(
                        files[i]['posx']-PrintStartIndex,
                        0,
                        f"[ >] {files[i]['text']}"
                     )
        except:
            pass


    # draw selections
    for i in range(len(directories)):
        try:
            if directories[i]['selected']:
                screen.addstr(
                            directories[i]['posx']-PrintStartIndex,
                            directories[i]['posy'],
                            "#",
                            curses.color_pair(2)
                         )
        except:
            pass
    for i in range(len(files)):
        try:
            if files[i]['selected']:
                screen.addstr(
                            files[i]['posx']-PrintStartIndex,
                            files[i]['posy'],
                            "#",
                            curses.color_pair(2)
                         )
        except:
            pass
    # draw pointer
    if selectedIndex >= len(menu):
        indx = selectedIndex-len(menu)
        if indx >= len(directories):
            indx = indx-len(directories)
            letter = files
            selectedIndex = indx
        else:
            letter = directories
            selectedIndex = indx
    else:
        letter = menu
    screen.move(letter[selectedIndex]['posx']-PrintStartIndex, letter[selectedIndex]['posy'])
    screen.addstr(
                    letter[selectedIndex]['posx']-PrintStartIndex,
                    letter[selectedIndex]['posy'],
                    "#",
                    curses.color_pair(1)
                 )
    screen.refresh()


def exlpore(pwd=None):
    # curses.start_color()
    # curses.use_default_colors()
    CWD = os.getcwd()
    if pwd is None:
        pwd = CWD
    menu = {
            0: {'text': 'Insert tag', 'posx': 1, 'posy': 1},
            1: {'text': 'Remove tag', 'posx': 1, 'posy': 17},
            2: {'text': 'Modify tag', 'posx': 1, 'posy': 33},
            3: {'text': 'Search by tag', 'posx': 1, 'posy': 49},
            4: {'text': 'Exit', 'posx': 1, 'posy': 73},
            5: {'text': pwd, 'posx': 3, 'posy': 1},
            6: {'text': '..', 'posx': 5, 'posy': 1},
           }
    selectedIndex = len(menu)-1
    printStartIndex = 0
    indxd = 0
    directories = {}
    for d in childir(pwd):
        if DONT_SHOW_HIDDEN and d[0] == '.':
            continue
        directories.update({indxd: {'text': d, 'posx': indxd+len(menu), 'posy': 1, 'selected': False}})
        indxd += 1
    indxf = 0
    files = {}
    for f in childfiles(pwd):
        if DONT_SHOW_HIDDEN and f[0] == '.':
            continue
        files.update({indxf: {'text': f, 'posx': indxf+len(menu)+indxd, 'posy': 1, 'selected': False}})
        indxf += 1
    draw(menu, directories, files, selectedIndex)
    try:
        while True:
            char = screen.getch()
            if char == ord('q') or char == ord('Q'):
                break
            elif char == curses.KEY_RIGHT or char == curses.KEY_DOWN:
                y, _ = curses.getsyx()
                ymax, _ = screen.getmaxyx()
                if y == ymax-1:
                    printStartIndex += 1
                if selectedIndex == len(menu)+len(directories)+len(files)-1:
                    selectedIndex = 0
                    printStartIndex = 0
                    draw(menu, directories, files, selectedIndex, printStartIndex)
                else:
                    selectedIndex += 1
                    draw(menu, directories, files, selectedIndex, printStartIndex)
            elif char == curses.KEY_LEFT or char == curses.KEY_UP:
                y, x = curses.getsyx()
                ymax, _ = screen.getmaxyx()
                if y == 0:
                    printStartIndex -= 1
                if selectedIndex == 0:
                    selectedIndex = len(menu)+len(directories)+len(files)-1
                    printStartIndex = len(menu)+len(directories)+len(files) - ymax
                    if printStartIndex < 0:
                        printStartIndex = 0
                    draw(menu, directories, files, selectedIndex, printStartIndex)
                else:
                    selectedIndex -= 1
                    if selectedIndex <= len(menu)-1 and printStartIndex > menu[selectedIndex]['posx']:
                        printStartIndex = menu[selectedIndex]['posx']
                    draw(menu, directories, files, selectedIndex, printStartIndex)
            elif char == 10:  # Enter
                    if selectedIndex < len(menu):
                        if menu[selectedIndex]['text'] == '..':
                            return exlpore(pwd=parentdir(menu[5]['text']))
                        elif selectedIndex == 5:
                            exlpore(pwd=pwd)
                        else:
                            pass # TODO: run selected action
                    elif selectedIndex < len(menu)+len(directories):
                        return exlpore(pwd=os.path.join(pwd, directories[selectedIndex-len(menu)]['text']))
            elif char == 32:  # Space
                if selectedIndex >= len(menu):
                    indx = selectedIndex-len(menu)
                    if indx >= len(directories):
                        indx = indx-len(directories)
                        files[indx]['selected'] = not files[indx]['selected']
                    else:
                        directories[indx]['selected'] = not directories[indx]['selected']
                draw(menu, directories, files, selectedIndex)

    except PermissionError:
        exlpore(pwd=pwd)
    except Exception:
        exlpore(pwd=pwd)
    finally:
        # shut down cleanly
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()


if __name__ == "__main__":
    try:
        os.chdir(os.path.abspath(sys.argv[1]))
    except IndexError:
        pass
    exlpore()
