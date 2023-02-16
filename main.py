import curses #this is for the cli - command line interface
import json #this is to save and load shopping lists
import threading #this makes the input crispier than pringles
import queue #this is to send data between threads

class input_thread_class(threading.Thread): #making the input a separate thread makes the program feel more responsive
    def run(self):
        key = "null" #initialize var and enter the loop
        while key != "q":
            key = interface.stdscr.getkey()
            input_queue.put(key)

class interface_class():#this is the interface (cli class)
    def __init__(self):
        self.stdscr = curses.initscr()#create the curses screen
        curses.cbreak() #turn on cbreak (enter wont jump the cursor around)
        curses.noecho() #turn on noecho (you wont see what you type)
        curses.curs_set(0) #this is buggy on windows and in vscode, please use linuxx or at least powershell
        self.rows, self.cols = self.stdscr.getmaxyx() #get the windows rows and columns and store them in the object
        self.stdscr.clear()#clear the screen
        self.print_menu()#print the menu
        self.print_shopping_list()#print the shopping list beside the menu

    def print_shopping_list(self): #defines how you print the shopping list
        y_coord = 0 #setup coords
        x_coord = 18
        self.stdscr.move(y_coord +1, x_coord - 1) #move to coords with x - 1
        self.stdscr.vline(" ", len(shopping_list.items)) #this cleans out previous selection char (">")
        self.stdscr.move(y_coord, x_coord) #go to coord
        self.stdscr.addstr("shopping-list:")#15 chars long, this is the title of the shopping list section
        for iterator in range(len(shopping_list.items)):# go through every item in the shoppinglist and print them
            y_coord += 1 #set y coord to next line
            self.stdscr.move(y_coord, x_coord) #go to next line
            if shopping_list.selected == iterator: #is this the selected item?
                self.stdscr.move(y_coord, x_coord - 1) #go back to the margin
                self.stdscr.addch(">") #print the selection char (">")
            self.stdscr.addnstr((shopping_list.items[iterator][0] + "                                                         "), (self.cols - 19))#print item
        y_coord += 1 #when the foor loop is done go to the next line
        self.stdscr.refresh() #refresh the screen, this displays what we just printed

    def print_menu(self): #this prints the menu, it's quite simimilair to the shopping list print function
        y_coord = 0
        x_coord = 1
        self.stdscr.move(y_coord +1, x_coord - 1)
        self.stdscr.vline(" ", len(menu.options))
        self.stdscr.move(y_coord, x_coord)
        self.stdscr.addstr("menu:          ")#15 chars long
        self.stdscr.vline(curses.ACS_VLINE, 1000)
        for iterator in range(len(menu.options)):
            y_coord += 1
            self.stdscr.move(y_coord, x_coord)
            if menu.selected == iterator:
                self.stdscr.move(y_coord, x_coord - 1)
                self.stdscr.addch(">")
            self.stdscr.addstr(menu.options[iterator][0])
        y_coord += 1
        self.stdscr.move(y_coord, 1)
        self.stdscr.hline(curses.ACS_HLINE, 15)
        for iterator in range(len(menu.legend)):
            y_coord += 1
            self.stdscr.move(y_coord, x_coord)
            self.stdscr.addstr(menu.legend[iterator])
        self.stdscr.refresh()

class shopping_list_class: #this is the actual shopping list class, the items are stored in the item list "items"
    def __init__(self):
        try: #if we can read a json from default.shoppinglist we won't put the default items eggs and bacon in the list
            file_open = open("default.shoppinglist", "r") #open the file defailt.shoppinglist
            json_string = read(file_open) #read the file into a json string
            self.items = json.load(json_string) #parse the json into the "items" list
        except:
            self.items = [["eggs", 12], ["bacon", 1]] #if something goes wrong, just set these as default, bacon and eggs is the best breakfast innit
        #self.items = [["eggs", 12], ["bacon", 1], ["toast", 1], ["eggplant", 2], ["carrots", 4]]
        self.selected = 0 #the 0th item is selected, this is the top item in the list

