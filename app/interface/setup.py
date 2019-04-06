import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
# from tkinter import scrolledtext

class main_interface():

    def __init__(self, master, portfolio):
        self.master = master
        self.portfolio = portfolio

        self.title = tk.Label(master, text="Portfolio", font=("Arial Bold", 30))
        self.invest_button = tk.Button(master, text="Invest", command = self.invest)
        self.load_button = tk.Button(master, text="Load Portfolio", command=self.load_portfolio)
        self.save_button = tk.Button(master, text="Save Portfolio", command=self.save_portfolio)
        # self.buy_shares_button = tk.Button(master, text="Buy individual shares", command=self.buy_shares)
        # self.sell_shares_button = tk.Button(master, text="Sell individual shares", command=self.save_portfolio)

        master.title("Lazy balancer")
        master.geometry('500x700')

        self.title.grid(row=0, column=0)
        self.load_button.grid(row=1, column=0)
        self.save_button.grid(row=1, column=1)

        self.invest_button.grid(row=2, column=0)
        # self.buy_shares_button.grid(row=2, column=1)
        # self.sell_shares_button.grid(row=2, column=2)

    def load_portfolio(self):
        filename = askopenfilename()
        self.portfolio.load(filename)
        self.msg = tk.Message(self.master, text=str(self.portfolio))
        self.msg.grid(column=0, row=3)

    def save_portfolio(self):
        filename = asksaveasfilename()
        self.portfolio.save(filename)

    def invest(self):
        def tmp():
            amount = float(invest_amount.get())
            advice = self.portfolio.invest(amount)
            print(advice)
            print("got here")
        popup = tk.Tk()
        popup.wm_title("Invest")
        invest_amount = tk.Entry(popup,width=10)
        invest_amount.pack()
        invest_button = tk.Button(popup, text="Invest", command = tmp)
        invest_button.pack()
        B1 = tk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()



        # self.msg = tk.Message(self.master, text=str(self.portfolio))
        # self.msg.grid(column=0, row=3)
        # messagebox.showinfo("Advice", advice)

    # def buy_shares(self):
    #     popup = tk.Tk()
    #     popup_title = tk.Label(popup, text="Buy")
    #     popup_title.grid(column=0, row=0)

    def popupmsg(self, msg):
        popup = tk.Tk()
        popup.wm_title("!")
        self.invest_amount = tk.Entry(popup,width=10)
        label = tk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()
