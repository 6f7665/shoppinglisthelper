import curses #this is for the cli - command line interface
import json #this is to save and load shopping lists
import threading #this makes the input crispier than pringles
import queue #this is to send data between threads

class input_thread_class(threading.Thread):
    def run(self):
        key = "null" #initialize var and enter the loop
        while key != "q":
            key = interface.stdscr.getkey()
            input_queue.put(key)

class interface_class():
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        self.stdscr.clear()#clear the screen
        self.stdscr.addstr("menu:     ")#10 chars long
        self.stdscr.vline(curses.ACS_VLINE, 1000)
        self.stdscr.refresh()
        for option in menu.options:
            self.stdscr.addstr(option)

class shopping_list_class:
    def __init__(self):
        try: #if we can read a json from default.shoppinglist we won't put the default items eggs and bacon in the list
            file_open = open("default.shoppinglist", "r")
            json_string = read(file_open)
            self.items = json.load(json_string)
        except:
            self.items = [["eggs", 12], ["bacon", 1]]
        self.selected = 0

#menu class
class menu_class:
    def __init__(self):
        self.options = ["add", "remove", "read", "save"]
        self.selected = 0

#non functor functions
def select_down(pane):
    if pane == "menu" and menu.selected < len(menu.menu_list):
        menu.selected += 1
    elif pane == "shopping_list" and shopping_list.selected < len(shopping_list.items):
        shopping_list.selected += 1

def select_up(pane):
    if pane == "menu" and menu.selected != 0:
        menu.selected -= 1

def main():
    input_thread.start()
    selected_pane = "menu"
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
    input_thread.join()#when the loop is broken we will wait for the interface thread to join the main thread

menu = menu_class()#this is the menu class
input_thread = input_thread_class()
interface = interface_class()#the interface class (which is a thread)
input_queue = queue.Queue()#this makes it possible to read and send data between threads
shopping_list = shopping_list_class()#the actual shopping list
main()#starts main