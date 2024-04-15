import tkinter as tk
from AutoRefreshShop import AutoRefreshShop
from tkinter import messagebox

class AutoRefreshShopGUI:
    def __init__(self, master):
        self.master = master
        master.title("Auto Refresh Shop")
        self.cost_label = tk.Label(master, text="Gold:")
        self.cost_label.grid(row=0, column=0, sticky="w")
        self.cost_entry = tk.Entry(master)
        self.cost_entry.grid(row=0, column=1, sticky='ew')

        self.ss_label = tk.Label(master, text="Sky stone:")
        self.ss_label.grid(row=1, column=0, sticky="w")
        self.ss_entry = tk.Entry(master)
        self.ss_entry.grid(row=1, column=1, sticky='ew')

        self.window_title_label = tk.Label(master, text="Window Title:")
        self.window_title_label.grid(row=2, column=0, sticky="w")
        self.window_title_entry = tk.Entry(master)
        self.window_title_entry.grid(row=2, column=1, sticky='ew')

        self.run_button = tk.Button(master, text="Run", command=self.run_auto)
        self.run_button.grid(row=3, column=0)
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_auto)
        self.stop_button.grid(row=3, column=1)

        self.bm_label = tk.Label(master, text="BM:")
        self.bm_label.grid(row=5, column=0)
        self.mys_label = tk.Label(master, text="MYS:")
        self.mys_label.grid(row=5, column=1)

        self.auto_refresh_shop = None

    def run_auto(self):
        if not self.auto_refresh_shop or not self.auto_refresh_shop.is_alive():
            cost = int(self.cost_entry.get())
            ss = int(self.ss_entry.get())
            window_title = str(self.window_title_entry.get())
            self.auto_refresh_shop = AutoRefreshShop(
                self.master, cost, ss, window_title, self.update_results
            )
            self.auto_refresh_shop.start()
        else:
            print("Auto Refresh is already running.")

    def stop_auto(self):
        if self.auto_refresh_shop and self.auto_refresh_shop.is_alive():

            self.auto_refresh_shop.running = False
            self.auto_refresh_shop.join()

            bm, mys = self.auto_refresh_shop.get_current_state()

            self.update_results(bm, mys)

            print("Auto Refresh stopped.")
        else:
            print("Auto Refresh is not running.")

    def update_results(self, bm, mys):
        self.bm_label.config(text=f"BM: {bm}")
        self.mys_label.config(text=f"MYS: {mys}")
        messagebox.showwarning("Warning", "Completed")


    