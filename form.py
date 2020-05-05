import curses

ENTER = 10
ESCAPE = 27


class INPUT_FORM():
    def __init__(self, default_input=''):
        self.screen = curses.initscr()
        # curses.curs_set(False)
        # curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.selected = False
        self.True_text = 'OK'
        self.False_text = 'CANCEL'
        self.input = default_input

    def draw(self, messageTitle, selected):
        # self.screen.clear()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        ymax, xmax = self.screen.getmaxyx()
        x_start = int(xmax/4)
        y_start = int(ymax/4)
        for j in range(x_start, xmax):
            for i in range(y_start-4, ymax):
                self.screen.move(i, j)
                try:
                    self.screen.addch(i, j, ' ')
                except Exception:
                    pass
        for i in range(x_start, x_start*3+1):
            self.screen.move(y_start-4, i)
            self.screen.addstr('=')
            self.screen.move(y_start, i)
            self.screen.addstr('=')
            if i >= x_start+2 and i <= x_start*3-1:
                self.screen.move(y_start+2, i)
                self.screen.addstr('-')
            self.screen.move(y_start+4, i)
            self.screen.addstr('=')
            self.screen.move(y_start+6, i)
            self.screen.addstr('=')
        for i in range(y_start-3, y_start+6):
            if i == y_start:
                continue
            self.screen.move(i, x_start)
            self.screen.addstr('|')
            self.screen.move(i, x_start*3)
            self.screen.addstr('|')
        true_x = x_start+int(x_start/2)
        false_x = 2*x_start+int(x_start/3)
        self.screen.move(y_start+5, true_x)
        if selected:
            self.screen.addstr('['+self.True_text+']', curses.color_pair(1))
        else:
            self.screen.addstr('['+self.True_text+']')
        self.screen.move(y_start+5, false_x)
        if selected:
            self.screen.addstr('['+self.False_text+']')
        else:
            self.screen.addstr('['+self.False_text+']', curses.color_pair(2))

        # Print Title
        Title_x = (2*x_start) - int(len(messageTitle)/2)
        Title_y = y_start - 2
        self.screen.move(Title_y, Title_x)
        self.screen.addstr(messageTitle)

        # Print Message
        inputShow = ' '+self.input+' '
        x = (2*x_start) - int(len(inputShow)/2)
        y = y_start+2
        self.screen.move(y, x)
        self.screen.addstr(inputShow)

    def show(self, messageTitle=''):
        self.draw(messageTitle, self.selected)
        while True:
            ch = self.screen.getch()
            if ch == curses.KEY_RIGHT or ch == curses.KEY_LEFT:
                self.selected = not self.selected
                self.draw(messageTitle, self.selected)
            elif ch == ESCAPE:
                return None
            elif ch == ENTER:
                if self.selected:
                    curses.nocbreak()
                    self.screen.keypad(0)
                    curses.echo()
                    curses.endwin()
                    if self.input != '':
                        return self.input
                    return None
                else:
                    return None
            elif ch == curses.KEY_BACKSPACE:
                self.input = self.input[0:-1]
                self.draw(messageTitle, self.selected)
            else:
                self.input += chr(ch)
                self.draw(messageTitle, self.selected)


class MESSAGEBOX():
    def __init__(self, KEYS):
        self.screen = curses.initscr()
        curses.curs_set(False)
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.selected = 0
        self.Buttons = KEYS
        self.startIndex = 0
        if not len(KEYS):
            raise ValueError('KEYS must contains at least 1 item')

    def draw(self, messageTitle, messageText):
        # self.screen.clear()
        curses.start_color()
        curses.use_default_colors()
        ymax, xmax = self.screen.getmaxyx()
        x_start = int(xmax/4)
        y_start = int(ymax/4)
        for j in range(x_start, xmax):
            for i in range(y_start-4, ymax):
                self.screen.move(i, j)
                try:
                    self.screen.addch(i, j, ' ')
                except Exception:
                    pass
        for i in range(x_start, x_start*3+1):
            self.screen.move(y_start-4, i)
            self.screen.addstr('=')
            self.screen.move(y_start, i)
            self.screen.addstr('=')
            self.screen.move(y_start*3-4, i)
            self.screen.addstr('-')
            self.screen.move(y_start*3, i)
            self.screen.addstr('=')
        for i in range(y_start-3, y_start*3):
            if i == y_start:
                continue
            self.screen.move(i, x_start)
            self.screen.addstr('|')
            self.screen.move(i, x_start*3)
            self.screen.addstr('|')

        # Print MessageBox Buttons
        for indx, button in enumerate(self.Buttons):
            curses.init_pair(indx+1, button['ForeColor'], button['BackColor'])
            pos_x = (
                x_start+(
                            (len(self.Buttons)-indx)*int(
                                            (2*x_start)/(len(self.Buttons)+1)
                                        )
                        )
                    ) - int(len(button['Text'])/2)
            self.screen.move(y_start*3-2, pos_x)
            if self.selected == indx:
                self.screen.addstr(
                    '['+button['Text']+']', curses.color_pair(indx+1)
                                  )
            else:
                self.screen.addstr('['+button['Text']+']')

        # Print Title
        Title_x = (2*x_start) - int(len(messageTitle)/2)
        Title_y = y_start - 2
        self.screen.move(Title_y, Title_x)
        self.screen.addstr(messageTitle)

        # Print Message
        lineMaxLength = 2*x_start - int(x_start/2)
        if '\n' in messageText:
            messageLines = messageText.split('\n')
        else:
            messageLines = []
            string = ""
            for i in messageText.split():
                if len(string)+len(i)+1 <= lineMaxLength:
                    string += ' '+i
                else:
                    messageLines.append(string)
                    string = i
            if string != "":
                messageLines.append(string)
        y = y_start
        end = y_start*3-6
        messageFieldSize = int((end - y-2)/2)+1
        maxAvailIndex = len(messageLines) - messageFieldSize
        if len(messageLines) <= messageFieldSize:
            self.startIndex = 0
        elif self.startIndex > maxAvailIndex:
            self.startIndex = maxAvailIndex
        for ml in messageLines[self.startIndex:]:
            x = (2*x_start) - int(len(ml)/2)
            y += 2
            if y > end:
                break
            self.screen.move(y, x)
            self.screen.addstr(ml)

    def show(self, messageTitle='', messageText=''):
        self.draw(messageTitle, messageText)
        while True:
            ch = self.screen.getch()
            if ch == curses.KEY_RIGHT:
                if self.selected != 0:
                    self.selected -= 1
                self.draw(messageTitle, messageText)
            elif ch == curses.KEY_LEFT:
                if self.selected != len(self.Buttons)-1:
                    self.selected += 1
                self.draw(messageTitle, messageText)
            elif ch == curses.KEY_UP:
                if self.startIndex > 0:
                    self.startIndex -= 1
                else:
                    self.startIndex = 0
                self.draw(
                    messageTitle, messageText)
            elif ch == curses.KEY_DOWN:
                self.startIndex += 1
                self.draw(messageTitle, messageText)
            elif ch == ENTER:
                curses.nocbreak()
                self.screen.keypad(0)
                curses.echo()
                curses.endwin()
                return self.selected
            elif ch == ESCAPE:
                return 0
