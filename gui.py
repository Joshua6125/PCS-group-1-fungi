import tkinter
import numpy as np

from config import SPORE, sim_parameters, colors, state_names

import threading
import queue

from transitions import ProbToxinSim

# Implement the default Matplotlib key bindings.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches


sim = ProbToxinSim(sim_parameters)
sim.set_state(sim_parameters["n"]//2, sim_parameters["n"]//2, SPORE)


def dict_to_grid(state_dict):
    """Convert sparse dictionary state into a dense grid for plotting,
    expanding bounds."""
    if not state_dict:
        # Default small grid
        return np.zeros((sim_parameters["n"], sim_parameters["n"]))

    xs = [x for _, x in state_dict.keys()]
    ys = [y for y, _ in state_dict.keys()]

    # Determine bounds
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Add padding
    pad = 5
    min_x -= pad
    max_x += pad
    min_y -= pad
    max_y += pad

    height = max_y - min_y + 1
    width = max_x - min_x + 1

    dense = np.zeros((height, width))
    for (y, x), val in state_dict.items():
        dense[y - min_y, x - min_x] = val
    return dense


root = tkinter.Tk()
root.wm_title("FFR simulation")

cmap = ListedColormap(colors)
fig, ax = plt.subplots()
grid_data = dict_to_grid(sim.state_grid)
im = ax.imshow(grid_data, origin='lower', cmap=cmap,
               vmin=0, vmax=len(colors)-1)

patches = [mpatches.Patch(color=col, label=lab)
           for col, lab in zip(colors, state_names)]
legend = ax.legend(handles=patches, bbox_to_anchor=(
    1.05, 1), loc=2, borderaxespad=0.)
colorbar = plt.colorbar(im, label="Toxicity value")
colorbar.ax.set_visible(False)

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
    data = dict_to_grid(sim.state_grid)
    im.set_data(data)
    h, w = data.shape
    im.set_extent((-0.5, w-0.5, -0.5, h-0.5))
    ax.set_xlim(-0.5, w-0.5)
    ax.set_ylim(-0.5, h-0.5)
    canvas.draw()

    global view
    if view == "Toxins":
        switch_view()


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
        update_queue.put((sim.state_grid, sim.toxicity_grid))
    root.after(0, on_simulation_finished)


def check_queue():
    global check_queue_id
    if not root.winfo_exists():
        return

    new_data_pair = None
    try:
        while True:
            new_data_pair = update_queue.get_nowait()
    except queue.Empty:
        pass

    if new_data_pair is not None and\
       new_data_pair[0] is not None and\
       new_data_pair[1] is not None:
        state_data, toxin_data = new_data_pair

        if view == "CA":
            grid = dict_to_grid(state_data)
            im.set_cmap(cmap)
            im.set_clim(0, len(colors) - 1)

            legend.set_visible(True)
            colorbar.ax.set_visible(False)
        else:
            grid = dict_to_grid(toxin_data)
            im.set_cmap('viridis')
            im.set_clim(0, 1.0)
            legend.set_visible(False)
            colorbar.ax.set_visible(True)

        im.set_data(grid)
        h, w = dict_to_grid(state_data).shape
        im.set_extent((-0.5, w-0.5, -0.5, h-0.5))
        ax.set_xlim(-0.5, w-0.5)
        ax.set_ylim(-0.5, h-0.5)
        ratio, hull = sim.inner_ring_detector()
        hull_x = [point.x for point in hull]
        hull_y = [point.y for point in hull]
        inner_ring_detector.config(text=f"outer hull ratio: {round(ratio, 2)}")
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
                                            command=update_prob_spore_to_hyphae,
                                            label="Probability spore to hyphae")
slider_prob_spore_to_hyphae.set(sim_parameters["prob_spore_to_hyphae"])


def update_prob_spread(new_val):
    sim_parameters["prob_spread"] = float(new_val.replace(',', '.'))
    sim.change_parameters(sim_parameters)


slider_prob_spread = tkinter.Scale(slider_frame, from_=0, to=1, digits=3,
                                   resolution=0.05, orient=tkinter.HORIZONTAL,
                                   command=update_prob_spread,
                                   label="Probability of spreading")
slider_prob_spread.set(sim_parameters["prob_spread"])


def update_toxin_threshold(new_val):
    sim_parameters["toxin_threshold"] = float(new_val.replace(',', '.'))
    sim.change_parameters(sim_parameters)


slider_toxin_threshold = tkinter.Scale(slider_frame, from_=0, to=1, digits=3,
                                       resolution=0.05,
                                       orient=tkinter.HORIZONTAL,
                                       command=update_toxin_threshold,
                                       label="Toxin threshold")
slider_toxin_threshold.set(sim_parameters["toxin_threshold"])


def update_toxin_decay(new_val):
    sim_parameters["toxin_decay"] = float(new_val.replace(',', '.'))
    sim.change_parameters(sim_parameters)


slider_toxin_decay = tkinter.Scale(slider_frame, from_=0, to=0.1, digits=3,
                                   resolution=0.005, orient=tkinter.HORIZONTAL,
                                   command=update_toxin_decay,
                                   label="Toxin decay")
slider_toxin_decay.set(sim_parameters["toxin_decay"])


slider_prob_spore_to_hyphae.grid(
    in_=slider_frame, row=0, column=0, padx=5, pady=5)
slider_prob_spread.grid(in_=slider_frame, row=0, column=1, padx=5, pady=5)
slider_toxin_decay.grid(in_=slider_frame, row=1, column=0, padx=5, pady=5)
slider_toxin_threshold.grid(in_=slider_frame, row=1, column=1, padx=5, pady=5)


button_quit.pack(side=tkinter.BOTTOM)

sim_control_frame.pack(side=tkinter.BOTTOM)

slider_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)

view = "CA"

inner_ring_detector = tkinter.Label(root, text=f"Relative size outer rings: {1}")
inner_ring_detector.pack(side=tkinter.BOTTOM)

def switch_view():
    global view
    view = "CA" if view == "Toxins" else "Toxins"
    button_switch_view.config(text="Show CA" if view ==
                              "Toxins" else "Show toxins")
    if sim.state_grid and sim.toxicity_grid:
        update_queue.put((sim.state_grid, sim.toxicity_grid))


button_switch_view = tkinter.Button(root, text="Show toxins", command=switch_view)


button_switch_view = tkinter.Button(
    root, text="Show toxins", command=switch_view)
button_switch_view.pack(side=tkinter.BOTTOM)

toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

check_queue()
tkinter.mainloop()
