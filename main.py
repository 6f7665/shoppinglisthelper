from threading import Thread
try:
    import tkinter as tk
except:
    print('''tkinter couldnt initialize, if you are using GNU/Linux try running any of these commands:\n"pip install tk"\n"pacman -S tk"\n"echo 'dev-lang/python tk' >> /etc/portage/package.use/python; emerge -uvDU @world"''')
    exit(1)

#interface class with non specific functors
class interface_class(Thread):
    sidebar_info = ""
    shopping_list = ""
    def set_sidebar_info(self, sidebar_info_to_set):
        self.sidebar_info = sidebar_info_to_set
    def set_shopping_list(self, shopping_list_to_set):
        self.shopping_list = shopping_list_to_set

#tk_interface based on interface class
class tk_interface_class(interface_class):
    def run(self):
        self.window = tk.Tk()
        self.window.title("Shopping List Assistant")
        self.side_panel = tk.Frame(master=self.window, width=200, height=500, bg="#202020")
        self.side_panel.pack(fill=tk.Y, side=tk.LEFT, expand=False)
        self.main_panel = tk.Canvas(self.window, width=600, height=500, bg="black", highlightthickness=0)
        self.main_panel.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.main_panel.create_line(100, 100, 200, 50, fill = "#204090", width = 3)
        self.window.bind('<KeyPress>', self.keypress_handler)
        self.window.mainloop()
        global action
        action = "exit"
    def keypress_handler(self, event):
        global action
        action = str(event.keysym)
    def destroy_interface(self):
        self.window.quit()
        self.window.destroys()

action = "none"

def main():
    #start the interface
    interface = tk_interface_class()
    interface.start()

    #setup variables
    option_list = ["a = add", "d = delete", "j = down", "k = up", "q = quit"]

    global action
    for i in range(3000):
        if action == "a":
            print("add")
        elif action == "q":
            interface.destroy_interface()
            break
        elif action == "exit": #someone pressed the x
            print(action)
            break
        print(action)
        action = "none"

    #this destroys the window and closes the program
    print(action)
    interface.join()
    exit(0)

main()