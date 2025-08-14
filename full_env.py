import tkinter as tk
from tkinter import ttk, simpledialog, messagebox,filedialog
import tkinter.font as tkfont
import math, random, datetime
from datetime import datetime as dt
from PIL import Image, ImageTk

# Constants
AGENT_RADIUS = 10
MAX_ATTEMPTS = 10000
STATE_PADDING = 2

# Descriptions and image
IMAGE_DIR = r"C:\Users\mitta\Desktop\Agentic AI\images"
current_image = None
descriptions = {
    "Environment": "The external context in which an agent operates.",
    "Fully Observable": "A fully observable environment is one in which the agent has complete access to all relevant information about the environment’s current state through its sensors. There is no hidden or unknown data, so the agent can make decisions based solely on the current percept.\n\nExample: A game of chess, where the positions of all pieces are visible to both players.",
    "Partially Observable":"A partially observable environment is one where the agent has incomplete or noisy information about the current state of the environment due to limited sensors or hidden variables. The agent may need to guess, infer, or remember past observations to make good decisions.\n\nExample: Driving a car in fog, where the agent cannot see all obstacles or vehicles clearly.",
    "Deterministic": "A deterministic environment is one in which the outcome of every action is completely predictable—given the current state and the agent’s action, the next state is always the same. There is no randomness or uncertainty involved, so the agent doesn’t need to consider probabilities while making decisions.\n\nExample: Solving a maze where each move (e.g., go left or right) always leads to the same specific location.",
    "Stochastic": "A stochastic environment is one in which the outcomes of actions are uncertain or probabilistic. Even if the agent performs the same action in the same situation, the result may vary due to randomness or unpredictable external factors. The agent must therefore plan for multiple possible outcomes and often use probabilities or expectations to make decisions.\n\nExample: A robot walking on a slippery floor—when it tries to move forward, it might sometimes slip sideways instead.",
    "Episodic": "An episodic environment is one where the agent’s experience is divided into separate episodes, and each episode is independent of the others. The agent’s actions in one episode do not affect future episodes, so no memory or planning is required across time.\n\nExample: Classifying images or detecting spam emails — each case is handled independently.",
    "Sequential": "A sequential environment is one where the agent’s current actions affect not just the present outcome but also future states and decisions. The agent must consider the long-term impact of its actions and often needs memory or planning.\n\nExample: Playing chess or driving a car, where each move or turn influences what happens next.",
    "Static": "A static environment is one that does not change while the agent is thinking or deciding. It remains fixed unless the agent takes an action, meaning there is no time pressure or external interference. This allows the agent to take as much time as needed to plan its moves.\n\nExample: A crossword puzzle—nothing changes until the solver fills in a word.",
    "Dynamic": "A dynamic environment is one that can change on its own over time, even while the agent is deciding what to do. The agent must act quickly and continuously, as delays in decision-making can lead to outdated or incorrect actions.\n\nExample: Driving in traffic—other vehicles, pedestrians, and traffic signals keep changing regardless of the driver’s actions.",
    "Discrete": "A discrete environment is one in which the number of possible states, actions, and time steps is finite or countable. The environment can be broken down into clearly defined parts, making it easier to represent and solve using logic or search algorithms.\n\nExample: A board game like chess, where positions and moves occur in distinct, separate steps.",
    "Continuous": "A continuous environment is one where the states, actions, or time can take on an infinite number of values, often represented by real numbers. The agent must handle smooth, uninterrupted changes, and decisions often involve complex calculations like calculus or control theory.\n\nExample: Flying a drone, where position, speed, and direction change in a continuous manner.",
    "Single agent": "A single-agent environment is one in which only one agent is actively making decisions and interacting with the environment. There are no other intelligent entities whose actions influence the outcomes, so the agent can focus solely on its own goals without needing to account for opponents or collaborators.\n\nExample: Solving a maze or playing a solo puzzle game like Sudoku.",
    "Multi agent": "A multi-agent environment is one where two or more agents operate and interact, each with their own goals or tasks. These agents can be cooperative, competitive, or a mix of both, meaning an agent’s success may depend on the actions of others.\n\nExample: A soccer match, where players (agents) on both teams interact, compete, and coordinate in real time.",
    "Sequential Environment": "A simulation environment where operations are applied step-by-step on an initial number, showing results graphically.",
    
    "Agents": "Entities that perceive their environment and act upon it.",
    "Simple Reflex": "A simple reflex agent acts solely on the current percept, without using any memory of the past. It works by evaluating condition–action rules—essentially a list of \"if percept → then action\" statements. Such agents are fast and suitable for fully observable environments but fail when history or context matters.\n\nExample:\nIn the vacuum-cleaner world, a simple reflex agent could follow rules like:\n -If the current tile is dirty, then suck.\n -Else if the tile is clean, then move to the next tile.",
    "Model-Based": "A model-based agent is an improvement over a simple reflex agent—it maintains an internal model of the world to keep track of parts of the environment it cannot currently observe. This allows it to act based on both the current percept and its history or beliefs about the unseen state of the world.\n\nExample:\nIn the vacuum-cleaner world:\nA model-based agent remembers which tiles are already cleaned, so it doesn’t revisit them unnecessarily.\nEven if it can’t see the entire room at once, it can infer where dirt may still be left.",
    "Goal-Based": "A goal-based agent makes decisions by considering not just the current state of the environment, but also a specific goal it wants to achieve. It evaluates possible actions based on whether they move it closer to that goal, and may use search or planning algorithms to find a sequence of actions that lead to success.\n\nExample:\nIn the vacuum-cleaner world, a goal-based agent might have the goal:\n\“Clean the entire room.\”\nTo achieve this, it:\nKeeps track of what areas are dirty.\nPlans a path to reach and clean every dirty tile.\nChooses actions that reduce the number of dirty spots.",
    "Utility-Based": "Agents that act to maximize a utility function.",
    "Learning-Based": "Agents that can learn from experience to improve their performance over time.",
}

# Image paths
image_paths = {
    key: f"{IMAGE_DIR}\\{key.lower().replace(' ', '_').replace('-', '_')}.png"
    for key in descriptions
}


# Helper for labeled Entry
def labeled_entry(parent, text):
    tk.Label(parent, text=text).pack(anchor='nw', pady=2)
    entry = tk.Entry(parent)
    entry.pack(anchor='nw', pady=2)
    return entry

#Shows a confirmation dialog and closes the window if user confirms.
def confirm_close(window):
    if messagebox.askyesno("Close Confirmation", "Your previous data is not saved. Do you still want to close this window?"):
        window.destroy()

