import tkinter as tk
from tkinter import messagebox
import random

AGENT_RADIUS = 10  # Agent visual radius

class SingleAgentEnvironment:
    def __init__(self, master):
        self.master = master
        self.master.title("Single Agent Environment")

        # --- Left Panel ---
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor='n')

        self.label_size = tk.Label(self.left_frame, text="Enter size (width x height):")
        self.label_size.pack(anchor='nw')

        self.entry_size = tk.Entry(self.left_frame)
        self.entry_size.pack(anchor='nw')

        self.start_button = tk.Button(self.left_frame, text="Create Simulation", command=self.create_environment)
        self.start_button.pack(pady=5, anchor='nw')

        self.reset_button = tk.Button(self.left_frame, text="Reset", command=self.reset_environment)
        self.reset_button.pack(pady=5, anchor='nw')


        # --- Right Panel (Canvas with Scrollbars) ---
        self.right_frame = tk.Frame(master, width=800, height=600, bg="gray90")
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        self.right_frame.pack_propagate(False)

        # Scrollable canvas setup
        self.canvas = tk.Canvas(self.right_frame, bg="white")
        self.h_scrollbar = tk.Scrollbar(self.right_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.v_scrollbar = tk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.canvas.yview)

        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

    def create_environment(self):
        size_input = self.entry_size.get().lower().replace(' ', '')
        if 'x' not in size_input:
            messagebox.showerror("Invalid Format", "Use format: width x height (e.g. 400x300).")
            return

        try:
            width_str, height_str = size_input.split('x')
            width = int(width_str)
            height = int(height_str)

            if width <= 2 * AGENT_RADIUS or height <= 2 * AGENT_RADIUS:
                raise ValueError("Size too small for agent.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        # Clear existing canvas content
        self.canvas.delete("all")

        # Resize scrollable area
        self.canvas.config(scrollregion=(0, 0, width, height))
        self.canvas.config(width=min(800, width), height=min(600, height))

        # Draw environment area border
        self.canvas.create_rectangle(0, 0, width, height, outline="lightgray")

        # Deploy agent
        self.deploy_agent(width, height)

    def deploy_agent(self, width, height):
        x = random.randint(AGENT_RADIUS, width - AGENT_RADIUS)
        y = random.randint(AGENT_RADIUS, height - AGENT_RADIUS)

        self.canvas.create_oval(
            x - AGENT_RADIUS, y - AGENT_RADIUS,
            x + AGENT_RADIUS, y + AGENT_RADIUS,
            fill="blue", outline="black"
        )
    def reset_environment(self):
        self.canvas.delete("all")               # Clears all drawings from the canvas
        self.entry_size.delete(0, tk.END)       # Clears the text input field
        self.canvas.config(scrollregion=(0, 0, 0, 0))  # Resets the scrollable region

    

# --- Run the Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SingleAgentEnvironment(root)
    root.mainloop()
