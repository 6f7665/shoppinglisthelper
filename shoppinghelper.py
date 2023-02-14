import curses
import json
from curses.textpad import rectangle

def load_default_shoppinglist():
    try:
        file_to_read_from = open("default.shoppinglist", "w+")
        data_from_file = file_to_read_from.read()
        return json.loads(data_from_file)
        file_to_read_from.close()
    except:
        return [["eggs", "24"], ["chicken", "1kg"]] #default shoppinglist

class item_class:
    def __init__(self, name_to_init):
        self.name = name_to_init
    def get_full_name(self):
        return self.name
    def get_full_name_selected(self):
        return str(">" + self.name)

class input_class(item_class):
    def activate(self):
        self.input_string = screen.get_input()
        self.run()
    def run(self):
        print(f'{self.input_string}')

class add_class(input_class):
    def run(self):
        return self.input_string

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
                                "main": [0, (self.menu_width + 2), (curses.LINES -1), ((curses.COLS - self.menu_width) + 1)],
                                "popup": [((curses.LINES // 2) - 10), ((curses.COLS // 2) -20), 20, 40],
                              } #this is y, x, height, width

    def print_list_to_pane(self, list_to_write, selected, pane):
        pane_coords = self.pane_dictonary.get(pane)
        for iterator in range(len(list_to_write)):
            self.stdscrn.move((iterator + 1), (pane_coords[1] + 1))
            if iterator == selected:
                try:
                    self.stdscrn.addnstr(list_to_write[iterator].get_full_name_selected() + self.cleanstring, self.menu_width - 3)
                except:
                    self.stdscrn.addnstr((">" + str(list_to_write[iterator][0]) + ": " + str(list_to_write[iterator][1])), 30)
            else:
                try:
                    self.stdscrn.addnstr(" " + list_to_write[iterator].get_full_name() + self.cleanstring, self.menu_width - 3)
                except:
                    self.stdscrn.addnstr((" " + str(list_to_write[iterator][0]) + ": " + str(list_to_write[iterator][1])), 30)
        self.update_screen()

    def update_screen(self):
        curses.curs_set(False)
        self.stdscrn.refresh()
    
    def terminate(self):#this is mainly to reset the terminal on gnu/linux systems
        curses.echo()#turn on writing into stdscrn
        curses.nocbreak()#turn on jumping around with cursor
        curses.curs_set(True)#show the cursor
        self.stdscrn.keypad(False)#keypad off

    def get_input(self):
        return "maguro"

screen = screen_class()
def main():
    menu_list = [ add_class("add"), input_class("save"), item_class("load") ]
    current_selected = 0
    menu_selected = current_selected
    screen.print_list_to_pane(menu_list, current_selected, "menu")
    shopping_list = load_default_shoppinglist()
    screen.print_list_to_pane(shopping_list, -1, "main")
    current_pane = "menu"
    current_list = menu_list
    while(True):
        char = screen.stdscrn.getkey()
        if char == "q":
            break
        elif char == "j" and current_selected < (len(current_list) - 1):
            current_selected += 1
            screen.print_list_to_pane(current_list, current_selected, current_pane)
        elif char == "k" and current_selected > 0:
            current_selected -= 1
            screen.print_list_to_pane(current_list, current_selected, current_pane)
        elif current_pane == "menu":
            if char == "l":
                screen.print_list_to_pane(current_list, -1, current_pane)
                current_pane = "main"
                current_list = shopping_list
                menu_selected = current_selected
                current_selected = 0
                screen.print_list_to_pane(current_list, current_selected, current_pane)
            elif char == "\n" and current_pane == "menu":
                menu_list[current_selected].activate()
        elif current_pane == "main":
            if char == "h":
                screen.print_list_to_pane(current_list, -1, current_pane)
                current_pane = "menu"
                current_list = menu_list
                current_selected = menu_selected
                screen.print_list_to_pane(current_list, current_selected, current_pane)
            elif char == "m":
                menu_list[current_selected].activate(screen)
    screen.terminate()

main()#ore ha ochinchin ga daisuki nan da yo // is this divine intellect even?
