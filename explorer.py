#!/usr/bin/python3.8
import os
import re
import sys
import curses
import shutil
from form import INPUT_FORM, MESSAGEBOX
import settings


ENTER = 10
SPACE = 32
CTRLH = 8
HOME = 262
END = 360
CTRLHOME = 535
CTRLEND = 530
CTRLA = 1
SHIFTDELETE = 383
PAGEUP = 339
PAGEDOWN = 338
VERBOS = False

COLOR = {
            'BLACK': 0,
            'RED': 1,
            'GREEN': 2,
            'YELLOW': 3,
            'BLUE': 4,
            'MAGENTA': 5,
            'CYAN': 6,
            'WHITE': 7
        }


CLIPBOARD = {
                'Action': None,
                'Fs': []
            }


def find_name(name):
    res = []
    os.system(settings.UPDATERPATH)
    Res = os.popen(f'locate -i {name}').read()
    for i in Res.split('\n'):
        if name.upper() in i.upper().split('/')[-1]:
            res.append(i)
    if res == []:
        res = None
    return res


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


def draw(
            menu, directories, files, selectedIndex,
            PrintStartIndex=0, SearchMode=False
        ):
    global screen
    y, x = screen.getmaxyx()
    screen.clear()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    if SearchMode:
        header = 'Xplore (Search Mode)'
    else:
        header = 'Xplore'
    menuformat = [
        '='*x,
        ((' '*(int(x/2)-int(len(header)/2))) +
            header+' '*(int(x/2)-int(len(header)/2))),
        '='*x,
        f"[ :>] {menu[0]['text']}",
        '-'*x
        ]
    try:
        menuformat.append(f"[ >] {menu[1]['text']}")
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
    # if PrintStartIndex <= len(menuformat):

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

    for i in range(len(menuformat)):
        try:
            if PrintStartIndex > 0 and i == len(menuformat)-1:
                continue
            screen.addstr(i, 0, menuformat[i])
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
            ErrorForm = MESSAGEBOX(
                    [
                        {
                            'Text': 'CANCEL',
                            'ForeColor': COLOR['BLACK'],
                            'BackColor': COLOR['RED']
                        },
                        {
                            'Text': 'OK',
                            'ForeColor': COLOR['BLACK'],
                            'BackColor': COLOR['GREEN']
                        }
                    ])
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
            ErrorForm = MESSAGEBOX([
                {
                    'Text': 'Ok',
                    'ForeColor': COLOR['WHITE'],
                    'BackColor': COLOR['BLACK']
                }
                ])
            msg = 'Permission denied'
            ErrorForm.show(
                title='Something went wrong!',
                message=msg
                )


def Rename(NewName):
    if NewName is None:
        return
    i = 0
    for item in CLIPBOARD['Fs']:
        try:
            if i == 0:
                nn = NewName
            else:
                nn = f"{NewName}({i})"
            if nn != item:
                while os.path.exists(nn):
                    i += 1
                    nn = f"{NewName}({i})"
            os.rename(src=item, dst=os.path.join(parentdir(item), nn))
            i += 1
        except PermissionError:
            ErrorForm = MESSAGEBOX([
                    {
                        'Text': 'Ok',
                        'ForeColor': COLOR['WHITE'],
                        'BackColor': COLOR['BLACK']
                    }
                ])
            msg = 'Permission denied'
            ErrorForm.show(
                title='Something went wrong!',
                message=msg
                )


