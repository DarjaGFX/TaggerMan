#!/usr/bin/python3.8
import os
import re
import sys
import curses
import shutil
from form import BOOLEAN_FORM, ONE_BUTTON_FORM, INPUT_FORM
# import mongoengine

ENTER = 10
SPACE = 32
CTRLX = 24
CTRLH = 8
SHIFTDELETE = 383

CLIPBOARD = {
                'Action': None,
                'Fs': []
            }


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
    global screen
    y, x = screen.getmaxyx()
    screen.clear()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    menuformat = [
        '-'*x,
        f"[ ]{menu[0]['text']}\t[ ]{menu[1]['text']}\t[ ]{menu[2]['text']}\
\t[ ]{menu[3]['text']}\t[ ]{menu[4]['text']}",
        '-'*x,
        f"[ :>] {menu[5]['text']}",
        '-'*x,
        f"[ >] {menu[6]['text']}"
                 ]

    if PrintStartIndex <= len(menuformat):
        for i in range(len(menuformat)):
            try:
                screen.addstr(i-PrintStartIndex, 0, menuformat[i])
            except Exception:
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
        except Exception:
            pass
    for i in range(len(files)):
        try:
            screen.move(files[i]['posx']-PrintStartIndex, 0)
            screen.addstr(
                        files[i]['posx']-PrintStartIndex,
                        0,
                        f"[ >] {files[i]['text']}"
                     )
        except Exception:
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
        except Exception:
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
        except Exception:
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
    screen.move(
                letter[selectedIndex]['posx']-PrintStartIndex,
                letter[selectedIndex]['posy']
               )
    screen.addstr(
                    letter[selectedIndex]['posx']-PrintStartIndex,
                    letter[selectedIndex]['posy'],
                    "#",
                    curses.color_pair(1)
                 )
    screen.refresh()


def resetClipboard():
    global CLIPBOARD
    CLIPBOARD = {
                'Action': None,
                'Fs': []
            }


def permanent_delete():
    for f in CLIPBOARD['Fs']:
        try:
            if os.path.exists(f):
                if os.path.isdir(f):
                    shutil.rmtree(f, ignore_errors=False)
                else:
                    os.remove(f)
        except Exception:
            pass


def NewFolder(Path, FolderName='UntitledFolder'):
    try:
        os.mkdir(FolderName)
    except Exception:
        if os.path.exists(os.path.join(Path, FolderName)):
            ErrorForm = BOOLEAN_FORM('OK', 'Cancel')
            if ErrorForm.show(
                    messageTitle='Something went wrong!',
                    messageText='Folder exists...\nchoose another name.'
                 ):
                inp = INPUT_FORM()
                return NewFolder(
                        Path=Path,
                        FolderName=inp.show("Folder Name:")
                    )
        else:
            ErrorForm = ONE_BUTTON_FORM('Ok')
            msg = 'Permission denied'
            ErrorForm.show(
                title='Something went wrong!',
                message=msg
                )


def Move(destination):
    for f in CLIPBOARD['Fs']:
        try:
            if os.path.exists(f):
                if os.path.isdir(f):
                    shutil.rmtree(f, ignore_errors=False)
                else:
                    os.remove(f)
        except Exception:
            pass


def runaction():
    if CLIPBOARD['Action'] == permanent_delete:
        form = BOOLEAN_FORM(True_key_Text='OK', False_key_Text='CANCEL')
        if form.show(
                messageTitle='Deleting These Files/Folders Permanently!',
                messageText='\n'.join(CLIPBOARD['Fs'])
                    ):
            CLIPBOARD['Action']()
    # elif CLIPBOARD['Action'] == Move:
        #  #if exists in destination , ask for replace or new name
        # form = OK_CANCEL_FORM()
        # if form.show(
        #         messageTitle='DELETE',
        #         messageText='DELETE selected file/folders PERMANENTLY?'
        #             ):
        #    CLIPBOARD['Action']()
    resetClipboard()


