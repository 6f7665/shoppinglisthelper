import curses
import json
from curses.textpad import rectangle

def load_default_shoppinglist():
    data_from_file = '{1: ["eggs", "24" ], 2: ["chicken", "1kg"],}'
    try:
        file_to_read_from = open("default.shoppinglist", "w+")
        data_from_file = file_to_read_from.read()
        return json.loads(data_from_file)
    except:
        return { 1: ["eggs", "24"], 2: ["chicken", "1kg"] } #default shoppinglist

class option_class:
    def __init__(self, name_to_init)
        self.name = name_to_init
    def get_full_name(self):
        return self.name
    def get_full_name_selected(self)
        return ">" + self.name

class screen_class:
    def __init__(self):
        self.stdscrn = curses.initscr()#create a stdscrn
        curses.noecho()#turn off writing into stdscrn
        curses.cbreak()#turn off jumping around with cursor
        curses.curs_set(False)#hide the cursor
        self.stdscrn.keypad(True)#curses will return curses codes (curses.KEY_UP) instead of multibyte codes
        self.menu_width = int(curses.COLS // 3)#1/3 looks kirei af
        if self.menu_width > 20:
            self.menu_width = 20
        rectangle(self.stdscrn, 0, 0, (curses.LINES - 1), self.menu_width + 2)
        rectangle(self.stdscrn, 0, 0, (curses.LINES - 1), (curses.COLS - 2))

        self.cleanstring = "                                                                                                                                                                                         "
        self.pane_dictonary = { "menu": [0, 0, (curses.LINES -1), (self.menu_width + 2)],
                           "main": [0, self.menu_width, (curses.LINES -1), (curses.COLS - (self.menu_width + 2))],
                          } #this is y, x, height, width

    def print_list_to_pane(self, list_to_write, selected, pane):
        pane_coords = self.pane_dictonary.get(pane)
        for iterator in range(len(list_to_write)):
            self.stdscrn.move((iterator + 1), (pane_coords[1] + 2))
            if iterator == selected:
                self.stdscrn.addnstr(list_to_write[iterator][0] + self.cleanstring, self.menu_width - 3)
            else:
                self.stdscrn.addnstr(list_to_write[iterator][0] + self.cleanstring, self.menu_width - 3)
        self.update_screen()

    def update_screen(self):
        curses.curs_set(False)
        self.stdscrn.refresh()
    
    def terminate(self):#this is mainly to reset the terminal on gnu/linux systems
        curses.echo()#turn on writing into stdscrn
        curses.nocbreak()#turn on jumping around with cursor
        curses.curs_set(True)#show the cursor

def main():
    screen = screen_class()
    menu_list = [["add", 1], ["save", 2], ["load", 6]]
    menu_selected = 0
    screen.print_list_to_pane(menu_list, menu_selected, "menu")
    #load the standard shoppinglist
    shoppinglist = load_default_shoppinglist()
    while(True):
        char = screen.stdscrn.getkey()
        if char == "q":
            break
        elif char == "j" and menu_selected < (len(menu_list) - 1):
            menu_selected += 1
            screen.print_list_to_pane(menu_list, menu_selected, "menu")
        elif char == "k" and menu_selected != 0:
            menu_selected -= 1
            screen.print_list_to_pane(menu_list, menu_selected, "menu")
    #debug# print(f'{shoppinglist[1][0]}: {shoppinglist[1][1]}')
    screen.terminate()

main()#ore ha ochinchin ga daisuki nan da yo // is this divine intellect even?
