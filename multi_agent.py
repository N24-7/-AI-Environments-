import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import random
import math

AGENT_RADIUS_BASE = 10  # Minimum base size for an agent

class MultiAgentEnvironment:
    def __init__(self, master):
        self.master = master
        self.master.title("Multi-Agent Environment")

        # --- Left Panel ---
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, anchor='nw', fill=tk.Y, padx=10, pady=10)

        self.label_size = tk.Label(self.left_frame, text="Enter size (width x height):")
        self.label_size.pack(anchor='nw', pady=2)

        self.entry_size = tk.Entry(self.left_frame)
        self.entry_size.pack(anchor='nw', pady=2)

        self.label_agents = tk.Label(self.left_frame, text="Enter number of agents:")
        self.label_agents.pack(anchor='nw', pady=2)

        self.entry_agents = tk.Entry(self.left_frame)
        self.entry_agents.pack(anchor='nw', pady=2)

        self.start_button = tk.Button(self.left_frame, text="Create Simulation", command=self.create_environment)
        self.start_button.pack(anchor='nw', pady=5)

        # --- Right Panel (Canvas with Scrollbars) ---
        self.right_frame = tk.Frame(master, width=800, height=600, bg="gray90")
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        self.right_frame.pack_propagate(False)

        self.canvas = tk.Canvas(self.right_frame, bg="white")
        self.h_scrollbar = tk.Scrollbar(self.right_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.v_scrollbar = tk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.canvas.yview)

        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Font for agent labels
        self.label_font = tkfont.Font(family="Helvetica", size=10, weight="bold")

    def create_environment(self):
        size_input = self.entry_size.get().lower().replace(' ', '')
        agent_input = self.entry_agents.get()

        if 'x' not in size_input:
            messagebox.showerror("Invalid Format", "Use format: width x height (e.g. 400x300).")
            return

        try:
            width_str, height_str = size_input.split('x')
            width = int(width_str)
            height = int(height_str)

            if width <= 2 * AGENT_RADIUS_BASE or height <= 2 * AGENT_RADIUS_BASE:
                raise ValueError("Size too small for agents.")

            num_agents = int(agent_input)
            if num_agents <= 0:
                raise ValueError("Number of agents must be positive.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, width, height))
        self.canvas.config(width=min(800, width), height=min(600, height))
        self.canvas.create_rectangle(0, 0, width, height, outline="lightgray")

        self.deploy_agents(width, height, num_agents)

    def deploy_agents(self, width, height, num_agents):
        positions = []
        max_attempts = 1000

        for i in range(1, num_agents + 1):
            label = f"A{i}"
            label_width = self.label_font.measure(label)
            label_height = self.label_font.metrics("linespace")
            # Ensure circle radius fits the text with padding
            radius = int(max(AGENT_RADIUS_BASE, 0.6 * max(label_width, label_height)))

            for attempt in range(max_attempts):
                x = random.randint(radius, width - radius)
                y = random.randint(radius, height - radius)

                # Ensure no overlap
                if all(math.hypot(x - px, y - py) > (radius + pr) for (px, py, pr) in positions):
                    positions.append((x, y, radius))

                    # Draw the agent circle
                    self.canvas.create_oval(
                        x - radius, y - radius,
                        x + radius, y + radius,
                        fill="red", outline="black"
                    )

                    # Draw the label centered
                    self.canvas.create_text(
                        x, y,
                        text=label,
                        fill="white",
                        font=self.label_font
                    )
                    break
            else:
                messagebox.showwarning("Placement Warning", f"Only placed {len(positions)} out of {num_agents} agents.")
                break

# --- Run the Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MultiAgentEnvironment(root)
    root.mainloop()