# Global session history(Store house for export option)
session_log = {
    "episodic": [],
    "sequential": [],
    "static": [],
    "multi_agent": [],
    "single_agent": []
}
#export function
def export_to_file(content, title="Export"):
    file_path = filedialog.asksaveasfilename(
        title=title,
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            messagebox.showinfo("Export Successful", f"Data saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Error saving file:\n{e}")

def l1(parent, label):
    frame = tk.Frame(parent)
    lbl = tk.Label(frame, text=label, width=18, anchor="w")
    lbl.pack(side="left")
    entry = tk.Entry(frame, width=12)
    entry.pack(side="left")
    return frame, entry

def midpoint(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def point_in_polygon(point, polygon):
    x, y = point
    inside = False
    n = len(polygon)
    px1, py1 = polygon[0]
    for i in range(1, n + 1):
        px2, py2 = polygon[i % n]
        if y > min(py1, py2):
            if y <= max(py1, py2):
                if x <= max(px1, px2):
                    if py1 != py2:
                        xinters = (y - py1) * (px2 - px1) / (py2 - py1) + px1
                    if px1 == px2 or x <= xinters:
                        inside = not inside
        px1, py1 = px2, py2
    return inside

# Base class for environments with similar UI
class BaseEnvironment:
    def __init__(self, master, title):
        self.master = master
        self.master.title(title)
        self._setup_layout()

    def _setup_layout(self):
        # Left panel
        self.left = tk.Frame(self.master)
        self.left.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        # Right panel (canvas area)
        self.right = tk.Frame(self.master, bg="gray90")
        self.right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Canvas and scrollbars
        self.canvas = tk.Canvas(self.right, bg="white")
        hbar = tk.Scrollbar(self.right, orient='horizontal', command=self.canvas.xview)
        vbar = tk.Scrollbar(self.right, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self.canvas.grid(row=0, column=0, sticky='nsew')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='ew')

        # Make canvas expandable inside right frame
        self.right.grid_rowconfigure(0, weight=1)
        self.right.grid_columnconfigure(0, weight=1)

        # Make right frame expandable inside master
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def reset_canvas(self):
        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, 0, 0))
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
#static environment
class StaticEnvironment(BaseEnvironment):
    def __init__(self, master):
        super().__init__(master, "Static")
        self.session_log = []
        self.environment_snapshots = []

        self.entry_size = labeled_entry(self.left, "Area of terrain (eg:800x600)")
        self.entry_agents = labeled_entry(self.left, "Number of agents")
        self.entry_states = labeled_entry(self.left, "Number of states")

        tk.Button(self.left, text="Deploy", width=20, command=self.create_env).pack(pady=5)
        tk.Button(self.left, text="Environment Reset", width=20, command=self.reset_env).pack(pady=2)
        tk.Button(self.left, text="Export", width=20, command=self.export_log).pack(side="bottom", pady=10)

        self.status_label = tk.Label(
            self.left,
            text="",
            justify="left",
            anchor="w",
            wraplength=200,
            fg="darkgreen",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=(20, 0), fill="x")

        self.master.protocol("WM_DELETE_WINDOW", lambda: confirm_close(self.master))

    def update_status(self, message):
        self.status_label.config(text=message)
        self.session_log.append(message)

    def create_env(self):
        s = self.entry_size.get().replace(' ', '').lower()
        if 'x' not in s:
            return messagebox.showerror("Invalid Format", "Format: width x height (e.g. 400x300).")
        try:
            W, H = map(int, s.split('x'))
            NA, NS = int(self.entry_agents.get()), int(self.entry_states.get())
            if W <= 0 or H <= 0 or NA < 0 or NS < 0:
                raise ValueError
        except:
            return messagebox.showerror("Invalid Input", "Enter valid non-negative values.")

        self.reset_canvas()
        self.canvas.config(scrollregion=(0, 0, W, H), width=min(800, W), height=min(600, H))
        self.canvas.create_rectangle(0, 0, W, H, outline="lightgray")

        grid_spacing = 50
        for x in range(0, W + 1, grid_spacing):
            self.canvas.create_line(x, 0, x, H, fill="lightblue", dash=(2, 4))
            self.canvas.create_text(x + 2, H - 10, text=str(x), anchor="nw", font=("Arial", 7), fill="blue")
        for y in range(0, H + 1, grid_spacing):
            flipped_y = H - y
            self.canvas.create_line(0, flipped_y, W, flipped_y, fill="lightblue", dash=(2, 4))
            self.canvas.create_text(2, flipped_y - 2, text=str(y), anchor="sw", font=("Arial", 7), fill="blue")

        all_items = []
        min_dim = min(W, H)
        state_radius = max(2, min(20, min_dim // 25))
        agent_radius = max(1, min(8, min_dim // 50))

        state_items = self.place_items(W, H, state_radius, NS, all_items)
        all_items += state_items
        agent_items = self.place_items(W, H, agent_radius, NA, all_items)

        state_positions = [(x, y) for x, y, _ in state_items]
        agent_positions = [(x, y) for x, y, _ in agent_items]

        # Store full snapshot for export
        self.environment_snapshots.append({
            "width": W,
            "height": H,
            "states": state_positions,
            "agents": agent_positions
        })

        self.session_log.append("=" * 50)
        self.session_log.append(f"Created environment: Size {W}x{H}, Agents: {NA}, States: {NS}, Total items placed: {len(state_items) + len(agent_items)}")
        self.update_status(f"Deployed {NA} agent(s) and {NS} state(s) randomly on {W}×{H} terrain.")

        def draw_states(index=0):
            if index < len(state_items):
                x, y, r = state_items[index]
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="#FFF2CC", outline="black")
                self.canvas.create_text(x, y, text=f"S{index+1}", font=("Arial", max(4, int(r))), fill="black")
                self.master.after(100, lambda: draw_states(index + 1))
            else:
                self.master.after(100, draw_agents)

        def draw_agents(index=0):
            if index < len(agent_items):
                x, y, r = agent_items[index]
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="#EDEDED", outline="black")
                self.canvas.create_text(x, y, text=f"A{index+1}", font=("Arial", max(4, int(r))), fill="black")
                self.master.after(100, lambda: draw_agents(index + 1))

        self.master.after(100, draw_states)
    def place_items(self, W, H, r, count, existing):
        placed, attempts = [], 0
        while len(placed) < count and attempts < MAX_ATTEMPTS:
            x, y = random.uniform(r, W - r), random.uniform(r, H - r)
            if all(math.hypot(x - px, y - py) > (r + pr + STATE_PADDING) for px, py, pr in existing + placed):
                placed.append((x, y, r))
            attempts += 1
        return placed

    def reset_env(self):
        for entry in [self.entry_size, self.entry_agents, self.entry_states]:
            entry.delete(0, tk.END)
        self.reset_canvas()
        self.session_log.append("-" * 50)
        self.session_log.append("Environment Reset.")
        self.session_log.append("-" * 50)
        self.update_status("Environment reset. Ready for new input.")

    def export_log(self):
        if not self.session_log:
            return messagebox.showinfo("Export", "No session data to export.")

        try:
            output = []
            output.append("Agentic AI")
            output.append("Static Agent")
            output.append("=" * 50)

            for line in self.session_log:
                output.append(line)

            # Export full environment snapshots
            for idx, snap in enumerate(self.environment_snapshots):
                output.append("=" * 50)
                output.append(f"Environment {idx + 1}: {snap['width']}x{snap['height']}")
                output.append("State Coordinates:")
                for i, (x, y) in enumerate(snap["states"], 1):
                    output.append(f"  S{i}: ({x:.1f}, {y:.1f})")
                output.append("Agent Coords:")
                for i, (x, y) in enumerate(snap["agents"], 1):
                    output.append(f"  A{i}: ({x:.1f}, {y:.1f})")

            output.append("-" * 50)

            export_to_file('\n'.join(output), "Export Static Environment Log")

        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred during export:\n{str(e)}")


# Single-Agent Environment
class SingleAgentEnvironment(BaseEnvironment):
    def __init__(self, master):
        super().__init__(master, "Single agent Environment")
        self.entry_size = labeled_entry(self.left, "Area of terrain (eg:800x600)")
        self.master.protocol("WM_DELETE_WINDOW", lambda: confirm_close(self.master))

        tk.Button(self.left, text="Deploy", width=20, command=self.create_env).pack(pady=5)
        tk.Button(self.left, text="Environment reset", width=20, command=self.reset_env).pack(pady=5)
        tk.Button(self.left, text="Export", width=20, command=self.export_log).pack(side="bottom", pady=10)

        self.status_label = tk.Label(
            self.left,
            text="",
            justify="left",
            anchor="w",
            wraplength=200,
            fg="darkgreen",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=(20, 0), fill="x")

        self.session_log = []
        self.environment_snapshots = []

        self.canvas_width = self.canvas_height = 0
        self.agent_position = None

    def update_status(self, message):
        self.status_label.config(text=message)
        self.session_log.append(message)

    def create_env(self):
        s = self.entry_size.get().replace(' ', '').lower()
        if 'x' not in s:
            return messagebox.showerror("Invalid Format", "Format: width x height (e.g. 400x300).")
        try:
            W, H = map(int, s.split('x'))
            if W <= 2 * AGENT_RADIUS or H <= 2 * AGENT_RADIUS:
                raise ValueError("Size too small.")
        except ValueError as e:
            return messagebox.showerror("Invalid Input", str(e))

        self.canvas_width, self.canvas_height = W, H
        self.reset_canvas()
        self.canvas.config(scrollregion=(0, 0, W, H), width=min(800, W), height=min(600, H))
        self.canvas.create_rectangle(0, 0, W, H, outline="lightgray")

        # Draw grid
        grid_spacing = 50
        for x in range(0, W + 1, grid_spacing):
            self.canvas.create_line(x, 0, x, H, fill="lightblue", dash=(2, 4))
            self.canvas.create_text(x + 2, H - 10, text=str(x), anchor="nw", font=("Arial", 7), fill="blue")
        for y in range(0, H + 1, grid_spacing):
            flipped_y = H - y
            self.canvas.create_line(0, flipped_y, W, flipped_y, fill="lightblue", dash=(2, 4))
            self.canvas.create_text(2, flipped_y - 2, text=str(y), anchor="sw", font=("Arial", 7), fill="blue")

        x = random.randint(AGENT_RADIUS, W - AGENT_RADIUS)
        y = random.randint(AGENT_RADIUS, H - AGENT_RADIUS)

        self.canvas.create_oval(
            x - AGENT_RADIUS, y - AGENT_RADIUS,
            x + AGENT_RADIUS, y + AGENT_RADIUS,
            fill="#EDEDED", outline="black"
        )

        self.agent_position = (x, y)

        # Log environment
        self.environment_snapshots.append({
            "width": W,
            "height": H,
            "agent": (x, y)
        })

        self.session_log.append("=" * 50)
        self.session_log.append(f"Created environment: Size {W}x{H}")
        self.update_status(f"Deployed 1 agent randomly on {W}×{H} terrain.")

    def reset_env(self):
        self.entry_size.delete(0, tk.END)
        self.reset_canvas()
        self.agent_position = None
        self.session_log.append("-" * 50)
        self.session_log.append("Environment reset.")
        self.session_log.append("-" * 50)
        self.update_status("Environment reset. Ready for new deployment.")

    def export_log(self):
        if not self.environment_snapshots:
            return messagebox.showinfo("Export", "No session data to export.")

        try:
            output = []
            output.append("Agentic AI")
            output.append("Single Agent")
            output.append("=" * 50)

            for line in self.session_log:
                output.append(line)

            for idx, snap in enumerate(self.environment_snapshots):
                output.append("=" * 50)
                output.append(f"Environment {idx + 1}: {snap['width']}x{snap['height']}")
                output.append("Agent Coordinates:")
                x, y = snap["agent"]
                output.append(f"  A1: ({x:.1f}, {y:.1f})")

            output.append("-" * 50)
            export_to_file('\n'.join(output), "Single_Agent_Environment_Log.txt")

        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred during export:\n{str(e)}")


# Multi-Agent Environment
class MultiAgentEnvironment(BaseEnvironment):
    def __init__(self, master):
        super().__init__(master, "Multi agent Environment ")
        self.entry_size = labeled_entry(self.left, "Area of terrain (eg:800x600)")
        self.entry_agents = labeled_entry(self.left, "Number of agents")
        self.label_font = tkfont.Font(family="Helvetica", size=10, weight="bold")
        self.master.protocol("WM_DELETE_WINDOW", lambda: confirm_close(self.master))

        tk.Button(self.left, text="Deploy", width=20, command=self.create_env).pack(pady=5)
        tk.Button(self.left, text="Environment reset", width=20, command=self.reset_env).pack(pady=2)
        tk.Button(self.left, text="Export", width=20, command=self.export_log).pack(side="bottom", pady=5)

        self.status_label = tk.Label(
            self.left,
            text="",
            justify="left",
            anchor="w",
            wraplength=200,
            fg="darkgreen",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=(20, 0), fill="x")

        self.session_log = []  # Clear old header, will add in export
        self.environment_snapshots = []

        self.agent_positions = []
        self.canvas_width = self.canvas_height = 0

    def update_status(self, message):
        self.status_label.config(text=message)

    def create_env(self):
        s = self.entry_size.get().replace(' ', '').lower()
        if 'x' not in s:
            return messagebox.showerror("Invalid Format", "Format: width x height.")
        try:
            W, H = map(int, s.split('x'))
            NA = int(self.entry_agents.get())
            if W <= 2 * AGENT_RADIUS or H <= 2 * AGENT_RADIUS:
                raise ValueError("Size too small.")
            if NA <= 0:
                raise ValueError("Number of agents must be positive.")
        except ValueError as e:
            return messagebox.showerror("Invalid Input", str(e))

        self.canvas_width, self.canvas_height = W, H
        self.reset_canvas()
        self.canvas.config(scrollregion=(0, 0, W, H), width=min(800, W), height=min(600, H))
        self.canvas.create_rectangle(0, 0, W, H, outline="lightgray")

        # Draw Cartesian grid with origin at bottom-left
        grid_spacing = 50
        for x in range(0, W + 1, grid_spacing):
            self.canvas.create_line(x, 0, x, H, fill="lightblue", dash=(2, 4))
            self.canvas.create_text(x + 2, H - 10, text=str(x), anchor="nw", font=("Arial", 7), fill="blue")

        for y in range(0, H + 1, grid_spacing):
            flipped_y = H - y
            self.canvas.create_line(0, flipped_y, W, flipped_y, fill="lightblue", dash=(2, 4))
            self.canvas.create_text(2, flipped_y - 2, text=str(y), anchor="sw", font=("Arial", 7), fill="blue")

        self.update_status("Deploying agents...")
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.session_log.append("=" * 50)
        self.session_log.append(f"[{timestamp}] Deploying {NA} agent(s) on {W}×{H} terrain\n")

        self.agent_positions = []
        label_prefix = "A"  # Agents labeled A1, A2, ...

        def place_next_agent(index=1):
            if index > NA:
                self.update_status(f"Deployed {len(self.agent_positions)} agent(s) randomly on {W}×{H} terrain.")
                # Save snapshot after all agents deployed
                self.environment_snapshots.append({
                    "width": W,
                    "height": H,
                    "agents": [(pos[0], pos[1]) for pos in self.agent_positions]
                })
                return

            tag = f"{label_prefix}{index}"
            lw = self.label_font.measure(tag)
            radius = max(AGENT_RADIUS, int(0.6 * max(lw, self.label_font.metrics("linespace"))))

            for _ in range(MAX_ATTEMPTS):
                x, y = random.randint(radius, W - radius), random.randint(radius, H - radius)
                # Check minimum distance to existing agents
                if all(math.hypot(x - px, y - py) > (radius + pr + 2) for px, py, pr in self.agent_positions):
                    self.agent_positions.append((x, y, radius))
                    self.session_log.append(f"Agent {tag} at ({x},{y})\n")
                    self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#EDEDED", outline="black")
                    self.canvas.create_text(x, y, text=tag, font=self.label_font, fill="black")
                    break
            else:
                messagebox.showwarning("Placement Warning", f"Only {len(self.agent_positions)} out of {NA} agents could be placed.")
                self.update_status(f"Deployed {len(self.agent_positions)} agent(s) on {W}×{H} terrain.")
                self.session_log.append("-" * 40 + "\n")
                # Save snapshot even if partial
                self.environment_snapshots.append({
                    "width": W,
                    "height": H,
                    "agents": [(pos[0], pos[1]) for pos in self.agent_positions]
                })
                return

            self.master.after(100, lambda: place_next_agent(index + 1))

        self.master.after(100, place_next_agent)

    def reset_env(self):
        self.entry_size.delete(0, tk.END)
        self.entry_agents.delete(0, tk.END)
        self.reset_canvas()
        self.agent_positions = []
        self.update_status("Environment reset. Ready for new deployment.")
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.session_log.append(f"\n[{timestamp}] Environment reset.\n" + "-" * 50 + "\n")

    def export_log(self):
        if not self.environment_snapshots:
            return messagebox.showinfo("Export", "No session data to export.")

        output = []
        output.append("Agentic AI")
        output.append("Multi Agent")
        output.append("=" * 50)

        for idx, snap in enumerate(self.environment_snapshots):
            output.append(f"Created environment: Size {snap['width']}x{snap['height']}")
            output.append(f"Deployed {len(snap['agents'])} agent(s) randomly on {snap['width']}×{snap['height']} terrain.")
            output.append("Agent Coordinates:")
            for i, (x, y) in enumerate(snap["agents"], start=1):
                output.append(f"  A{i}: ({x:.1f}, {y:.1f})")
            output.append("-" * 50)

        export_to_file('\n'.join(output), "Multi_Agent_Environment_Log.txt")


# Episodic Environment
def open_episodic_env(parent):
    session_log["episodic"].clear()  # Clear old logs when opening new window
    win = tk.Toplevel(parent)
    win.title("Episodic Environment")
    win.geometry("700x350")
    win.protocol("WM_DELETE_WINDOW", lambda: confirm_close(win))

    last_selected = []
    last_total = 0

    tf, rf = tk.Frame(win), tk.Frame(win)
    tf.pack(side='left', fill='y', padx=10, pady=10)
    rf.pack(side='right', fill='both', expand=True, padx=10, pady=10)

    use_ts = tk.BooleanVar()

    # Define inputs
    tk.Label(tf, text="Total number of states:", width=25).pack(anchor='w', pady=2)
    total_e = tk.Entry(tf)
    total_e.pack(fill='x', pady=5)

    tk.Label(tf, text="Number to select:", width=25).pack(anchor='w', pady=2)
    select_e = tk.Entry(tf)
    select_e.pack(fill='x', pady=5)

    #for timestamps
    def render_states():
        nonlocal last_selected, last_total
        status_label.config(text=f"From deployed {last_total} states, {len(last_selected)} were selected randomly.")
        canvas.delete("all")
        cols = 10
        spacing = 60
        radius = 20
        now = datetime.datetime.now()

        result_log = []
        for i in range(last_total):
            row, col = divmod(i, cols)
            x, y = col * spacing + 50, row * spacing + 50
            color = "#0078d7" if i in last_selected else "#EDEDED"
        
            canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
            canvas.create_text(x, y, text=str(i))

            if i in last_selected and use_ts.get():
                ts = now + datetime.timedelta(seconds=last_selected.index(i) * random.randint(1, 5))
                ts_str = ts.strftime('%H:%M:%S')
                # Show timestamp below the circle
                canvas.create_text(x, y + 25, text=ts_str, font=("Arial", 8), fill="black")

                result_log.append(f"State: {i} at {ts.strftime('%Y-%m-%d %H:%M:%S')}\n")

        if result_log:
            log_entry = f"Input - Total States: {last_total}, Selected: {len(last_selected)}, With Timestamp: {use_ts.get()}\n"
            log_entry += ''.join(result_log)
            session_log["episodic"].append(log_entry)


    tk.Checkbutton(tf, text="Include Timestamps", variable=use_ts, command=render_states).pack(anchor='w', pady=5)
    canvas = tk.Canvas(rf, bg="white")
    canvas.pack(fill='both', expand=True)

    # Simulate logic
    def simulate():
        try:
            n, a = int(total_e.get()), int(select_e.get())
            if a > n:
                return messagebox.showerror("Error", "Cannot select more states than available.")
            sel = random.sample(range(n), a)
            nonlocal last_selected, last_total
            last_selected = sel
            last_total = n
            result_log = []

            render_states()
            cols = 10
            spacing = 60
            radius = 20

            now = datetime.datetime.now()
            result_log = []

            for i in range(n):
                row, col = divmod(i, cols)
                x, y = col * spacing + 50, row * spacing + 50
                color = "#0078d7" if i in sel else "#EDEDED"
                canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
                canvas.create_text(x, y, text=str(i))

                if i in sel and use_ts.get():
                    ts = now + datetime.timedelta(seconds=sel.index(i) * random.randint(1, 5))
                    result_log.append(f"State: {i} at {ts.strftime('%Y-%m-%d %H:%M:%S')}\n")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers.")

    def reset_fields():
        total_e.delete(0, tk.END)
        select_e.delete(0, tk.END)
        use_ts.set(False)
        canvas.delete("all")
        session_log["episodic"].clear()
        status_label.config(text="Environment reset. Ready for new input.")

    #Status message label
    status_label = tk.Label(tf, text="", fg="darkgreen", justify="left", wraplength=180, font=("Arial", 9))
    status_label.pack(pady=(10, 0), anchor="w")

    tk.Button(tf, text="Export",width=20, command=lambda: export_to_file('\n\n'.join(session_log["episodic"]), "Episodic Session Log")).pack(side = "bottom", pady=10)
    tk.Button(tf, text="Deploy",width=20, command=simulate).pack(pady=5)
    tk.Button(tf, text="Environment reset",width=20, command=reset_fields).pack(pady=2)


# Sequential Environment (unchanged)
def open_sequential_env():
    import math
    from tkinter import simpledialog, messagebox

    seq_win = tk.Toplevel(root)
    seq_win.title("Sequential Environment")
    seq_win.geometry("1200x480")
    seq_win.protocol("WM_DELETE_WINDOW", lambda: confirm_close(seq_win))
    state = {"current_step": 0, "result": 0, "total_steps": 0}
    session_log["sequential"].clear()

    ops = {
        1: lambda n, o: n + o,
        2: lambda n, o: n * o,
        3: lambda n, o: n - o,
        4: lambda n, o: n / o if o != 0 else (_ for _ in ()).throw(ValueError("Cannot divide by zero.")),
        5: lambda n, o: n ** o,
        6: lambda n, _: math.log10(n) if n > 0 else (_ for _ in ()).throw(ValueError("Log undefined for ≤0")),
        7: lambda n, _: math.sqrt(n) if n >= 0 else (_ for _ in ()).throw(ValueError("Sqrt undefined for <0")),
        8: lambda n, _: round(n)
    }
    need_operand = {1, 2, 3, 4, 5}
    op_labels = {
        1: "Add", 2: "Multiply", 3: "Subtract", 4: "Divide",
        5: "Power", 6: "Log base 10", 7: "Square Root", 8: "Round Off"
    }

    left_frame = tk.Frame(seq_win)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=10)
    right_frame = tk.Frame(seq_win)
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)

    def make_label_entry(parent, label_text):
        tk.Label(parent, text=label_text).pack(anchor="w")
        e = tk.Entry(parent)
        e.pack(fill=tk.X, pady=5)
        return e

    entry_input = make_label_entry(left_frame, "Enter a number")
    entry_operations = make_label_entry(left_frame, "Number of operations")
    label_step = tk.Label(left_frame, text="")
    label_step.pack(pady=10)
    frame_operations = tk.Frame(left_frame)
    frame_operations.pack(pady=10, fill=tk.X)

    for text, op in [
        ("Add (+)", 1), ("Multiply (×)", 2), ("Subtract (-)", 3),
        ("Divide (÷)", 4), ("Power (xʸ)", 5), ("Log base 10", 6),
        ("Square Root", 7), ("Round Off", 8)
    ]:
        tk.Button(frame_operations, text=text, command=lambda op=op: apply_operation(op), width=18).pack(pady=3)

    label_result = tk.Label(left_frame, text="Final Result:")
    label_result.pack(pady=15)

    def reset_env():
        for e in (entry_input, entry_operations):
            e.delete(0, tk.END)
        state.update({"current_step": 0, "result": 0, "total_steps": 0})
        label_step.config(text="")
        label_result.config(text="Final Result:")
        canvas.delete("all")
        frame_operations.pack_forget()
    tk.Button(left_frame, text="Start",width=20, command=lambda: start_operations()).pack(pady=5)
    tk.Button(left_frame, text="Environment reset",width=20, command=reset_env).pack(pady=5)
    tk.Button(left_frame, text="Export",width=20, command=lambda: export_to_file('\n'.join(session_log["sequential"]), "Export Sequential Log")).pack(side = "bottom", pady=10)

    canvas = tk.Canvas(right_frame, bg="#f0f0f0", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    frame_operations.pack_forget()

    def draw_step_circle(step, val):
        r_x, r_y, sp_x, sp_y, max_row = 70, 35, 190, 120, 4
        row, col = divmod(step, max_row)
        y, x_c = 80 + row * sp_y, 110 + col * sp_x
        canvas.create_oval(x_c - r_x, y - r_y, x_c + r_x, y + r_y, fill="#FFF2CC", outline="black", width=2)
        canvas.create_oval(x_c - r_x + 5, y - r_y + 5, x_c + r_x - 5, y + r_y - 5, fill="#FFF2CC", outline="")
        canvas.create_text(x_c, y, text=f"{round(val,6) if isinstance(val,float) else val}", fill="black")
        if step > 0:
            p = step - 1
            p_row, p_col = divmod(p, max_row)
            p_x, p_y = 110 + p_col * sp_x, 80 + p_row * sp_y
            if row == p_row:
                canvas.create_line(p_x + r_x, p_y, x_c - r_x, y, arrow=tk.LAST, width=4, fill="black", arrowshape=(20,25,10), smooth=True)
            else:
                off_x, off_y = 25, 15
                canvas.create_line(p_x + r_x, p_y, p_x + r_x + off_x, p_y, width=4, fill="black", smooth=True)
                canvas.create_line(p_x + r_x + off_x, p_y, p_x + r_x + off_x, y - r_y - off_y, width=4, fill="black", smooth=True)
                canvas.create_line(p_x + r_x + off_x, y - r_y - off_y, x_c - r_x, y - r_y - off_y, arrow=tk.LAST, width=4, fill="black", arrowshape=(20,25,10), smooth=True)

    def start_operations():
        try:
            user_input = float(entry_input.get())
            total = int(entry_operations.get())
            if total <= 0:
                messagebox.showerror("Input Error", "Number of operations must be positive.")
                return
            state.update({"result": user_input, "total_steps": total, "current_step": 0})
            session_log["sequential"].append(f"Initial Number: {user_input}, Steps: {total}")
            canvas.delete("all")
            draw_step_circle(0, user_input)
            label_step.config(text="Step 1: Choose operation")
            label_result.config(text="Final Result:")
            frame_operations.pack()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")

    def ask_next_operation():
        if state["current_step"] < state["total_steps"]:
            label_step.config(text=f"Step {state['current_step'] + 1}: Choose operation")
            frame_operations.pack()
        else:
            label_step.config(text="All operations done.")
            label_result.config(text=f"Final Result: {round(state['result'], 6)}")
            frame_operations.pack_forget()

    def apply_operation(op_choice):
        func = ops.get(op_choice)
        if not func:
            messagebox.showerror("Invalid Choice", "Choose a valid operation.")
            return
        try:
            if op_choice in need_operand:
                operand = simpledialog.askfloat("Input", "Enter the number for the operation")
                if operand is None:
                    return
                state["result"] = func(state["result"], operand)
                log_msg = f"Step {state['current_step']+1}: {op_labels[op_choice]} ({operand}) => Result: {round(state['result'],6)}"
            else:
                state["result"] = func(state["result"], None)
                log_msg = f"Step {state['current_step']+1}: {op_labels[op_choice]} => Result: {round(state['result'],6)}"
            state["current_step"] += 1
            draw_step_circle(state["current_step"], state["result"])
            session_log["sequential"].append(log_msg)
            ask_next_operation()
        except Exception as e:
            messagebox.showerror("Error", f"Operation failed: {e}")

#Dynamic Environment
def open_dynamic_env():
    class DynamicEnvironmentGUI:
        def __init__(self, master):
            self.master = master
            self.master.title("Dynamic Environment")
            self.num_agents = 0
            self.num_states = 0
            self.agent_positions = []
            self.state_positions = []
            self.agent_canvas_ids = []
            self.state_canvas_ids = []
            self.canvas_width = 800
            self.canvas_height = 600
            self.small_font = ("Arial", 9)
            self.session_log = []
            self.setup_ui()
            self.master.protocol("WM_DELETE_WINDOW", lambda: confirm_close(self.master))

        def setup_ui(self):
            self.left_frame = tk.Frame(self.master)
            self.left_frame.pack(side=tk.LEFT, padx=5, pady=5)

            self.right_frame = tk.Frame(self.master)
            self.right_frame.pack(side=tk.RIGHT, expand=True, fill="both")

            self.canvas_frame = tk.Frame(self.right_frame)
            self.canvas_frame.pack(expand=True, fill="both")

            self.canvas = tk.Canvas(self.canvas_frame, bg="white", bd=0, highlightthickness=0)
            self.hbar = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.vbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
            self.hbar.pack(side="bottom", fill="x")
            self.vbar.pack(side="right", fill="y")
            self.canvas.pack(side="left", expand=True, fill="both")
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
            self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)

            def add_labeled_entry(label_text):
                wrapper = tk.Frame(self.left_frame)
                wrapper.pack(fill="x", pady=2)
                label = tk.Label(wrapper, text=label_text, font=self.small_font, anchor="w", justify="left")
                label.pack(fill="x")
                entry = tk.Entry(wrapper, font=self.small_font, width=25)
                entry.pack()
                return entry

            self.area_entry = add_labeled_entry("Area of terrain (eg. 800x600):")
            self.agent_entry = add_labeled_entry("Number of Agents")
            self.state_entry = add_labeled_entry("Number of States")

            tk.Button(self.left_frame, text="Deploy", width=20, command=self.start_environment,
                      font=self.small_font).pack(pady=4)

            self.add_state_entry = tk.Entry(self.left_frame, font=self.small_font, width=25)
            self.add_state_entry.pack(pady=1)
            tk.Button(self.left_frame, text="Add States", width=20, command=self.add_states,
                      font=self.small_font).pack(pady=1)
            tk.Button(self.left_frame, text="Delete States", width=20, command=self.delete_states,
                      font=self.small_font).pack(pady=1)

            self.add_agent_entry = tk.Entry(self.left_frame, font=self.small_font, width=25)
            self.add_agent_entry.pack(pady=1)
            tk.Button(self.left_frame, text="Add Agents", width=20, command=self.add_agents,
                      font=self.small_font).pack(pady=1)
            tk.Button(self.left_frame, text="Delete Agents", width=20, command=self.delete_agents,
                      font=self.small_font).pack(pady=1)

            tk.Button(self.left_frame, text="Environment reset", width=20,
                      command=self.reset_env, font=self.small_font).pack(pady=4)
            
            tk.Button(self.left_frame, text="Export", width=20,
                      command=self.export_log, font=self.small_font,).pack(side="bottom",pady=4)

            self.log_text = tk.Text(self.left_frame, font=self.small_font, width=24, height=15, wrap="word", state="disabled")
            self.log_text.pack(pady=4)

        def _on_mousewheel(self, event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_shift_mousewheel(self, event):
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        def log(self, action, count, entity):
            timestamp = dt.now().strftime("%H:%M:%S")
            symbol = "➕" if action == "Added" else "➖" if action == "Deleted" else "●"
            entry = f"[{timestamp}] {symbol} {action} {count} {entity}\n"
            self.log_text.configure(state="normal")
            self.log_text.insert(tk.END, entry)
            self.log_text.configure(state="disabled")
            self.log_text.yview(tk.END)
            # Also add to session log
            self.session_log.append(entry.strip())

        def start_environment(self):
            try:
                area = self.area_entry.get().strip()
                if area:
                    w, h = map(int, area.lower().split("x"))
                    self.canvas_width, self.canvas_height = max(100, w), max(100, h)
                    self.canvas.config(width=min(800, self.canvas_width), height=min(600, self.canvas_height))
                self.num_agents = max(0, int(self.agent_entry.get()))
                self.num_states = max(0, int(self.state_entry.get()))

                # Clear previous positions and canvas items
                self.agent_positions.clear()
                self.state_positions.clear()
                for cid in self.agent_canvas_ids + self.state_canvas_ids:
                    self.canvas.delete(cid)
                self.agent_canvas_ids.clear()
                self.state_canvas_ids.clear()
                self.canvas.delete("all")

                # Log user inputs
                self.session_log.append("===== Agentic AI =====")
                self.session_log.append("===== Dynamic Environment =====")
                self.session_log.append("===== User Inputs =====")
                self.session_log.append(f"Terrain Size: {self.canvas_width}x{self.canvas_height}")
                self.session_log.append(f"Initial Agents: {self.num_agents}")
                self.session_log.append(f"Initial States: {self.num_states}")
                self.session_log.append("")

                # Draw grid lines
                gs = 50
                for xx in range(0, self.canvas_width + 1, gs):
                    self.canvas.create_line(xx, 0, xx, self.canvas_height, fill="lightblue", dash=(2, 4))
                    self.canvas.create_text(xx + 2, self.canvas_height - 10, text=str(xx), anchor="nw", font=self.small_font, fill="blue")
                for yy in range(0, self.canvas_height + 1, gs):
                    fy = self.canvas_height - yy
                    self.canvas.create_line(0, fy, self.canvas_width, fy, fill="lightblue", dash=(2, 4))
                    self.canvas.create_text(2, fy - 2, text=str(yy), anchor="sw", font=self.small_font, fill="blue")

                self.canvas.config(scrollregion=(0, 0, self.canvas_width, self.canvas_height))

                # Define callback to log initial positions after drawing
                def log_initial_positions():
                    self.session_log.append("\n===== Initial Positions =====")
                    for i, (x, y) in enumerate(self.state_positions, 1):
                        self.session_log.append(f"State S{i} at ({x}, {y})")
                    for i, (x, y) in enumerate(self.agent_positions, 1):
                        self.session_log.append(f"Agent A{i} at ({x}, {y})")
                    self.session_log.append("")
                    self.log("Deployed", f"{self.num_agents} agents and {self.num_states} states", "environment")

                # Draw states, then agents, then log
                self.draw_states(self.num_states, animated=True, done_callback=lambda:
                    self.draw_agents(self.num_agents, animated=True, done_callback=log_initial_positions)
                )

            except Exception as e:
                messagebox.showerror("Error", f"Invalid input. Check area and numbers.\n{e}")

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

        def draw_states(self, count, animated=True, done_callback=None):
            min_dim = min(self.canvas_width, self.canvas_height)
            r = max(15, min_dim // 30)
            def step(i=0):
                if i >= count:
                    if done_callback:
                        done_callback()
                    return
                x, y = self.random_position(self.state_positions + self.agent_positions, r, r)
                if x is None:
                    messagebox.showwarning("Warning", "Some states couldn't be placed.")
                    if done_callback:
                        done_callback()
                    return
                self.state_positions.append((x, y))
                cid = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="#FFF2CC")
                tid = self.canvas.create_text(x, y, text=f"S{len(self.state_positions)}", font=self.small_font, fill="black")
                self.state_canvas_ids.extend([cid, tid])
                # Log position
                self.session_log.append(f"Added State S{len(self.state_positions)} at ({x}, {y})")
                if animated:
                    self.master.after(100, lambda: step(i + 1))
                else:
                    step(i + 1)
            step()

        def draw_agents(self, count, animated=True, done_callback=None):
            min_dim = min(self.canvas_width, self.canvas_height)
            r = max(8, min_dim // 60)
            def step(i=0):
                if i >= count:
                    if done_callback:
                        done_callback()
                    return
                x, y = self.random_position(self.state_positions + self.agent_positions, r, r)
                if x is None:
                    messagebox.showwarning("Warning", "Some agents couldn't be placed.")
                    if done_callback:
                        done_callback()
                    return
                self.agent_positions.append((x, y))
                cid = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="#EDEDED")
                tid = self.canvas.create_text(x, y, text=f"A{len(self.agent_positions)}", font=self.small_font, fill="black")
                self.agent_canvas_ids.extend([cid, tid])
                # Log position
                self.session_log.append(f"Added Agent A{len(self.agent_positions)} at ({x}, {y})")
                if animated:
                    self.master.after(100, lambda: step(i + 1))
                else:
                    step(i + 1)
            step()

        def add_states(self):
            try:
                c = max(0, int(self.add_state_entry.get()))
                if c > 0:
                    self.draw_states(c, animated=False)
                    self.num_states += c
                    self.log("Added", c, "states")
            except:
                messagebox.showerror("Error", "Invalid number for states.")

        def delete_states(self):
            try:
                c = max(0, int(self.add_state_entry.get()))
                if c > 0:
                    d = min(c, self.num_states)
                    for _ in range(d):
                        self.canvas.delete(self.state_canvas_ids.pop())
                        self.canvas.delete(self.state_canvas_ids.pop())
                        pos = self.state_positions.pop()
                        self.session_log.append(f"Deleted State at {pos}")
                    self.num_states -= d
                    self.log("Deleted", d, "states")
            except:
                messagebox.showerror("Error", "Invalid number for states.")

        def add_agents(self):
            try:
                c = max(0, int(self.add_agent_entry.get()))
                if c > 0:
                    self.draw_agents(c, animated=False)
                    self.num_agents += c
                    self.log("Added", c, "agents")
            except:
                messagebox.showerror("Error", "Invalid number for agents.")

        def delete_agents(self):
            try:
                c = max(0, int(self.add_agent_entry.get()))
                if c > 0:
                    d = min(c, self.num_agents)
                    for _ in range(d):
                        self.canvas.delete(self.agent_canvas_ids.pop())
                        self.canvas.delete(self.agent_canvas_ids.pop())
                        pos = self.agent_positions.pop()
                        self.session_log.append(f"Deleted Agent at {pos}")
                    self.num_agents -= d
                    self.log("Deleted", d, "agents")
            except:
                messagebox.showerror("Error", "Invalid number for agents.")

        def reset_env(self):
            self.session_log.append("===== Environment Reset =====")
            self.session_log.append("The environment has been reset by the user.\n")

            self.agent_positions.clear()
            self.state_positions.clear()
            for cid in self.agent_canvas_ids + self.state_canvas_ids:
                self.canvas.delete(cid)
            self.agent_canvas_ids.clear()
            self.state_canvas_ids.clear()
            self.num_agents = self.num_states = 0
            self.canvas.delete("all")
            self.canvas.config(width=800, height=600, scrollregion=(0, 0, 800, 600))
            for e in [self.area_entry, self.agent_entry, self.state_entry, self.add_agent_entry, self.add_state_entry]:
                e.delete(0, tk.END)
            self.log_text.configure(state="normal")
            self.log_text.delete(1.0, tk.END)
            self.log_text.configure(state="disabled")
            self.log("Reset", "", "environment")

        def export_log(self):
            # Ask user where to save
            filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    filetypes=[("Text files", "*.txt")],
                                                    initialfile=f"DynamicEnvLog_{dt.now().strftime('%Y%m%d_%H%M%S')}.txt")
            if filename:
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        # Write structured log
                        f.write("Agentic AI\n")
                        f.write("Dynamic Environment\n")
                        f.write("\n".join(self.session_log))
                        f.write("\n")
                    messagebox.showinfo("Export", f"Log successfully saved to:\n{filename}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save log:\n{e}")      
    root = tk.Tk()
    app = DynamicEnvironmentGUI(root)