#menu class
class menu_class:
    def __init__(self):
        self.options = [["add", add_class()], "load", "save", ["sort list", sort_class()], "export to file", "from recipe"]
        self.legend = ["k: up", "j: down", "l: list", "h: menu", "m: move up", "n: move down", "q: quit"]
        self.selected = 0
    def activate(self):
        self.options[self.selected][1].activate_option()

class option_class:
    def set_coords(self): #this just returns 0 so that the main function doesn't throw an exception when it tries to set coords to all the options in them menu
        return 0

class sort_class(option_class):
    def activate_option(self):
        shopping_list.items.sort()
        interface.print_shopping_list()

class popup_class(option_class):
    def __init__(self):
        self.width = 40
        self.height = 4
        self.titel = "popup"
        #this is just placeholders because the interface has yet to initiate since the interface depends on the menu this object is inside
        self.x_coord = 30
        self.y_coord = 6
    def set_coords(self):
        self.x_coord = (interface.cols // 2) - (self.width // 2)
        self.y_coord = (interface.rows // 2) - (self.height // 2)
    def activate_popup(self):
        interface.stdscr.move(self.y_coord, self.x_coord)
        interface.stdscr.hline(curses.ACS_HLINE, self.width)
        interface.stdscr.move(self.y_coord + self.height, self.x_coord)
        interface.stdscr.hline(curses.ACS_HLINE, self.width)
        interface.stdscr.refresh()

class add_class(popup_class):
    def activate_option(self):
        self.activate_popup()

#non functor functions
def move_down(pane):
    if pane == "shopping_list" and shopping_list.selected < (len(shopping_list.items) - 1):
        item = shopping_list.items.pop(shopping_list.selected)
        shopping_list.items.insert((shopping_list.selected + 1), item)
        shopping_list.selected += 1
        interface.print_shopping_list()

def select_down(pane):
    if pane == "menu" and menu.selected < (len(menu.options) - 1):
        menu.selected += 1
        interface.print_menu()
    elif pane == "shopping_list" and shopping_list.selected < (len(shopping_list.items) - 1):
        shopping_list.selected += 1
        interface.print_shopping_list()

def move_up(pane):
    if pane == "shopping_list" and shopping_list.selected != 0:
        item = shopping_list.items.pop(shopping_list.selected)
        shopping_list.items.insert((shopping_list.selected - 1), item)
        shopping_list.selected -= 1
        interface.print_shopping_list()

def select_up(pane):
    if pane == "menu" and menu.selected != 0:
        menu.selected -= 1
        interface.print_menu()
    elif pane == "shopping_list" and shopping_list.selected != 0:
        shopping_list.selected -= 1
        interface.print_shopping_list()

def main():
    input_thread.start()
    selected_pane = "menu"

    for iterator in range(len(menu.options)):
        try:
            menu.options[iterator][1].set_coords()
        except:
            print(f'{menu.options[iterator][0]} doesnt have a popup function')
    while True:
        key = input_queue.get()
        if key == "q":
            break
        elif key == "m":
            move_up(selected_pane)
        elif key == "n":
            move_down(selected_pane)
        elif key == "j":
            select_down(selected_pane)
        elif key == "k":
            select_up(selected_pane)
        elif key == "h":
            selected_pane = "menu"
        elif key == "l":
            selected_pane = "shopping_list"
        elif key == " " or key == "\n":
            menu.activate()
    input_thread.join()#when the loop is broken we will wait for the interface thread to join the main thread

menu = menu_class()#this is the menu class
shopping_list = shopping_list_class()#the actual shopping list
input_thread = input_thread_class()
interface = interface_class()#the interface class (which is a thread)
input_queue = queue.Queue()#this makes it possible to read and send data between threads
main()#starts main