
try:
    import tkinter as tk
except:
    print('''tkinter couldnt initialize, if you are using GNU/Linux try running any of these commands:\n"pip install tk"\n"pacman -S tk"\n"echo 'dev-lang/python tk' >> /etc/portage/package.use/python; emerge -uvDU @world"''')
    exit(1)

def main():
    window = tk.Tk() #create a tk window object
    window.title("Shopping List Assistant 3000") #heckin poggers innit?

    side_panel = tk.Frame(master=window, width=200, height=400, bg="green")
    main_panel = tk.Frame(master=window, width=200, height=400, bg="black")

    window.mainloop()

main()