def Copy():
    des = os.getcwd()
    replaceAll_Flag = False
    skipAll_Flag = False
    for i in CLIPBOARD['Fs']:
        name = i.split('/')[-1]
        try:
            new_name = os.path.join(des, name)
            if os.path.isdir(i):
                for r, d, f in os.walk(i):
                    rs = len(i)
                    nr = new_name+r[rs:]
                    try:
                        os.makedirs(nr)
                    except FileExistsError:
                        pass
                    for ffile in f:
                        new_file_name = os.path.join(nr, ffile)
                        if os.path.exists(new_file_name):
                            if skipAll_Flag:
                                continue
                            if not replaceAll_Flag:
                                replaceMSGBOX = MESSAGEBOX([
                                    {
                                        'Text': 'CANCEL',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['RED']
                                    },
                                    {
                                        'Text': 'REPLACE',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['GREEN']
                                    },
                                    {
                                        'Text': 'REPLACE ALL',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['YELLOW']
                                    },
                                    {
                                        'Text': 'SKIP',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['GREEN']
                                    },
                                    {
                                        'Text': 'SKIP ALL',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['YELLOW']
                                    }
                                ])
                                response = replaceMSGBOX.show(
                                    messageTitle='File Exists',
                                    messageText=f"{new_file_name} Already\
Exists.\nreplace it?")
                                if response == 4:
                                    skipAll_Flag = True
                                if response == 2:
                                    replaceAll_Flag = True
                                elif response == 0:
                                    break
                                elif response == 3:
                                    continue
                        shutil.copy2(
                            os.path.join(r, ffile), os.path.join(nr, ffile))
            else:
                if os.path.exists(new_name):
                    if skipAll_Flag:
                        continue
                    if not replaceAll_Flag:
                        replaceMSGBOX = MESSAGEBOX([
                                    {
                                        'Text': 'CANCEL',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['RED']
                                    },
                                    {
                                        'Text': 'REPLACE',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['GREEN']
                                    },
                                    {
                                        'Text': 'REPLACE ALL',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['YELLOW']
                                    },
                                    {
                                        'Text': 'SKIP',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['GREEN']
                                    },
                                    {
                                        'Text': 'SKIP ALL',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['YELLOW']
                                    }
                                ])
                        response = replaceMSGBOX.show(
                            messageTitle='File Exists',
                            messageText=f"{new_name} Already Exists.\n\
replace it?")
                        if response == 4:
                            skipAll_Flag = True
                        if response == 2:
                            replaceAll_Flag = True
                        elif response == 0:
                            break
                        elif response == 3:
                            continue
                shutil.copy2(i, new_name)
        except PermissionError:
            if VERBOS:
                ErrorForm = MESSAGEBOX([
                    {
                        'Text': 'Ok',
                        'ForeColor': COLOR['WHITE'],
                        'BackColor': COLOR['BLACK']
                    }
                ])
                msg = 'Permission denied'
                ErrorForm.show(
                    title='Something went wrong!',
                    message=msg
                    )
        except Exception:
            if VERBOS:
                ErrorForm = MESSAGEBOX([
                    {
                        'Text': 'Ok',
                        'ForeColor': COLOR['WHITE'],
                        'BackColor': COLOR['BLACK']
                    }
                ])
                msg = f'{i} could not be copied'
                ErrorForm.show(
                    title='Something went wrong!',
                    message=msg
                    )


