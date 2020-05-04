import curses

ENTER = 10
ESCAPE = 27


class BOOLEAN_FORM():
    def __init__(self, True_key_Text, False_key_Text):
        self.screen = curses.initscr()
        curses.curs_set(False)
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.selected = False
        self.True_text = True_key_Text
        self.False_text = False_key_Text
        self.startIndex = 0

    def draw(self, messageTitle, messageText, selected, startIndex=0):
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
        true_x = x_start+int(x_start/2)
        false_x = 2*x_start+int(x_start/3)
        self.screen.move(y_start*3-2, true_x)
        if selected:
            self.screen.addstr('['+self.True_text+']', curses.color_pair(1))
        else:
            self.screen.addstr('['+self.True_text+']')
        self.screen.move(y_start*3-2, false_x)
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
            startIndex = 0
            self.startIndex = 0
        elif startIndex > maxAvailIndex:
            startIndex = maxAvailIndex
            self.startIndex = maxAvailIndex
        for ml in messageLines[startIndex:]:
            x = (2*x_start) - int(len(ml)/2)
            y += 2
            if y > end:
                break
            self.screen.move(y, x)
            self.screen.addstr(ml)

    def show(self, messageTitle='', messageText=''):
        self.draw(messageTitle, messageText, self.selected)
        while True:
            ch = self.screen.getch()
            if ch == curses.KEY_RIGHT or ch == curses.KEY_LEFT:
                self.selected = not self.selected
                self.draw(messageTitle, messageText, self.selected)
            elif ch == curses.KEY_UP:
                if self.startIndex > 0:
                    self.startIndex -= 1
                else:
                    self.startIndex = 0
                self.draw(
                    messageTitle, messageText, self.selected, self.startIndex)
            elif ch == curses.KEY_DOWN:
                self.startIndex += 1
                self.draw(
                    messageTitle, messageText, self.selected, self.startIndex)
            elif ch == ENTER:
                curses.nocbreak()
                self.screen.keypad(0)
                curses.echo()
                curses.endwin()
                return self.selected
            elif ch == ESCAPE:
                return False


class ONE_BUTTON_FORM():
    def __init__(self, button_text):
        self.screen = curses.initscr()
        curses.curs_set(False)
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.button_text = button_text
        self.startIndex = 0

    def draw(self, messageTitle, messageText, startIndex=0):
        # self.screen.clear()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
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
        true_x = (2*x_start) - int(len(self.button_text)/2)
        self.screen.move(y_start*3-2, true_x)
        self.screen.addstr('['+self.button_text+']', curses.color_pair(1))

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
            startIndex = 0
            self.startIndex = 0
        elif startIndex > maxAvailIndex:
            startIndex = maxAvailIndex
            self.startIndex = maxAvailIndex
        for ml in messageLines[startIndex:]:
            x = (2*x_start) - int(len(ml)/2)
            y += 2
            if y > end:
                break
            self.screen.move(y, x)
            self.screen.addstr(ml)

    def show(self, title='', message=''):
        self.draw(title, message)
        while True:
            ch = self.screen.getch()
            if ch == curses.KEY_UP:
                if self.startIndex > 0:
                    self.startIndex -= 1
                else:
                    self.startIndex = 0
                self.draw(title, message, self.startIndex)
            elif ch == curses.KEY_DOWN:
                self.startIndex += 1
                self.draw(title, message, self.startIndex)
            elif ch == ENTER:
                curses.nocbreak()
                self.screen.keypad(0)
                curses.echo()
                curses.endwin()
                return


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


class THREE_BUTTON_FORM():
    def __init__(self, first_key_Text, second_key_Text, third_key_Text):
        self.screen = curses.initscr()
        curses.curs_set(False)
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.selected = 0
        self.first_button = first_key_Text
        self.second_button = second_key_Text
        self.third_button = third_key_Text
        self.startIndex = 0

    def draw(self, messageTitle, messageText, selected, startIndex=0):
        # self.screen.clear()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
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
        third_x = (x_start+int(x_start/2)) - int(len(self.third_button)/2)
        second_x = (2*x_start) - int(len(self.second_button)/2)
        first_x = (2*x_start+int(x_start/2)) - int(len(self.first_button)/2)
        self.screen.move(y_start*3-2, first_x)
        if selected == 0:
            self.screen.addstr('['+self.first_button+']', curses.color_pair(1))
        else:
            self.screen.addstr('['+self.first_button+']')
        self.screen.move(y_start*3-2, second_x)
        if selected == 1:
            self.screen.addstr(
                '['+self.second_button+']', curses.color_pair(2))
        else:
            self.screen.addstr('['+self.second_button+']')
        self.screen.move(y_start*3-2, third_x)
        if selected == 2:
            self.screen.addstr('['+self.third_button+']', curses.color_pair(3))
        else:
            self.screen.addstr('['+self.third_button+']')

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
            startIndex = 0
            self.startIndex = 0
        elif startIndex > maxAvailIndex:
            startIndex = maxAvailIndex
            self.startIndex = maxAvailIndex
        for ml in messageLines[startIndex:]:
            x = (2*x_start) - int(len(ml)/2)
            y += 2
            if y > end:
                break
            self.screen.move(y, x)
            self.screen.addstr(ml)

    def show(self, messageTitle='', messageText=''):
        self.draw(messageTitle, messageText, self.selected)
        while True:
            ch = self.screen.getch()
            if ch == curses.KEY_RIGHT:
                if self.selected != 0:
                    self.selected -= 1
                self.draw(messageTitle, messageText, self.selected)
            elif ch == curses.KEY_LEFT:
                if self.selected != 2:
                    self.selected += 1
                self.draw(messageTitle, messageText, self.selected)
            elif ch == curses.KEY_UP:
                if self.startIndex > 0:
                    self.startIndex -= 1
                else:
                    self.startIndex = 0
                self.draw(
                    messageTitle, messageText, self.selected, self.startIndex)
            elif ch == curses.KEY_DOWN:
                self.startIndex += 1
                self.draw(
                    messageTitle, messageText, self.selected, self.startIndex)
            elif ch == ENTER:
                curses.nocbreak()
                self.screen.keypad(0)
                curses.echo()
                curses.endwin()
                return self.selected
            elif ch == ESCAPE:
                return False
