import tkinter as tk
from config import config

def update(val, attr):
    setattr(config, attr, int(val))

root = tk.Tk()
root.title("Virtual Mouse Control Panel")

# smoothing slider
tk.Label(root, text="Smoothing").pack()
tk.Scale(root, from_=1, to=15,
         orient="horizontal",
         command=lambda v: update(v, "SMOOTHING")).pack()

# toggles
tk.Label(root, text="Features").pack()

click_var = tk.IntVar(value=1)

tk.Checkbutton(root, text="Enable Click",
               variable=click_var,
               command=lambda: setattr(config, "ENABLE_CLICK", bool(click_var.get()))
               ).pack()

tk.Button(root, text="Start App",
          command=lambda: exec(open("main.py").read())
          ).pack()

root.mainloop()