def Move():
    des = os.getcwd()
    replaceAll_Flag = False
    skipAll_Flag = False
    for i in CLIPBOARD['Fs']:
        name = i.split('/')[-1]
        try:
            new_name = os.path.join(des, name)
            if i == new_name:
                continue
            if os.path.isdir(i):
                for r, d, f in os.walk(i):
                    rs = len(i)
                    nr = new_name+r[rs:]
                    try:
                        os.makedirs(nr)
                    except FileExistsError:
                        pass
                    for ffile in f:
                        new_file_name = os.path.join(nr, ffile)
                        if os.path.exists(new_file_name):
                            if skipAll_Flag:
                                continue
                            if not replaceAll_Flag:
                                replaceMSGBOX = MESSAGEBOX([
                                    {
                                        'Text': 'CANCEL',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['RED']
                                    },
                                    {
                                        'Text': 'REPLACE',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['GREEN']
                                    },
                                    {
                                        'Text': 'REPLACE ALL',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['YELLOW']
                                    },
                                    {
                                        'Text': 'SKIP',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['GREEN']
                                    },
                                    {
                                        'Text': 'SKIP ALL',
                                        'ForeColor': COLOR['BLACK'],
                                        'BackColor': COLOR['YELLOW']
                                    }
                                ])
                                response = replaceMSGBOX.show(
                                    messageTitle='File Exists',
                                    messageText=f"{new_file_name} Already\
Exists.\nreplace it?")
                                if response == 4:
                                    skipAll_Flag = True
                                if response == 2:
                                    replaceAll_Flag = True
                                elif response == 0:
                                    break
                                elif response == 3:
                                    continue
                        shutil.move(
                            os.path.join(r, ffile), new_file_name)
                shutil.rmtree(i, ignore_errors=False)
            else:
                if os.path.exists(new_name):
                    if skipAll_Flag:
                        continue
                    if not replaceAll_Flag:
                        replaceMSGBOX = MESSAGEBOX([
                            {
                                'Text': 'CANCEL',
                                'ForeColor': COLOR['BLACK'],
                                'BackColor': COLOR['RED']
                            },
                            {
                                'Text': 'REPLACE',
                                'ForeColor': COLOR['BLACK'],
                                'BackColor': COLOR['GREEN']
                            },
                            {
                                'Text': 'REPLACE ALL',
                                'ForeColor': COLOR['BLACK'],
                                'BackColor': COLOR['YELLOW']
                            },
                            {
                                'Text': 'SKIP',
                                'ForeColor': COLOR['BLACK'],
                                'BackColor': COLOR['GREEN']
                            },
                            {
                                'Text': 'SKIP ALL',
                                'ForeColor': COLOR['BLACK'],
                                'BackColor': COLOR['YELLOW']
                            }
                        ])
                        response = replaceMSGBOX.show(
                            messageTitle='File Exists',
                            messageText=f"{new_name} Already Exists.\nreplace\
it?")
                        if response == 4:
                            skipAll_Flag = True
                        if response == 2:
                            replaceAll_Flag = True
                        elif response == 0:
                            break
                        elif response == 3:
                            continue
                shutil.move(i, new_name)
        except PermissionError:
            if VERBOS:
                ErrorForm = MESSAGEBOX([
                    {
                        'Text': 'Ok',
                        'ForeColor': COLOR['WHITE'],
                        'BackColor': COLOR['BLACK']
                    }
                ])
                msg = 'Permission denied'
                ErrorForm.show(
                    title='Something went wrong!',
                    message=msg
                    )
        except Exception:
            if VERBOS:
                ErrorForm = MESSAGEBOX([
                    {
                        'Text': 'Ok',
                        'ForeColor': COLOR['WHITE'],
                        'BackColor': COLOR['BLACK']
                    }
                ])
                msg = f'{i} could not be moved'
                ErrorForm.show(
                    title='Something went wrong!',
                    message=msg
                    )


def runaction():
    if CLIPBOARD['Action'] == permanent_delete:
        form = MESSAGEBOX(
                    [
                        {
                            'Text': 'CANCEL',
                            'ForeColor': COLOR['BLACK'],
                            'BackColor': COLOR['RED']
                        },
                        {
                            'Text': 'OK',
                            'ForeColor': COLOR['BLACK'],
                            'BackColor': COLOR['GREEN']
                        }
                    ])
        if form.show(
                messageTitle='Deleting These Files/Folders Permanently!',
                messageText='\n'.join(CLIPBOARD['Fs'])
                    ):
            CLIPBOARD['Action']()
    elif CLIPBOARD['Action'] == Rename:
        defval = ''
        if len(CLIPBOARD['Fs']) == 1:
            defval = CLIPBOARD['Fs'][0]
        inp = INPUT_FORM(defval)
        CLIPBOARD['Action'](inp.show('New Name:'))

    elif CLIPBOARD["Action"] == Move:
        Move()

    elif CLIPBOARD["Action"] == Copy:
        Copy()

    resetClipboard()