#Deterministic Environment
class DeterministicEnvironment(tk.Toplevel):
    def __init__(self):
        self.export_log = []  # Store session log entries
        super().__init__()
        self.geometry("1000x700+100+50")
        self.focus()
        self.title("Deterministic Environment")
        self.geometry("1000x700")
        self.configure(bg="#f9f9f9")
        self.shape_var = tk.StringVar()
        self.shape_type_var = tk.StringVar()
        self.triangle_side_entries = []
        self.state_positions = []
        self.canvas_states = []
        self.full_positions = []
        self.ngon_sides = 5
        self.label_font = tkfont.Font(family="Helvetica", size=10, weight="bold")
        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", lambda: confirm_close(self))
        
    def setup_ui(self):
        self.left = tk.Frame(self, width=280, bg="#eaeaea", padx=10, pady=10)
        self.left.pack(side="left", fill="y")

        # Two frames inside left for vertical split (approx 60-40)
        self.left_top = tk.Frame(self.left, bg="#eaeaea")
        self.left_bottom = tk.Frame(self.left, bg="#eaeaea")

        self.left_top.pack(side="top", fill="both", expand=True)
        self.left_bottom.pack(side="bottom", fill="both", expand=True)

        # Widgets in top 60%
        tk.Label(self.left_top, text="Choose Shape:", bg="#eaeaea", anchor="w").pack(anchor="w", pady=(0, 5))
        shape_options = ["Triangle", "Rectangle", "Square", "Circle", "N-gon"]
        self.shape_var.set("Select \u25BE")
        shape_menu = tk.OptionMenu(self.left_top, self.shape_var, *shape_options, command=self.on_shape_change)
        shape_menu.config(width=20)
        shape_menu.pack(anchor="w", pady=(0, 10))

        self.type_frame = tk.Frame(self.left_top, bg="#eaeaea")
        self.type_frame.pack(anchor="w", pady=(0, 10), fill="x")

        self.type_label = tk.Label(self.type_frame, text="Triangle Type:", bg="#eaeaea", anchor="w")
        self.type_optionmenu = None

        self.triangle_sides_frame = tk.Frame(self.left_top, bg="#eaeaea")
        self.triangle_sides_frame.pack(anchor="w", pady=(0, 10))

        self.size_label = tk.Label(self.left_top, text="Shape Size:", bg="#eaeaea", anchor="w")
        self.size_label.pack(anchor="w", pady=(0, 5))
        self.shape_size_entry = tk.Entry(self.left_top, width=25)
        self.shape_size_entry.pack(anchor="w", pady=(0, 10))

        tk.Label(self.left_top, text="Number of States:", bg="#eaeaea", anchor="w").pack(anchor="w", pady=(0, 5))
        self.entry_states = tk.Entry(self.left_top, width=25)
        self.entry_states.pack(anchor="w", pady=(0, 15))

        self.description_label = tk.Label(self.left_top, text="", bg="#eaeaea", wraplength=250, justify="left", fg="dark green")
        self.description_label.pack(anchor="w", pady=(10, 10))


        # Buttons in bottom 40%
        self.deploy_button = tk.Button(self.left_bottom, text="Deploy", width=20, command=self.plot_shape)
        self.deploy_button.pack(anchor="center", pady=(10, 5))

        self.reset_env_btn = tk.Button(self.left_bottom, text="Environment Reset", width=20, command=self.reset_environment)
        self.reset_env_btn.pack(anchor="center", pady=(5, 10))

        self.export_button = tk.Button(self.left_bottom, text="Export", width=20, command=self.export_session)
        self.export_button.pack(anchor="center",side="bottom", pady=(5, 10))

        # Right side remains unchanged
        self.right = tk.Frame(self)
        self.right.pack(side="right", expand=True, fill="both")

        self.canvas = tk.Canvas(self.right, bg="white")
        self.hbar = tk.Scrollbar(self.right, orient="horizontal", command=self.canvas.xview)
        self.vbar = tk.Scrollbar(self.right, orient="vertical", command=self.canvas.yview)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.hbar.pack(side="bottom", fill="x")
        self.vbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", expand=True, fill="both")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)


    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_shift_mousewheel(self, event):
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def reset_environment(self):
        self.reset_canvas()
        self.full_positions.clear()
        self.shape_var.set("")
        self.shape_type_var.set("")
        self.clear_triangle_side_inputs()
        self.shape_size_entry.delete(0, tk.END)
        self.entry_states.delete(0, tk.END)
        self.type_label.pack_forget()
        if self.type_optionmenu:
            self.type_optionmenu.pack_forget()
        self.size_label.pack(anchor="w", pady=(0, 5))
        self.shape_size_entry.pack(anchor="w", pady=(0, 10))
        self.canvas.config(scrollregion=(0, 0, 1000, 800))
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.export_log.append("Environment Reset.\n" + "-"*50)
        self.description_label.config(text="")  # Clear the description
        self.description_label.config(
        text="Environment reset, ready for new deployment.", fg="dark green"
        )

    def reset_canvas(self):
        self.canvas.delete("all")
        self.canvas_states.clear()
        self.state_positions.clear()
        
    def on_shape_change(self, selected_shape):
        self.reset_canvas()
        self.full_positions.clear()
        self.shape_type_var.set("")
        self.clear_triangle_side_inputs()
        if selected_shape == "Triangle":
            self.type_label.pack(anchor="w")
            if self.type_optionmenu:
                self.type_optionmenu.pack_forget()
            triangle_types = ["Equilateral", "Isosceles", "Scalene"]
            self.shape_type_var.set(triangle_types[0])
            self.type_optionmenu = tk.OptionMenu(self.type_frame, self.shape_type_var, *triangle_types, command=self.on_triangle_type_change)
            self.type_optionmenu.config(width=18)
            self.type_optionmenu.pack(anchor="w")
            self.size_label.pack_forget()
            self.shape_size_entry.pack_forget()
            self.show_triangle_side_inputs(triangle_types[0])
        else:
            self.type_label.pack_forget()
            if self.type_optionmenu:
                self.type_optionmenu.pack_forget()
            self.clear_triangle_side_inputs()
            self.size_label.pack(anchor="w", pady=(0, 5))
            self.shape_size_entry.pack(anchor="w", pady=(0, 10))
            if selected_shape == "Rectangle":
                self.size_label.config(text="Width x Height (e.g. 300x200):")
            elif selected_shape == "Square":
                self.size_label.config(text="Side Length:")
            elif selected_shape == "Circle":
                self.size_label.config(text="Radius:")
            elif selected_shape == "N-gon":
                self.size_label.config(text="Radius:")
                n = simpledialog.askinteger("N-gon", "Enter number of sides (5–10):", minvalue=5, maxvalue=10)
                if n is None:
                    self.shape_var.set("")
                    return
                self.ngon_sides = n
                self.shape_type_var.set(f"{n}-gon")

    def on_triangle_type_change(self, selected_type):
        self.show_triangle_side_inputs(selected_type)

    def clear_triangle_side_inputs(self):
        for w in self.triangle_sides_frame.winfo_children():
            w.destroy()
        self.triangle_side_entries = []
        self.triangle_sides_frame.pack_forget()

    def show_triangle_side_inputs(self, triangle_type):
        self.clear_triangle_side_inputs()
        self.triangle_sides_frame.pack(anchor="w", pady=(0, 10))
        if triangle_type == "Equilateral":
            f, e = l1(self.triangle_sides_frame, "Side Length:")
            f.pack(anchor="w", pady=2)
            self.triangle_side_entries = [e]
        elif triangle_type == "Isosceles":
            f1, e1 = l1(self.triangle_sides_frame, "Equal Side Length:")
            f2, e2 = l1(self.triangle_sides_frame, "Base Length:")
            f1.pack(anchor="w", pady=2)
            f2.pack(anchor="w", pady=2)
            self.triangle_side_entries = [e1, e2]
        elif triangle_type == "Scalene":
            f1, e1 = l1(self.triangle_sides_frame, "Side A:")
            f2, e2 = l1(self.triangle_sides_frame, "Side B:")
            f3, e3 = l1(self.triangle_sides_frame, "Side C:")
            f1.pack(anchor="w", pady=2)
            f2.pack(anchor="w", pady=2)
            f3.pack(anchor="w", pady=2)
            self.triangle_side_entries = [e1, e2, e3]

    def plot_shape(self):
        self.description_label.config(text="")  # Clear previous description
        self.reset_canvas()
        try:
            num_states = int(self.entry_states.get())
            if num_states <= 0:
                raise ValueError
        except:
            return messagebox.showerror("Invalid Input", "Please enter a valid positive integer for number of states.")

        shape = self.shape_var.get()
        shape_type = self.shape_type_var.get()
        size_input = None

        if shape == "Triangle":
            try:
                sides = [float(e.get()) for e in self.triangle_side_entries]
                if any(s <= 0 for s in sides):
                    raise ValueError
                size_input = sides
            except:
                return messagebox.showerror("Invalid Input", "Enter valid positive side lengths for triangle.")
        else:
            size_input = self.shape_size_entry.get()
            if shape in ["Square", "Circle", "N-gon"]:
                try:
                    size_input = float(size_input)
                    if size_input <= 0:
                        raise ValueError
                except:
                    return messagebox.showerror("Invalid Input", "Enter a valid positive number for size.")
            elif shape == "Rectangle":
                if "x" not in size_input:
                    return messagebox.showerror("Invalid Input", "Enter rectangle size as Width x Height, e.g. 300x200.")
        
        # Construct and set the description
        desc = f"Created a {shape}"
        if shape == "Triangle":
            desc += f" ({shape_type})"
            desc += f" with sides {', '.join(str(s) for s in size_input)}"
        elif shape == "Rectangle":
            desc += f" of size {size_input}"
        elif shape in ["Square", "Circle"]:
            desc += f" with {'side length' if shape == 'Square' else 'radius'} {size_input}"
        elif shape == "N-gon":
            desc += f" ({self.ngon_sides}-gon) with radius {size_input}"
        desc += f" and randomly deployed {num_states} states."
        self.description_label.config(text=desc)

        # Determine canvas size
        W, H = 700, 600
        if shape == "Rectangle":
            try:
                w, h = map(float, size_input.lower().split('x'))
                W, H = int(w), int(h)
            except:
                pass
        elif shape in ["Square", "Circle", "N-gon"]:
            side_or_radius = float(size_input)
            W = H = int(2 * side_or_radius )

        self.canvas.config(scrollregion=(0, 0, W, H), width=min(800, W), height=min(600, H))
        self.canvas.delete("all")
        grid_spacing = 50
        for x in range(0, W + 1, grid_spacing):
            self.canvas.create_line(x, 0, x, H, fill="lightblue", dash=(2, 4))
            self.canvas.create_text(x + 2, H - 10, text=str(x), anchor="nw", font=("Arial", 7), fill="blue")
        for y in range(0, H + 1, grid_spacing):
            flipped_y = H - y
            self.canvas.create_line(0, flipped_y, W, flipped_y, fill="lightblue", dash=(2, 4))
            self.canvas.create_text(2, flipped_y - 2, text=str(y), anchor="sw", font=("Arial", 7), fill="blue")

        positions, outline = self.generate_deterministic_positions(shape, shape_type, num_states, size_input, cx=W // 2, cy=H // 2)
        if not positions:
            return
        self.full_positions = positions
        self.state_positions = positions[:num_states]

        # Draw shape outline first
        if shape == "Circle":
            radius = float(size_input)
            cx, cy = W // 2, H // 2
            self.canvas.create_oval(cx - radius, H - (cy - radius), cx + radius, H - (cy + radius), outline="black", width=2)
        elif outline:
            flipped_outline = [(x, H - y) for (x, y) in outline]
            pts = [coord for point in flipped_outline for coord in point]
            self.canvas.create_polygon(pts, outline="black", fill="", width=2)

        # Start animated drawing of states one by one
        def draw_states(index=0):
            if index < len(self.state_positions):
                x, y = self.state_positions[index]
                fy = H - y
                oval = self.canvas.create_oval(x - 6, fy - 6, x + 6, fy + 6, fill="white")
                label = self.canvas.create_text(x, fy - 12, text=f"S{index + 1}", font=("Arial", 8), fill="black")
                self.canvas_states.append((oval, label))
                self.after(150, lambda: draw_states(index + 1))  # Delay next state
            else:
                # Finished drawing all states
                pass

        self.after(200, draw_states)  # Start after a small delay to ensure outline is visible

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.canvas.update_idletasks()
        export_entry = f"Shape: {shape}"
        if shape == "Triangle":
            export_entry += f" ({shape_type}), sides: {size_input}"
        elif shape == "Rectangle":
            export_entry += f", size: {size_input}"
        elif shape in ["Square", "Circle"]:
            export_entry += f", {'side' if shape == 'Square' else 'radius'}: {size_input}"
        elif shape == "N-gon":
            export_entry += f" ({self.ngon_sides}-gon), radius: {size_input}"
        export_entry += f"\nDescription: {desc}"

        if outline:
            export_entry += "\nShape Coordinates (outline):"
            for pt in outline:
                export_entry += f"\n  {pt}"

        export_entry += "\nState Coordinates:"
        for i, pos in enumerate(self.state_positions):
            export_entry += f"\n  S{i+1}: {pos}"
        
        self.export_log.append(export_entry + "\n" + "-"*50)

    def generate_deterministic_positions(self, shape, shape_type, num_states, size_input, cx=0, cy=0):
        positions = []
        outline = []

        def add_random_points_inside(polygon, count):
            bbox_x = [p[0] for p in polygon]
            bbox_y = [p[1] for p in polygon]
            min_x, max_x = min(bbox_x), max(bbox_x)
            min_y, max_y = min(bbox_y), max(bbox_y)
            added = 0
            attempts = 0
            while added < count and attempts < 1000:
                px = random.uniform(min_x, max_x)
                py = random.uniform(min_y, max_y)
                if point_in_polygon((px, py), polygon):
                    positions.append((px, py))
                    added += 1
                attempts += 1

        if shape == "Circle":
            radius = float(size_input)
            cx, cy = radius, radius  # circle starts from origin
            positions.append((cx, cy))  # center
            for _ in range(num_states - 1):
                angle = random.uniform(0, 2 * math.pi)
                r = random.uniform(0, radius)
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                positions.append((x, y))
            return positions, []

        elif shape == "Triangle":
            sides = size_input
            if shape_type == "Equilateral":
                side = sides[0]
                h = (math.sqrt(3) / 2) * side
                p1 = (0, 0)
                p2 = (side, 0)
                p3 = (side / 2, h)
            elif shape_type == "Isosceles":
                equal, base = sides
                h = math.sqrt(equal ** 2 - (base / 2) ** 2)
                p1 = (0, 0)
                p2 = (base, 0)
                p3 = (base / 2, h)
            elif shape_type == "Scalene":
                a, b, c = sides
                p1 = (0, 0)
                p2 = (c, 0)
                angle = math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c))
                px = c - a * math.cos(angle)
                py = a * math.sin(angle)
                p3 = (px, py)
            outline = [p1, p2, p3]

        elif shape == "Rectangle":
            w, h = map(float, size_input.lower().split('x'))
            p1 = (0, 0)
            p2 = (w, 0)
            p3 = (w, h)
            p4 = (0, h)
            outline = [p1, p2, p3, p4]

        elif shape == "Square":
            side = float(size_input)
            p1 = (0, 0)
            p2 = (side, 0)
            p3 = (side, side)
            p4 = (0, side)
            outline = [p1, p2, p3, p4]

        elif shape == "N-gon":
            n = self.ngon_sides
            radius = float(size_input)
            cx, cy = radius, radius  # start from radius so it stays positive
            for i in range(n):
                angle = 2 * math.pi * i / n
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                outline.append((x, y))

        # Place points: vertices → center → edge midpoints → inside
        if shape != "Circle":
            positions.extend(outline[:num_states])
            if len(positions) < num_states:
                center_x = sum(x for x, y in outline) / len(outline)
                center_y = sum(y for x, y in outline) / len(outline)
                positions.append((center_x, center_y))
            if len(positions) < num_states:
                for i in range(len(outline)):
                    mid = midpoint(outline[i], outline[(i + 1) % len(outline)])
                    positions.append(mid)
                    if len(positions) >= num_states:
                        break
            if len(positions) < num_states:
                add_random_points_inside(outline, num_states - len(positions))

        return positions, outline


    def export_session(self):
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")],
                title="Save Session Export As"
            )
            if not file_path:
                return  # User cancelled the dialog

            try:
                with open(file_path, "w") as file:
                    file.write("Agentic AI\n")
                    file.write("Deterministic Agent\n")
                    file.write("=" * 50 + "\n")
                    for entry in self.export_log:
                        file.write(entry + "\n")
                messagebox.showinfo("Export Successful", f"Session exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Error exporting session:\n{e}")


