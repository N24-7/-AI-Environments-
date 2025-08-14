import tkinter as tk
from tkinter import messagebox
import random
import math
from datetime import datetime

class DynamicEnvironmentGUI:
        def __init__(self, master):
            self.master = master
            self.master.title("Dynamic Environment")
            self.num_agents = 0
            self.num_states = 0
            self.agent_positions = []
            self.state_positions = []
            self.agent_canvas_ids = []  # Store tuples of (circle_id, text_id) for agents
            self.state_canvas_ids = []  # Same for states
            self.canvas_width = 800
            self.canvas_height = 600
            self.small_font = ("Arial", 9)
            self.log_entries = []
            self.setup_ui()

        def setup_ui(self):
            self.left_frame = tk.Frame(self.master)
            self.left_frame.pack(side=tk.LEFT, padx=5, pady=5)
            self.right_frame = tk.Frame(self.master)
            self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

            self.canvas = tk.Canvas(self.right_frame, width=self.canvas_width, height=self.canvas_height, bg="white")
            self.canvas.pack()

            def add_labeled_entry(label_text):
                tk.Label(self.left_frame, text=label_text, font=self.small_font).pack(anchor="w")
                entry = tk.Entry(self.left_frame, font=self.small_font, width=20)
                entry.pack(pady=1)
                return entry

            self.area_entry = add_labeled_entry("Area (e.g. 800x600):")
            self.agent_entry = add_labeled_entry("Number of Agents:")
            self.state_entry = add_labeled_entry("Number of States:")

            tk.Button(self.left_frame, text="Start Environment", command=self.start_environment,
                    font=self.small_font).pack(pady=4)

            self.add_state_entry = tk.Entry(self.left_frame, font=self.small_font, width=20)
            self.add_state_entry.pack(pady=1)
            tk.Button(self.left_frame, text="Add States", command=self.add_states,
                    font=self.small_font).pack(pady=1)
            tk.Button(self.left_frame, text="Delete States", command=self.delete_states,
                    font=self.small_font).pack(pady=1)

            self.add_agent_entry = tk.Entry(self.left_frame, font=self.small_font, width=20)
            self.add_agent_entry.pack(pady=1)
            tk.Button(self.left_frame, text="Add Agents", command=self.add_agents,
                    font=self.small_font).pack(pady=1)
            tk.Button(self.left_frame, text="Delete Agents", command=self.delete_agents,
                    font=self.small_font).pack(pady=1)
            tk.Button(self.left_frame, text="Reset", command=self.reset_env, font=self.small_font).pack(pady=4)

            self.log_text = tk.Text(self.left_frame, font=self.small_font, width=24, height=15, wrap="word", state="disabled")
            self.log_text.pack(pady=4)

        def log(self, action, count, entity):
            timestamp = datetime.now().strftime("%H:%M:%S")
            symbol = "➕" if action == "Added" else "➖"
            entry = f"[{timestamp}] {symbol} {action} {count} {entity}\n"
            self.log_text.configure(state="normal")
            self.log_text.insert(tk.END, entry)
            self.log_text.configure(state="disabled")
            self.log_text.yview(tk.END)  # Auto-scroll to bottom

        def start_environment(self):
            try:
                area = self.area_entry.get().strip()
                if area:
                    self.canvas_width, self.canvas_height = map(int, area.lower().split("x"))
                    self.canvas.config(width=self.canvas_width, height=self.canvas_height)
                self.num_agents = max(0, int(self.agent_entry.get()))
                self.num_states = max(0, int(self.state_entry.get()))
                # Clear previous data
                self.agent_positions.clear()
                self.state_positions.clear()
                self.agent_canvas_ids.clear()
                self.state_canvas_ids.clear()
                self.canvas.delete("all")
                # Draw all agents and states from scratch
                self.draw_states(self.num_states)
                self.draw_agents(self.num_agents)
            except:
                messagebox.showerror("Error", "Invalid input. Check area and numbers.")

        def overlaps(self, x, y, r, positions, r2):
            pad = 4
            return any(math.hypot(x - ox, y - oy) < r + r2 + pad for ox, oy in positions)

        def random_position(self, existing, r, r2):
            for _ in range(1000):
                x = random.randint(r, self.canvas_width - r)
                y = random.randint(r, self.canvas_height - r)
                if not self.overlaps(x, y, r, existing, r2):
                    return x, y
            return None, None

        def draw_states(self, count):
            min_dim = min(self.canvas_width, self.canvas_height)
            state_radius = max(15, min_dim // 30)

            for _ in range(count):
                x, y = self.random_position(self.state_positions + self.agent_positions, state_radius, state_radius)
                if x is None:
                    messagebox.showwarning("Warning", "Some states couldn't be placed.")
                    break
                self.state_positions.append((x, y))
                circle_id = self.canvas.create_oval(x - state_radius, y - state_radius, x + state_radius, y + state_radius, fill="red")
                text_id = self.canvas.create_text(x, y, text=f"S{len(self.state_positions)}", font=("Arial", 10), fill="white")
                self.state_canvas_ids.append((circle_id, text_id))

        def draw_agents(self, count):
            min_dim = min(self.canvas_width, self.canvas_height)
            agent_radius = max(8, min_dim // 60)

            for _ in range(count):
                x, y = self.random_position(self.state_positions + self.agent_positions, agent_radius, agent_radius)
                if x is None:
                    messagebox.showwarning("Warning", "Some agents couldn't be placed.")
                    break
                self.agent_positions.append((x, y))
                circle_id = self.canvas.create_oval(x - agent_radius, y - agent_radius, x + agent_radius, y + agent_radius, fill="skyblue")
                text_id = self.canvas.create_text(x, y, text=f"A{len(self.agent_positions)}", font=("Arial", 8), fill="black")
                self.agent_canvas_ids.append((circle_id, text_id))

        def add_states(self):
            try:
                count = int(self.add_state_entry.get())
                if count > 0:
                    self.draw_states(count)
                    self.num_states += count
                    self.log("Added", count, "states")
            except:
                messagebox.showerror("Error", "Invalid number for states.")

        def delete_states(self):
            try:
                count = int(self.add_state_entry.get())
                if count > 0:
                    deleted = min(count, self.num_states)
                    for _ in range(deleted):
                        circle_id, text_id = self.state_canvas_ids.pop()
                        self.canvas.delete(circle_id)
                        self.canvas.delete(text_id)
                        self.state_positions.pop()
                    self.num_states -= deleted
                    self.log("Deleted", deleted, "states")
            except:
                messagebox.showerror("Error", "Invalid number for states.")

        def add_agents(self):
            try:
                count = int(self.add_agent_entry.get())
                if count > 0:
                    self.draw_agents(count)
                    self.num_agents += count
                    self.log("Added", count, "agents")
            except:
                messagebox.showerror("Error", "Invalid number for agents.")

        def delete_agents(self):
            try:
                count = int(self.add_agent_entry.get())
                if count > 0:
                    deleted = min(count, self.num_agents)
                    for _ in range(deleted):
                        circle_id, text_id = self.agent_canvas_ids.pop()
                        self.canvas.delete(circle_id)
                        self.canvas.delete(text_id)
                        self.agent_positions.pop()
                    self.num_agents -= deleted
                    self.log("Deleted", deleted, "agents")
            except:
                messagebox.showerror("Error", "Invalid number for agents.")

        def reset_env(self):
            self.agent_positions.clear()
            self.state_positions.clear()
            self.agent_canvas_ids.clear()
            self.state_canvas_ids.clear()
            self.num_agents = 0
            self.num_states = 0
            self.canvas.delete("all")
            self.agent_entry.delete(0, tk.END)
            self.state_entry.delete(0, tk.END)
            self.add_agent_entry.delete(0, tk.END)
            self.add_state_entry.delete(0, tk.END)
            self.area_entry.delete(0, tk.END)
            self.log_text.configure(state="normal")
            self.log_text.delete(1.0, tk.END)
            self.log_text.configure(state="disabled")

root = tk.Tk()
app = DynamicEnvironmentGUI(root)
root.mainloop()