def exlpore(pwd=None):
    if CLIPBOARD['Action'] is None:
        resetClipboard()
    global DONT_SHOW_HIDDEN
    global screen
    screen = curses.initscr()
    curses.curs_set(False)
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    if pwd is None:
        pwd = os.getcwd()
    os.chdir(pwd)
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
    # Create Directories Dict
    for d in childir(pwd):
        if DONT_SHOW_HIDDEN and d[0] == '.':
            continue
        directories.update(
                            {
                                indxd: {
                                        'text': d,
                                        'posx': indxd+len(menu),
                                        'posy': 1,
                                        'selected': False
                                        }
                            }
                           )
        indxd += 1
    indxf = 0
    files = {}
    # Create Files Dict
    for f in childfiles(pwd):
        if DONT_SHOW_HIDDEN and f[0] == '.':
            continue
        files.update(
                        {
                            indxf: {
                                    'text': f,
                                    'posx': indxf+len(menu)+indxd,
                                    'posy': 1,
                                    'selected': False
                                    }
                        }
                    )
        indxf += 1
    draw(menu, directories, files, selectedIndex)
    lenAll = len(menu)+len(directories)+len(files)
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
                if selectedIndex == lenAll-1:
                    selectedIndex = 0
                    printStartIndex = 0
                    draw(menu, directories, files, selectedIndex,
                         printStartIndex)
                else:
                    selectedIndex += 1
                    draw(menu, directories, files, selectedIndex,
                         printStartIndex)
            elif char == curses.KEY_LEFT or char == curses.KEY_UP:
                y, x = curses.getsyx()
                ymax, _ = screen.getmaxyx()
                if y == 0:
                    printStartIndex -= 1
                if selectedIndex == 0:
                    selectedIndex = lenAll-1
                    printStartIndex = lenAll - ymax
                    if printStartIndex < 0:
                        printStartIndex = 0
                    draw(menu, directories, files, selectedIndex,
                         printStartIndex)
                else:
                    selectedIndex -= 1
                    if (selectedIndex <= len(menu)-1
                        and
                            printStartIndex > menu[selectedIndex]['posx']):
                        printStartIndex = menu[selectedIndex]['posx']
                    draw(menu, directories, files, selectedIndex,
                         printStartIndex)
            elif char == ENTER:
                if selectedIndex < len(menu):
                    if menu[selectedIndex]['text'] == '..':
                        return exlpore(pwd=parentdir(menu[5]['text']))
                    elif selectedIndex == 5:
                        return exlpore(pwd=pwd)
                    else:
                        pass  # TODO: run selected action
                elif selectedIndex < len(menu)+len(directories):
                    return exlpore(
                            pwd=os.path.join(
                                pwd,
                                directories[selectedIndex-len(menu)]['text']))
            elif char == SPACE:
                if selectedIndex >= len(menu):
                    indx = selectedIndex-len(menu)
                    if indx >= len(directories):
                        indx = indx-len(directories)
                        files[indx]['selected'] = not files[indx]['selected']
                        if files[indx]['selected']:
                            CLIPBOARD['Fs'].append(
                                os.path.join(pwd, files[indx]['text']))
                        else:
                            CLIPBOARD['Fs'].remove(
                                os.path.join(pwd, files[indx]['text']))
                    else:
                        directories[indx]['selected'] = \
                            not directories[indx]['selected']
                        if directories[indx]['selected']:
                            CLIPBOARD['Fs'].append(
                                os.path.join(pwd, directories[indx]['text']))
                        else:
                            CLIPBOARD['Fs'].remove(
                                os.path.join(pwd, directories[indx]['text']))
                draw(menu, directories, files, selectedIndex, printStartIndex)
            elif char == CTRLH:
                DONT_SHOW_HIDDEN = not DONT_SHOW_HIDDEN
                return exlpore(pwd=pwd)
            elif char == CTRLX:
                CLIPBOARD['Action'] = Move
            # elif char == curses.KEY_F2:
                # CLIPBOARD['Action'] = Rename
                # runaction()
                # return exlpore(pwd=pwd)
            elif char == SHIFTDELETE:
                if len(CLIPBOARD['Fs']):
                    CLIPBOARD['Action'] = permanent_delete
                    runaction()
                    return exlpore(pwd=pwd)
            elif char == ord('n') or char == ord('N'):
                form = INPUT_FORM()
                NewFolder(
                    Path=pwd,
                    FolderName=form.show(messageTitle="Folder Name:")
                    )
                return exlpore(pwd=pwd)

    except PermissionError:
        return exlpore(pwd=pwd)
    except Exception:
        return exlpore(pwd=pwd)
    finally:
        # shut down cleanly
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()


if __name__ == "__main__":
    try:
        if '-a' in sys.argv or '--all' in sys.argv:
            DONT_SHOW_HIDDEN = False
        os.chdir(os.path.abspath(sys.argv[-1]))
    except Exception:
        pass
    exlpore()