# --- Main App Window ---
root = tk.Tk()
root.title("Agents & Environment")
root.geometry("900x550")

paned = tk.PanedWindow(root, orient='horizontal', sashrelief=tk.RAISED)
paned.pack(fill='both', expand=True)

# Left Panel
left_frame = tk.Frame(paned)
tree = ttk.Treeview(left_frame, show="tree")
tree.pack(fill='both', expand=True, padx=5, pady=5)
paned.add(left_frame, width=300)

# Right Panel
right_frame = tk.Frame(paned)
image_label = tk.Label(right_frame)
image_label.pack(pady=(5, 0))
description_text = tk.Text(right_frame, wrap='word', state='disabled')
description_text.pack(fill='both', expand=True, padx=5, pady=5)
paned.add(right_frame)

# Global image holder
current_image = None

# Open Button
open_button = tk.Button(right_frame, text="Open", command=lambda: on_open_action())
open_button.pack(pady=10)
open_button.pack_forget()  # Hide by default

# Populate Tree
def create_tree():
    env_node = tree.insert("", "end", text="Environment", open=True)
    for name in [
        "Fully Observable", "Partially Observable", "Deterministic", "Stochastic",
        "Episodic", "Sequential", "Static", "Dynamic", "Discrete", "Continuous",
        "Single agent", "Multi agent"
    ]:
        tree.insert(env_node, "end", text=name)

    agent_node = tree.insert("", "end", text="Agents", open=True)
    for name in [
        "Simple Reflex", "Model-Based", "Goal-Based", "Utility-Based", "Learning-Based"
    ]:
        tree.insert(agent_node, "end", text=name)

