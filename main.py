import curses #this is for the cli - command line interface
import json #this is to save and load shopping lists
import threading #this makes the input crispier than pringles
import queue #this is to send data between threads

class input_thread_class(threading.Thread): #making the input a separate thread makes the program feel more responsive
    def run(self):
        key = "null" #initialize var and enter the loop
        stop_bool = False
        while stop_bool == False: #if the key is q and exit on q is armed we will exit this loop and join thread with main
            key = interface.stdscr.getkey()
            input_queue.put(key)
            if key == " " or key == "\n":
                exit_on_q.clear()#disarm the exit on q bool
            if exit_on_q.is_set() and key == "q":
                stop_bool = True #this will term the loop

class interface_class():#this is the interface (cli class)
    def __init__(self):
        self.stdscr = curses.initscr()#create the curses screen
        curses.cbreak() #turn on cbreak (enter wont jump the cursor around)
        curses.noecho() #turn on noecho (you wont see what you type)
        curses.curs_set(0) #this is buggy on windows and in vscodium (and vscode), please use linux or at least powershell
        self.menu_select_symbol = ">" #this is to show the which list you are in
        self.shopping_list_select_symbol = "-"
        self.rows, self.cols = self.stdscr.getmaxyx() #get the windows rows and columns and store them in the object
        self.stdscr.clear()#clear the screen
        self.print_menu()#print the menu
        self.print_shopping_list()#print the shopping list beside the menu

    def print_shopping_list(self): #defines how you print the shopping list
        y_coord = 0 #setup coords
        x_coord = 18
        self.stdscr.move(y_coord +1, x_coord - 1) #move to coords with x - 1
        self.stdscr.vline(" ", len(shopping_list.items) + 1) #this cleans out previous selection char (">") # + 1 doesnt throw exception when empty
        self.stdscr.move(y_coord, x_coord) #go to coord
        self.stdscr.addstr("shopping-list: (" + str(len(shopping_list.items)) + " items)")#this is the title of the shopping list section
        for iterator in range(len(shopping_list.items)):# go through every item in the shoppinglist and print them
            y_coord += 1 #set y coord to next line
            self.stdscr.move(y_coord, x_coord) #go to next line
            if shopping_list.selected == iterator: #is this the selected item?
                self.stdscr.move(y_coord, x_coord - 1) #go back to the margin
                self.stdscr.addch(self.shopping_list_select_symbol) #print the selection char (">")
            self.stdscr.addnstr((shopping_list.items[iterator][0] + "                                                             "), (self.cols - 19))#print item
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
                self.stdscr.addch(self.menu_select_symbol)
            self.stdscr.addnstr(menu.options[iterator][0], 15)
        y_coord += 1
        self.stdscr.move(y_coord, 1)
        self.stdscr.hline(curses.ACS_HLINE, 15)
        for iterator in range(len(menu.legend)):
            y_coord += 1
            self.stdscr.move(y_coord, x_coord)
            self.stdscr.addnstr(menu.legend[iterator], 15)
        self.stdscr.refresh()

class shopping_list_class: #this is the actual shopping list class, the items are stored in the item list "items"
    def __init__(self):
        try: #if we can read a json from default.shoppinglist we won't put the default items eggs and bacon in the list
            file_open = open("default.shoppinglist", "r+") #open the file defailt.shoppinglist
            json_string = file_open.read() #read the file into a json string
            self.items = json.loads(json_string) #parse the json into the "items" list
        except:
            self.items = [["eggs", 12], ["bacon", 1]] #if something goes wrong, just set these as default, bacon and eggs is the best breakfast innit
        #self.items = [["eggs", 12], ["bacon", 1], ["toast", 1], ["eggplant", 2], ["carrots", 4]]
        self.selected = 0 #the 0th item is selected, this is the top item in the list

#menu class
class menu_class:
    def __init__(self): #the menu class holds the options list and a list of keybinds the user may use, much like nano
        self.options = [["add", add_class()], ["load", load_class()], ["save", save_class()], ["sort list", sort_class()], ["remove", remove_class()], ["export", export_class()]]
        self.legend = ["k: up", "j: down", "l: list", "h: menu", "m: move up", "n: move down", "q: quit"]
        self.selected = 0
    def activate(self):
        self.options[self.selected][1].activate_option()

