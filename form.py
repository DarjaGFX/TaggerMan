import curses

ENTER = 10


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
        self.screen.clear()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        ymax, xmax = self.screen.getmaxyx()
        x_start = int(xmax/4)
        y_start = int(ymax/4)

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
            if ch == curses.KEY_UP:
                if self.startIndex > 0:
                    self.startIndex -= 1
                else:
                    self.startIndex = 0
                self.draw(messageTitle, messageText, self.selected, self.startIndex)
            if ch == curses.KEY_DOWN:
                self.startIndex += 1
                self.draw(messageTitle, messageText, self.selected, self.startIndex)
            if ch == ENTER:
                curses.nocbreak()
                self.screen.keypad(0)
                curses.echo()
                curses.endwin()
                return self.selected


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
        self.screen.clear()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        ymax, xmax = self.screen.getmaxyx()
        x_start = int(xmax/4)
        y_start = int(ymax/4)

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
            if ch == curses.KEY_DOWN:
                self.startIndex += 1
                self.draw(title, message, self.startIndex)
            if ch == ENTER:
                curses.nocbreak()
                self.screen.keypad(0)
                curses.echo()
                curses.endwin()
                return