create_tree()
# Action Mapping
def on_open_action():
    item = tree.focus()
    text = tree.item(item)["text"]
    fn_map = {
        "Episodic": lambda: open_episodic_env(root),
        "Sequential": lambda: open_sequential_env(),
        "Single agent": lambda: SingleAgentEnvironment(tk.Toplevel(root)),
        "Multi agent": lambda: MultiAgentEnvironment(tk.Toplevel(root)),
        "Static": lambda: StaticEnvironment(tk.Toplevel(root)),
        "Dynamic": lambda: open_dynamic_env(),
        "Deterministic": lambda: DeterministicEnvironment(),
    }
    fn = fn_map.get(text)
    if fn:
        fn()
    else:
        messagebox.showinfo("Info", f"No action defined for '{text}'")
# Selection Logic
def on_select(event=None):
    global current_image
    item = tree.focus()
    text = tree.item(item)["text"]
    desc = descriptions.get(text, "No description available.")
    # Load image
    img_path = image_paths.get(text)
    if img_path:
        try:
            img = Image.open(img_path)
            right_frame.update_idletasks()
            frame_width = right_frame.winfo_width() or 400
            max_width = min(frame_width - 20, 600)
            aspect_ratio = img.height / img.width
            new_width = max_width
            new_height = int(new_width * aspect_ratio)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            current_image = ImageTk.PhotoImage(img)
            image_label.config(image=current_image, text='')
        except Exception:
            image_label.config(image='', text='')
            current_image = None
    else:
        image_label.config(image='', text='')

    # Update description
    description_text.config(state='normal')
    description_text.delete("1.0", tk.END)
    description_text.insert(tk.END, f"{text}\n\n{desc}")
    description_text.config(state='disabled')

    # Show/hide open button
    if text in [
        "Episodic", "Sequential", "Static", "Dynamic", "Single agent", "Multi agent","Deterministic",
    ]:
        open_button.pack(pady=10)
    else:
        open_button.pack_forget()
# Bind Events
tree.bind("<<TreeviewSelect>>", on_select)
tree.bind("<Double-1>", lambda e: on_open_action())
# Start GUI
root.mainloop()