class option_class:
    def set_coords(self): #this just returns 0 so that the main function doesn't throw an exception when it tries to set coords to all the options in them menu
        return 0

class sort_class(option_class):
    def activate_option(self):
        shopping_list.items.sort() #this calls the sort function of a python list
        interface.print_shopping_list()
        exit_on_q.set()#arm the exit on q bool

class export_class(option_class):
    def activate_option(self):
        file_to_write = open("export.html", "w") #open the file specified by user
        file_to_write.write('''<html lang="en"><head><title="shoppinglist"></head><body><ul>''')
        for iterator in range(len(shopping_list.items)):
            write_string = "<li>" + str(shopping_list.items[iterator][0]) + ": " + str(shopping_list.items[iterator][1]) + "</li>"
            file_to_write.write(write_string)
        file_to_write.write('''</ul></body></html>''')
        exit_on_q.set()#arm the exit on q bool
        file_to_write.close() #close file

class popup_class(option_class):
    def __init__(self):
        self.width = 40
        self.height = 3
        #this is just placeholders because the interface has yet to initiate since the interface depends on the menu this object is inside
        self.x_coord = 30
        self.y_coord = 6
    def set_coords(self): #this will setup coords after the interface is initialized
        self.x_coord = (interface.cols // 2) - (self.width // 2)
        self.y_coord = (interface.rows // 2) - (self.height // 2)
    def activate_popup(self, title): #this hideous code creates a rectangle with a title
        interface.stdscr.move(self.y_coord, self.x_coord)
        interface.stdscr.hline(curses.ACS_HLINE, self.width)
        interface.stdscr.move(self.y_coord + 1, self.x_coord + 2)
        interface.stdscr.addnstr(title, self.width - 5)
        interface.stdscr.move(self.y_coord + 1, self.x_coord)
        interface.stdscr.vline(curses.ACS_VLINE, self.height - 1)
        interface.stdscr.move(self.y_coord + 1, self.x_coord + self.width - 1)
        interface.stdscr.vline(curses.ACS_VLINE, self.height - 1)
        interface.stdscr.move(self.y_coord + self.height, self.x_coord)
        interface.stdscr.hline(curses.ACS_HLINE, self.width)
        interface.stdscr.refresh()
    def show_input(self, input_string):
        interface.stdscr.move(self.y_coord + 2, self.x_coord + 2)
        interface.stdscr.addnstr(input_string, self.width - 5)
        interface.stdscr.refresh()
    def get_input(self):
        input_string = ""
        key = " "
        while key != "\n":
            key = input_queue.get()
            if key == "\n":
                break
            input_string += key
            self.show_input(input_string)
        exit_on_q.set()#arm the exit on q bool
        return input_string

class add_class(popup_class):
    def activate_option(self):
        self.width = 45
        self.activate_popup("enter item name: (enter to submit)")
        input_string = self.get_input() #get input using the the input method
        shopping_list.items.append([input_string, 1]) #append the string to the shopping list
        exit_on_q.set()#arm the exit on q bool
        interface.stdscr.clear()
        interface.print_menu()
        interface.print_shopping_list()

class remove_class(popup_class):
    def activate_option(self):
        self.width = 45
        self.activate_popup("remove: (enter to submit)")
        input_string = self.get_input() #get input using the the input method
        iterator = 0
        while iterator < len(shopping_list.items):#loop through list
            if shopping_list.items[iterator][0] == input_string: #find all matches
                shopping_list.items.pop(iterator)#pop all indexes that matches
            iterator += 1
        exit_on_q.set()#arm the exit on q bool
        interface.stdscr.clear()
        interface.print_menu()
        interface.print_shopping_list()

class save_class(popup_class):
    def activate_option(self):
        self.activate_popup("file name to save to: (enter to submit)")
        input_string = self.get_input() #get input using the the input method
        try:
            file_to_write = open(input_string + ".shoppinglist", "w") #open the file specified by user
            file_to_write.write(json.dumps(shopping_list.items)) #dump current shoppinglist as json
            file_to_write.close() #close file
        except:
            print(f"error: couldn't write to file")
        interface.stdscr.clear() #refresh terminal to remove popup
        interface.print_menu()
        interface.print_shopping_list()

class load_class(popup_class):
    def activate_option(self):
        self.activate_popup("enter list to load: (enter to submit)")
        input_string = self.get_input() #get input using the the input method
        try:
            file_load = open(input_string + ".shoppinglist", "r+") #open the file defailt.shoppinglist
            load_string = file_load.read() #read the file into a json string
            file_load.close()
            new_items = json.loads(load_string) #parse the json into the items list
            for iterator in range(len(new_items)):
                shopping_list.items.append(new_items[iterator])
        except:
            print(f"error: couldn't read from file")
        interface.stdscr.clear() #refresh terminal to remove popup
        interface.print_menu()
        interface.print_shopping_list()

def move_down(pane):#this will move the selected item down in the list
    if pane == "shopping_list" and shopping_list.selected < (len(shopping_list.items) - 1):#check if the variable is at the highest index already
        item = shopping_list.items.pop(shopping_list.selected)#pop the item and store it in a variable
        shopping_list.items.insert((shopping_list.selected + 1), item)#inser at higher index
        shopping_list.selected += 1#move the selection
        interface.print_shopping_list()#reprint the shopping list

def select_down(pane):
    if pane == "menu" and menu.selected < (len(menu.options) - 1):
        menu.selected += 1
        interface.print_menu()
    elif pane == "shopping_list" and shopping_list.selected < (len(shopping_list.items) - 1):
        shopping_list.selected += 1
        interface.print_shopping_list()

def move_up(pane):#this will move the selected item up in the list
    if pane == "shopping_list" and shopping_list.selected != 0: #check if we are already on top of the list
        item = shopping_list.items.pop(shopping_list.selected) #pop the item and put it in a variable
        shopping_list.items.insert((shopping_list.selected - 1), item) #insert the item at a lower index
        shopping_list.selected -= 1 #move the selection to match the item movement
        interface.print_shopping_list() #reprint the shopping list to display the update

def select_up(pane):
    if pane == "menu" and menu.selected != 0:
        menu.selected -= 1
        interface.print_menu()
    elif pane == "shopping_list" and shopping_list.selected != 0:
        shopping_list.selected -= 1
        interface.print_shopping_list()

def remove_item():
    try:
        shopping_list.items.pop(shopping_list.selected)
        interface.stdscr.clear()#flush the screen as the list gets shorter
        select_up("shopping_list")#move selection, update interface
        interface.print_menu()
        interface.print_shopping_list()
    except:
        print(f'error: shoppinglist is empty, cant delete item {str(shopping_list.selected)}')

def main():
    input_thread.start()
    selected_pane = "menu"

    for iterator in range(len(menu.options)):
        try:
            menu.options[iterator][1].set_coords()
        except:
            print(f'{menu.options[iterator][0]} doesnt have a popup function')
    while True:
        exit_on_q.set() #arm the exit on q bool for the input thread
        key = input_queue.get() #get the keypress from fifo queue
        if key == "q": #python doesn't have switch case and this has to call functions, thus dictonary is too much hassle
            break
        elif key == "d":
            remove_item()
        elif key == "m":
            move_up(selected_pane)
        elif key == "n":
            move_down(selected_pane)
        elif key == "j":
            select_down(selected_pane)
        elif key == "k":
            select_up(selected_pane)
        elif key == "h":
            selected_pane = "menu"#set selection
            interface.menu_select_symbol = ">"#set new selection symbols
            interface.shopping_list_select_symbol = "-"
            interface.print_menu()#update cli
            interface.print_shopping_list()
        elif key == "l":
            selected_pane = "shopping_list"#set selection
            interface.menu_select_symbol = "-"#set new selection symbols
            interface.shopping_list_select_symbol = ">"
            interface.print_menu()#update cli
            interface.print_shopping_list()
        elif key == " " or key == "\n":
            menu.activate()
    input_thread.join()#when the loop is broken we will wait for the interface thread to join the main thread

menu = menu_class()#this is the menu class
shopping_list = shopping_list_class()#the actual shopping list
input_queue = queue.Queue()#this makes it possible to read and send data between threads
exit_on_q = threading.Event()#exit the input loop when q is pressed when this is set
input_thread = input_thread_class() #this creates a thread for the input
interface = interface_class()#the interface class (which is a thread)
main()#starts main