def exlpore(pwd=None, SearchMode=None):
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
    searchmod_flag = False
    if SearchMode:
        searchmod_flag = True
        menu = {
                0: {'text': 'Search Result', 'posx': 3, 'posy': 1},
            }
        selectedIndex = len(menu)-1
        printStartIndex = 0
        indxd = 0
        directories = {}
        ln_menu = 6
        indxf = 0
        files = {}
        # Create Files Dict
        for f in SearchMode:
            files.update(
                            {
                                indxf: {
                                        'text': f,
                                        'posx': indxf+ln_menu+indxd,
                                        'posy': 1,
                                        'selected': False
                                        }
                            }
                        )
            indxf += 1
        draw(
                menu, directories, files,
                selectedIndex, SearchMode=searchmod_flag
            )
        lenAll = len(menu)+len(directories)+len(files)

    else:
        menu = {
                0: {'text': pwd, 'posx': 3, 'posy': 1},
                1: {'text': '..', 'posx': 5, 'posy': 1},
            }
        selectedIndex = len(menu)-1
        printStartIndex = 0
        indxd = 0
        directories = {}
        ln_menu = 6
        # Create Directories Dict
        for d in childir(pwd):
            if DONT_SHOW_HIDDEN and d[0] == '.':
                continue
            directories.update(
                                {
                                    indxd: {
                                            'text': d,
                                            'posx': indxd+ln_menu,
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
                                        'posx': indxf+ln_menu+indxd,
                                        'posy': 1,
                                        'selected': False
                                        }
                            }
                        )
            indxf += 1
        draw(
                menu, directories, files,
                selectedIndex, SearchMode=searchmod_flag
            )
        lenAll = len(menu)+len(directories)+len(files)

    def select():
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

    try:
        while True:
            char = screen.getch()
            ymax, _ = screen.getmaxyx()
            ymaxFrame = ymax - (ln_menu - 1)
            if char == ord('q') or char == ord('Q'):
                break
            elif char == ord('x') or char == ord('X'):
                if not len(CLIPBOARD['Fs']):
                    select()
                if len(CLIPBOARD['Fs']):
                    CLIPBOARD['Action'] = Move
            elif char == ord('c') or char == ord('C'):
                if not len(CLIPBOARD['Fs']):
                    select()
                if len(CLIPBOARD['Fs']):
                    CLIPBOARD['Action'] = Copy
            elif char == ord('v') or char == ord('V'):
                if len(CLIPBOARD) and CLIPBOARD['Action'] in [Move, Copy]:
                    runaction()
                    return exlpore(pwd=pwd)
            elif char == ord('n') or char == ord('N'):
                form = INPUT_FORM()
                msg = "Folder Name (will be set automaticly if cancel):"
                name = form.show(messageTitle=msg)
                if name:
                    NewFolder(
                        Path=pwd,
                        FolderName=name
                        )
                else:
                    NewFolder(
                        Path=pwd
                        )
                return exlpore(pwd=pwd)
            elif char == curses.KEY_RIGHT or char == curses.KEY_DOWN:
                y, _ = curses.getsyx()
                if y == ymax-1:
                    printStartIndex += 1
                if selectedIndex == lenAll-1:
                    selectedIndex = 0
                    printStartIndex = 0
                    draw(menu, directories, files, selectedIndex,
                         printStartIndex, SearchMode=searchmod_flag)
                else:
                    selectedIndex += 1
                    draw(menu, directories, files, selectedIndex,
                         printStartIndex, SearchMode=searchmod_flag)
            elif char == curses.KEY_LEFT or char == curses.KEY_UP:
                y, x = curses.getsyx()
                if y == 5 and printStartIndex > 0:
                    printStartIndex -= 1
                if selectedIndex == 0:
                    selectedIndex = lenAll-1
                    printStartIndex = (lenAll - 1) - ymaxFrame
                    if printStartIndex < 0:
                        printStartIndex = 0
                    draw(menu, directories, files, selectedIndex,
                         printStartIndex, SearchMode=searchmod_flag)
                else:
                    selectedIndex -= 1
                    if (selectedIndex <= len(menu)-1
                        and
                            printStartIndex > menu[selectedIndex]['posx']):
                        printStartIndex = menu[selectedIndex]['posx']
                    draw(menu, directories, files, selectedIndex,
                         printStartIndex, SearchMode=searchmod_flag)
            elif char == curses.KEY_F2:
                if not len(CLIPBOARD['Fs']):
                    select()
                if len(CLIPBOARD['Fs']):
                    CLIPBOARD['Action'] = Rename
                    runaction()
                return exlpore(pwd=pwd)
            elif char == curses.KEY_F3:
                inp = INPUT_FORM()
                name = inp.show('search for: ')
                opts = []
                if name:
                    opts = find_name(name)
                return exlpore(pwd=pwd, SearchMode=opts)
            elif char == curses.KEY_F5:
                return exlpore(pwd=pwd)
            elif char == ENTER:
                if selectedIndex < len(menu):
                    if menu[selectedIndex]['text'] == '..':
                        return exlpore(pwd=parentdir(menu[0]['text']))
                    return exlpore(pwd=pwd)
                elif selectedIndex < len(menu)+len(directories):
                    return exlpore(
                            pwd=os.path.join(
                                pwd,
                                directories[selectedIndex-len(menu)]['text']))
                elif searchmod_flag:
                    pwd = parentdir(files[selectedIndex-len(menu)]['text'])
                    return exlpore(pwd=pwd)
            elif char == SPACE:
                select()
                draw(
                        menu, directories, files, selectedIndex,
                        printStartIndex, SearchMode=searchmod_flag
                    )
            elif char == CTRLA:
                for i in directories.keys():
                    directories[i]['selected'] = True
                    CLIPBOARD['Fs'].append(
                        os.path.join(pwd, directories[i]['text']))
                for i in files.keys():
                    files[i]['selected'] = True
                    CLIPBOARD['Fs'].append(
                        os.path.join(pwd, files[i]['text']))
                draw(
                        menu, directories, files, selectedIndex,
                        printStartIndex, SearchMode=searchmod_flag
                    )
            elif char == CTRLH:
                DONT_SHOW_HIDDEN = not DONT_SHOW_HIDDEN
                return exlpore(pwd=pwd)
            elif char == SHIFTDELETE:
                if not len(CLIPBOARD['Fs']):
                    select()
                if len(CLIPBOARD['Fs']):
                    CLIPBOARD['Action'] = permanent_delete
                    runaction()
                return exlpore(pwd=pwd)
            elif char == CTRLHOME:
                selectedIndex = len(menu)-1
                printStartIndex = 0
                draw(
                        menu, directories, files, selectedIndex,
                        printStartIndex, SearchMode=searchmod_flag
                    )
            elif char == CTRLEND:
                selectedIndex = lenAll-1
                printStartIndex = (lenAll - 1) - ymaxFrame
                if printStartIndex < 0:
                    printStartIndex = 0
                draw(
                        menu, directories, files, selectedIndex,
                        printStartIndex, SearchMode=searchmod_flag
                    )
            elif char == HOME:
                selectedIndex = printStartIndex + 1
                draw(
                        menu, directories, files, selectedIndex,
                        printStartIndex, SearchMode=searchmod_flag
                    )
            elif char == END:
                if printStartIndex+ymaxFrame > lenAll:
                    selectedIndex = lenAll-1
                else:
                    selectedIndex = printStartIndex + ymaxFrame
                draw(
                        menu, directories, files, selectedIndex,
                        printStartIndex, SearchMode=searchmod_flag
                    )
            elif char == PAGEUP:
                if printStartIndex - ymaxFrame < 0:
                    printStartIndex = 0
                else:
                    printStartIndex -= ymaxFrame
                if selectedIndex - ymaxFrame < 0:
                    selectedIndex = 1
                else:
                    selectedIndex -= ymaxFrame
                draw(
                        menu, directories, files, selectedIndex,
                        printStartIndex, SearchMode=searchmod_flag
                    )
            elif char == PAGEDOWN:
                if printStartIndex + ymaxFrame > lenAll - ymaxFrame:
                    # printStartIndex = lenAll - ymaxFrame
                    pass
                else:
                    printStartIndex += ymaxFrame
                if selectedIndex + ymaxFrame > lenAll-1:
                    selectedIndex = lenAll-1
                else:
                    selectedIndex += ymaxFrame
                draw(
                        menu, directories, files, selectedIndex,
                        printStartIndex, SearchMode=searchmod_flag
                    )

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
        if '-v' in sys.argv or '--VERBOS' in sys.argv:
            VERBOS = True
        os.chdir(os.path.abspath(sys.argv[-1]))
    except Exception:
        pass
    exlpore()
