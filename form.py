import curses

ENTER = 10


class OK_CANCEL_FORM():

    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(False)
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.selected = False

    def draw(self, messageText, messageTitle, selected):
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
        ok_x = x_start+int(x_start/2)
        cancel_x = 2*x_start+int(x_start/3)
        self.screen.move(y_start*3-2, ok_x)
        if selected:
            self.screen.addstr('[OK]', curses.color_pair(1))
        else:
            self.screen.addstr('[OK]')
        self.screen.move(y_start*3-2, cancel_x)
        if selected:
            self.screen.addstr('[CANCEL]')
        else:
            self.screen.addstr('[CANCEL]', curses.color_pair(2))

        # Print Title
        Title_x = (2*x_start) - int(len(messageTitle)/2)
        Title_y = y_start - 2
        self.screen.move(Title_y, Title_x)
        self.screen.addstr(messageTitle)

        # Print Message
        lineMaxLength = 2*x_start - int(x_start/2)
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
        for ml in messageLines:
            x = (2*x_start) - int(len(ml)/2)
            y += 2
            self.screen.move(y, x)
            self.screen.addstr(ml)

    def show(self, messageText, messageTitle=''):
        self.draw(messageText, messageTitle, self.selected)
        while True:
            ch = self.screen.getch()
            if ch == curses.KEY_RIGHT or ch == curses.KEY_DOWN or ch == curses.KEY_LEFT or ch == curses.KEY_UP:
                self.selected = not self.selected
                self.draw(messageText, messageTitle, self.selected)
            if ch == ENTER:
                curses.nocbreak()
                self.screen.keypad(0)
                curses.echo()
                curses.endwin()
                return self.selected
