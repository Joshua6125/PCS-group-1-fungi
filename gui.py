import tkinter
import numpy as np

from constants import *

import threading
import queue

from transitions import BasicToxinSim
from utils import gkern

# Implement the default Matplotlib key bindings.
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

sim_parameters = {
    "n": 75,
    "prob_spore_to_hyphae": 1.0,
    "prob_mushroom": 0.7,
    "prob_spread": 0.5,
    "toxin_threshold": 0.3,
    "toxin_decay": 0.05,
    "toxin_convolution": gkern(5, 1, 1)
}

colors = [(0, 1, 0), (0, 0.5, 0.5), (0, 0, 0.5), (0, 0, 1),
          (1, 0, 0), (0.5, 0.5, 0), (0, 0, 0), (0, 0, 0), (1, 1, 1)]

sim = BasicToxinSim(sim_parameters)
sim.set_state(sim_parameters["n"]//2, sim_parameters["n"]//2, SPORE)

root = tkinter.Tk()
root.wm_title("FFR simulation")

cmap = LinearSegmentedColormap.from_list("cmap_name", colors, N=10)
fig, ax = plt.subplots()
ax.imshow(sim.state_grids[-1], origin='lower', cmap=cmap)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

button_quit = tkinter.Button(master=root, text="Quit", command=root.destroy)

sim_control_frame = tkinter.Frame(root)
sim_control_frame.columnconfigure(0, weight=1)
sim_control_frame.columnconfigure(1, weight=1)
iter_amount_var = tkinter.StringVar(sim_control_frame)
iter_amount_var.set("10")
iter_amount_spinbox = tkinter.Spinbox(
    sim_control_frame, from_=1, to=100, textvariable=iter_amount_var)
iter_amount_spinbox.grid(in_=sim_control_frame, row=0, column=0)

update_queue = queue.Queue()


def run_iterations():
    n = int(iter_amount_var.get())
    threading.Thread(target=sim_worker, args=(n,), daemon=True).start()
    root.after(100, check_queue)


def sim_worker(n):
    for _ in range(n):
        sim.step()
        update_queue.put(sim.state_grids[-1].copy())


def check_queue():
    if not root.winfo_exists():
        return

    new_data = None
    try:
        while True:
            new_data = update_queue.get_nowait()
    except queue.Empty:
        pass

    if new_data is not None:
        ax.imshow(sim.state_grids[-1], origin='lower', cmap=cmap)
        canvas.draw()
    root.after(20, check_queue)


run_for_button = tkinter.Button(
    sim_control_frame, text="Run for n iterations", command=run_iterations)
run_for_button.grid(in_=sim_control_frame, row=0, column=1)

slider_frame = tkinter.Frame(root)
slider_frame.columnconfigure(0, weight=1)
slider_frame.columnconfigure(1, weight=1)


def update_prob_spore_to_hyphae(new_val):
    sim_parameters["prob_spore_to_hyphae"] = float(new_val.replace(',', '.'))
    sim.change_parameters(sim_parameters)


slider_prob_spore_to_hyphae = tkinter.Scale(slider_frame, from_=0, to=1,
                                            digits=3, resolution=0.05,
                                            orient=tkinter.HORIZONTAL,
                                            command=update_prob_spore_to_hyphae, label="Probability spore to hyphae")
slider_prob_spore_to_hyphae.set(sim_parameters["prob_spore_to_hyphae"])


def update_prob_spread(new_val):
    sim_parameters["prob_spread"] = float(new_val.replace(',', '.'))
    sim.change_parameters(sim_parameters)


slider_prob_spread = tkinter.Scale(slider_frame, from_=0, to=1, digits=3, resolution=0.05, orient=tkinter.HORIZONTAL,
                                   command=update_prob_spread, label="Probability of spreading")
slider_prob_spread.set(sim_parameters["prob_spread"])


def update_toxin_treshold(new_val):
    sim_parameters["toxin_treshold"] = float(new_val.replace(',', '.'))
    sim.change_parameters(sim_parameters)


slider_toxin_treshold = tkinter.Scale(slider_frame, from_=0, to=1, digits=3, resolution=0.05, orient=tkinter.HORIZONTAL,
                                      command=update_toxin_treshold, label="Toxin treshold")
slider_toxin_treshold.set(sim_parameters["toxin_threshold"])


def update_toxin_decay(new_val):
    sim_parameters["toxin_decay"] = float(new_val.replace(',', '.'))
    sim.change_parameters(sim_parameters)


slider_toxin_decay = tkinter.Scale(slider_frame, from_=0, to=1, digits=3, resolution=0.05, orient=tkinter.HORIZONTAL,
                                   command=update_toxin_decay, label="Toxin decay")
slider_toxin_decay.set(sim_parameters["toxin_decay"])


slider_prob_spore_to_hyphae.grid(
    in_=slider_frame, row=0, column=0, padx=5, pady=5)
slider_prob_spread.grid(in_=slider_frame, row=0, column=1, padx=5, pady=5)
slider_toxin_decay.grid(in_=slider_frame, row=1, column=0, padx=5, pady=5)
slider_toxin_treshold.grid(in_=slider_frame, row=1, column=1, padx=5, pady=5)

button_quit.pack(side=tkinter.BOTTOM)

sim_control_frame.pack(side=tkinter.BOTTOM)

slider_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)

toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

tkinter.mainloop()
