from interface.setup import main_interface
import tkinter as tk

def run_interface(portfolio):
    root = tk.Tk()
    main_interface(root, portfolio)
    root.mainloop()