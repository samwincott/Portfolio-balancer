import tkinter as tk
from tkinter.filedialog import askopenfilename
# from tkinter import scrolledtext

class main_interface():

    def __init__(self, master, portfolio):
        self.master = master
        self.portfolio = portfolio
        self.invest_amount = tk.Entry(master,width=10)
        self.title = tk.Label(master, text="Portfolio", font=("Arial Bold", 30))
        self.invest_label = tk.Label(master, text="Amount: ", font=("Arial Bold", 10))
        self.invest_button = tk.Button(master, text="Click Me", command=self.invest)
        self.load_button = tk.Button(master, text="Load Portfolio", command=self.load_portfolio)

        master.title("Lazy balancer")
        master.geometry('350x200')

        self.title.grid(column=0, row=0)
        self.load_button.grid(column=2, row=0)
        self.invest_label.grid(column=0, row=1)
        self.invest_amount.grid(column=1, row=1)
        self.invest_button.grid(column=2, row=1)

    def load_portfolio(self):
        filename = askopenfilename()
        self.portfolio.load_from_file(filename)
        # self.portfolio.pretty_print()
        self.msg = tk.Message(self.master, text=self.portfolio.get_data())
        self.msg.grid(column=0, row=3)

    def invest(self):
        amount = float(self.invest_amount.get())
        self.portfolio.allocate_funds(amount)
