import tkinter

import numpy as np

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure

root = tkinter.Tk()
root.wm_title("Embedded in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
ax = fig.add_subplot()
line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
ax.set_xlabel("time [s]")
ax.set_ylabel("f(t)")

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)

button_quit = tkinter.Button(master=root, text="Quit", command=root.destroy)

slider_frame = tkinter.Frame(root)
slider_frame.columnconfigure(0, weight=1)
slider_frame.columnconfigure(1, weight=1)

def update_prob_spore_to_hyphae(new_val):
    canvas.draw()
slider_prob_spore_to_hyphae = tkinter.Scale(slider_frame, from_=0, to=1, digits=3, resolution=0.05, orient=tkinter.HORIZONTAL,
                              command=update_prob_spore_to_hyphae, label="Probability spore to hyphae")

def update_prob_spread(new_val):
    canvas.draw()
slider_prob_spread = tkinter.Scale(slider_frame, from_=0, to=1, digits=3, resolution=0.05, orient=tkinter.HORIZONTAL,
                              command=update_prob_spread, label="Probability of spreading")

def update_toxin_treshold(new_val):
    canvas.draw()
slider_toxin_treshold = tkinter.Scale(slider_frame, from_=0, to=1, digits=3, resolution=0.05, orient=tkinter.HORIZONTAL,
                              command=update_toxin_treshold, label="Toxin treshold")

def update_toxin_decay(new_val):
    canvas.draw()
slider_toxin_decay = tkinter.Scale(slider_frame, from_=0, to=1, digits=3, resolution=0.05, orient=tkinter.HORIZONTAL,
                              command=update_toxin_decay, label="Toxin decay")


slider_prob_spore_to_hyphae.grid(in_=slider_frame, row=0, column=0, padx=5, pady=5)
slider_prob_spread.grid(in_=slider_frame, row=0, column=1, padx=5, pady=5)
slider_toxin_decay.grid(in_=slider_frame, row=1, column=0, padx=5, pady=5)
slider_toxin_treshold.grid(in_=slider_frame, row=1, column=1, padx=5, pady=5)

button_quit.pack(side=tkinter.BOTTOM)

slider_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)

toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

tkinter.mainloop()