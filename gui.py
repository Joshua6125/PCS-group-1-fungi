import tkinter
import numpy as np

from config import SPORE, sim_parameters

import threading
import queue

from transitions import ProbToxinSim

# Implement the default Matplotlib key bindings.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap

colors = [(0, 0.4, 0), (1, 1, 1), (1, .8, .8), (1, .4, .4),
          (.8, 0, 0), (0.4, 0.2, 0), (.4, .4, 0), (.1, .2, 0), (.1, .2, 0)]

sim = ProbToxinSim(sim_parameters)
sim.set_state(sim_parameters["n"]//2, sim_parameters["n"]//2, SPORE)


def state_dict_to_grid(state_dict, n):
    """Convert sparse dictionary state into a dense n x n grid for plotting."""
    dense = np.zeros((n, n), dtype=int)
    for (y, x), val in state_dict.items():
        if 0 <= y < n and 0 <= x < n:
            dense[y, x] = val
    return dense

root = tkinter.Tk()
root.wm_title("FFR simulation")

cmap = ListedColormap(colors)
fig, ax = plt.subplots()
im = ax.imshow(state_dict_to_grid(
    sim.state_grids[-1], sim_parameters["n"]), origin='lower', cmap=cmap, vmin=0, vmax=len(colors)-1)


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

def on_closing():
    global check_queue_id
    if check_queue_id:
        root.after_cancel(check_queue_id)
        check_queue_id = None
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
button_quit = tkinter.Button(master=root, text="Quit", command=on_closing)

sim_control_frame = tkinter.Frame(root)
sim_control_frame.columnconfigure(0, weight=1)
sim_control_frame.columnconfigure(1, weight=1)
sim_control_frame.columnconfigure(2, weight=1)
iter_amount_var = tkinter.StringVar(sim_control_frame)
iter_amount_var.set("10")
iter_amount_spinbox = tkinter.Spinbox(
    sim_control_frame, from_=1, to=100, textvariable=iter_amount_var)
iter_amount_spinbox.grid(in_=sim_control_frame, row=0, column=0)

update_queue = queue.Queue()


def reset_simulation():
    sim.reset()
    sim.set_state(sim_parameters["n"]//2, sim_parameters["n"]//2, SPORE)
    im.set_data(state_dict_to_grid(sim.state_grids[-1], sim_parameters["n"]))
    canvas.draw()


def on_simulation_finished():
    run_for_button.config(state="normal")
    button_reset.config(state="normal")


def run_iterations():
    run_for_button.config(state="disabled")
    button_reset.config(state="disabled")
    n = int(iter_amount_var.get())
    threading.Thread(target=sim_worker, args=(n,), daemon=True).start()


def sim_worker(n):
    for _ in range(n):
        sim.step()
        update_queue.put(state_dict_to_grid(
            sim.state_grids[-1], sim_parameters["n"]))
    root.after(0, on_simulation_finished)


check_queue_id = None

def check_queue():
    global check_queue_id
    if not root.winfo_exists():
        return

    new_data = None
    try:
        while True:
            new_data = update_queue.get_nowait()
    except queue.Empty:
        pass

    if new_data is not None:
        im.set_data(new_data)
        canvas.draw()
    check_queue_id = root.after(20, check_queue)


run_for_button = tkinter.Button(
    sim_control_frame, text="Run for n iterations", command=run_iterations)
run_for_button.grid(in_=sim_control_frame, row=0, column=1)

button_reset = tkinter.Button(
    sim_control_frame, text="Reset", command=reset_simulation)
button_reset.grid(in_=sim_control_frame, row=0, column=2)


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


def update_toxin_threshold(new_val):
    sim_parameters["toxin_threshold"] = float(new_val.replace(',', '.'))
    sim.change_parameters(sim_parameters)


slider_toxin_threshold = tkinter.Scale(slider_frame, from_=0, to=1, digits=3, resolution=0.05, orient=tkinter.HORIZONTAL,
                                      command=update_toxin_threshold, label="Toxin threshold")
slider_toxin_threshold.set(sim_parameters["toxin_threshold"])


def update_toxin_decay(new_val):
    sim_parameters["toxin_decay"] = float(new_val.replace(',', '.'))
    sim.change_parameters(sim_parameters)


slider_toxin_decay = tkinter.Scale(slider_frame, from_=0, to=0.1, digits=3, resolution=0.005, orient=tkinter.HORIZONTAL,
                                   command=update_toxin_decay, label="Toxin decay")
slider_toxin_decay.set(sim_parameters["toxin_decay"])


slider_prob_spore_to_hyphae.grid(
    in_=slider_frame, row=0, column=0, padx=5, pady=5)
slider_prob_spread.grid(in_=slider_frame, row=0, column=1, padx=5, pady=5)
slider_toxin_decay.grid(in_=slider_frame, row=1, column=0, padx=5, pady=5)
slider_toxin_threshold.grid(in_=slider_frame, row=1, column=1, padx=5, pady=5)

button_quit.pack(side=tkinter.BOTTOM)

sim_control_frame.pack(side=tkinter.BOTTOM)

slider_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)

toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

check_queue()
tkinter.mainloop()
