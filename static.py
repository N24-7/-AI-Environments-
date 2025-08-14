import tkinter as tk
from tkinter import messagebox
import random
import math

MAX_ATTEMPTS = 10000
STATE_PADDING = 2  # Minimal padding in small spaces


class StaticEnvironment:
    def __init__(self, master):
        self.master = master
        self.master.title("Agent and State Simulation")
        self.setup_ui()

    def setup_ui(self):
        lf = tk.Frame(self.master)
        lf.pack(side=tk.LEFT, padx=10, pady=10, anchor='n')
        for label, var in [
            ("Enter size (w x h):", 'size'),
            ("Number of agents:", 'agents'),
            ("Number of states:", 'states')
        ]:
            tk.Label(lf, text=label).pack(anchor='nw')
            setattr(self, f'entry_{var}', tk.Entry(lf))
            getattr(self, f'entry_' + var).pack(anchor='nw')
        tk.Button(lf, text="Create Simulation", command=self.create_environment).pack(pady=5)
        tk.Button(lf, text="Reset", command=self.reset_environment).pack(pady=5)


        rf = tk.Frame(self.master, width=800, height=600, bg="gray90")
        rf.pack(side=tk.RIGHT, padx=10, pady=10)
        rf.pack_propagate(False)
        self.canvas = tk.Canvas(rf, bg="white")
        hb = tk.Scrollbar(rf, orient=tk.HORIZONTAL, command=self.canvas.xview)
        vb = tk.Scrollbar(rf, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=hb.set, yscrollcommand=vb.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        vb.grid(row=0, column=1, sticky="ns")
        hb.grid(row=1, column=0, sticky="ew")
        rf.grid_rowconfigure(0, weight=1)
        rf.grid_columnconfigure(0, weight=1)

    def create_environment(self):
        s = self.entry_size.get().strip().lower().replace(' ', '')
        if 'x' not in s:
            return messagebox.showerror("Invalid Format", "Use format: width x height (e.g. 400x300).")
        try:
            W, H = map(int, s.split('x'))
            NA = int(self.entry_agents.get().strip())
            NS = int(self.entry_states.get().strip())
            if W <= 0 or H <= 0 or NA < 0 or NS < 0:
                raise ValueError
        except Exception:
            return messagebox.showerror("Invalid Input", "Please enter valid, non-negative values.")

        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, W, H), width=min(800, W), height=min(600, H))
        self.canvas.create_rectangle(0, 0, W, H, outline="lightgray")

        self.deploy(W, H, NA, NS)
    def reset_environment(self):
        self.canvas.delete("all")  # Clear the canvas
        self.entry_size.delete(0, tk.END)       # Clear size input
        self.entry_agents.delete(0, tk.END)     # Clear agents input
        self.entry_states.delete(0, tk.END)     # Clear states input
        self.canvas.config(scrollregion=(0, 0, 0, 0))  # Reset scrollable area


    def deploy(self, W, H, NA, NS):
        # Dynamically size based on canvas
        min_dim = max(1, min(W, H))
        agent_radius = max(1, min(8, min_dim // 50))
        state_radius = max(2, min(20, min_dim // 25))

        all_positions = []

        # Place states
        state_positions = self.place_non_overlapping(NS, state_radius, W, H, all_positions)
        for i, (x, y, r) in enumerate(state_positions):
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red", outline="black")
            self.canvas.create_text(x, y, text=f"S{i+1}", font=("Arial", max(4, int(r))), fill="white")
            all_positions.append((x, y, r))

        # Place agents
        agent_positions = self.place_non_overlapping(NA, agent_radius, W, H, all_positions)
        for i, (x, y, r) in enumerate(agent_positions):
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="skyblue", outline="black")
            self.canvas.create_text(x, y, text=f"A{i+1}", font=("Arial", max(3, int(r))), fill="black")
            all_positions.append((x, y, r))

    def place_non_overlapping(self, count, radius, W, H, existing_positions):
        placed = []
        attempts = 0
        while len(placed) < count and attempts < MAX_ATTEMPTS:
            x = random.uniform(radius, W - radius)
            y = random.uniform(radius, H - radius)
            if all(math.hypot(x - px, y - py) > (radius + pr + STATE_PADDING)
                   for px, py, pr in existing_positions + placed):
                placed.append((x, y, radius))
            attempts += 1
        return placed

root = tk.Tk()
app = StaticEnvironment(root)
root.mainloop()
