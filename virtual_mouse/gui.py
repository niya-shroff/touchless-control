import tkinter as tk
from config import config
import threading
import main

def start_main():
    threading.Thread(target=main.run, daemon=True).start()

def start():
    root = tk.Tk()
    root.title("Virtual Mouse Control Panel")

    tk.Label(root, text="Smoothing").pack()

    tk.Scale(root,
             from_=1,
             to=15,
             orient="horizontal",
             command=lambda v: setattr(config, "SMOOTHING", int(v))
             ).pack()

    tk.Button(root, text="Start Tracking", command=start_main).pack()

    root.mainloop()