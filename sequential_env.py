import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import math

descriptions = {
    "Agentic AI": "New Generation AI focused on agents interacting with environments.",
    "Environment": "The external context in which an agent operates.",
    "Environment Types": "Classifications of environments based on characteristics that affect agent design.",

    "Fully Observable": "The agent's sensors give it access to the complete state of the environment at each point in time.",
    "Partially Observable": "The agent does not have access to the complete state of the environment.",
    "Deterministic": "The next state of the environment is completely determined by the current state and the agent's action.",
    "Stochastic": "There is some randomness in state transitions.",
    "Episodic": "Each episode (interaction) is independent of the previous ones.",
    "Sequential": "Current decisions affect future states or decisions.",
    "Static": "The environment does not change while the agent is deliberating.",
    "Dynamic": "The environment can change while the agent is choosing an action.",
    "Discrete": "There are a finite number of distinct states, percepts, and actions.",
    "Continuous": "States and actions vary smoothly (e.g., real numbers).",
    "Single-Agent": "Only one agent acts in the environment.",
    "Multi-Agent": "Multiple agents interact, possibly competing or cooperating.",

    "Agents": "Entities that perceive their environment and act upon it.",
    "Simple Reflex": "Agents that act only on the basis of the current percept, ignoring the rest of the percept history.",
    "Model-Based": "Agents that maintain some internal state based on the history of percepts.",
    "Goal-Based": "Agents that act to achieve a specific goal.",
    "Utility-Based": "Agents that act to maximize a utility function.",
    "Learning-Based": "Agents that can learn from experience to improve their performance over time.",

    "Sequential Environment": "A simulation environment where operations are applied step-by-step on an initial number, showing results graphically.",
}

def create_tree(tree):
    root_node = tree.insert("", "end", text="Agentic AI", open=True)
    env_types = tree.insert(root_node, "end", text="Environment Types", open=True)
    for env_type in [
        "Fully Observable", "Partially Observable",
        "Deterministic", "Stochastic",
        "Episodic", "Sequential",
        "Static", "Dynamic",
        "Discrete", "Continuous",
        "Single-Agent", "Multi-Agent"
    ]:
        tree.insert(env_types, "end", text=env_type)
    agents = tree.insert(root_node, "end", text="Agents", open=True)
    for agent_type in [
        "Simple Reflex", "Model-Based", "Goal-Based", "Utility-Based", "Learning-Based"
    ]:
        tree.insert(agents, "end", text=agent_type)

def on_tree_select(event):
    selected_item = tree.focus()
    item_text = tree.item(selected_item)["text"]
    desc = descriptions.get(item_text, "No description available for this item.")
    description_text.config(state="normal")
    description_text.delete("1.0", tk.END)
    description_text.insert(tk.END, f"{item_text}\n\n{desc}")
    description_text.config(state="disabled")

    # Remove previous Open button
    for widget in right_frame.pack_slaves():
        if isinstance(widget, tk.Button) and widget.cget("text") == "Open":
            widget.destroy()

    if item_text == "Sequential":
        open_btn = tk.Button(right_frame, text="Open", command=open_sequential_env)
        open_btn.pack(pady=10)

def on_tree_double_click(event):
    selected_item = tree.focus()
    item_text = tree.item(selected_item)["text"]
    if item_text == "Sequential":
        open_sequential_env()

def open_sequential_env():
    seq_win = tk.Toplevel(root)
    seq_win.title("Sequential Environment Simulation")
    seq_win.geometry("1200x480")

    state = {
        "current_step": 0,
        "result": 0,
        "total_steps": 0,
    }

    def function1(number, operand):  # Addition
        return number + operand

    def function2(number, operand):  # Multiplication
        return number * operand

    def function3(number, operand):  # Subtraction
        return number - operand

    def function4(number, operand):  # Division
        if operand == 0:
            raise ValueError("Cannot divide by zero.")
        return number / operand

    def function5(number, operand):  # Exponential (power)
        return number ** operand

    def function6(number, operand):  # Logarithm base 10
        if number <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers.")
        return math.log10(number)

    def function7(number, operand):  # Square root
        if number < 0:
            raise ValueError("Square root undefined for negative numbers.")
        return math.sqrt(number)

    def function8(number, operand):  # Round off
        return round(number)

    operation_functions = {
        1: function1,
        2: function2,
        3: function3,
        4: function4,
        5: function5,
        6: function6,
        7: function7,
        8: function8
    }

    operations_need_operand = {1, 2, 3, 4, 5}

    left_frame = tk.Frame(seq_win)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=10)

    tk.Label(left_frame, text="Enter a number:").pack(anchor="w")
    entry_input = tk.Entry(left_frame)
    entry_input.pack(fill=tk.X, pady=5)

    tk.Label(left_frame, text="Number of operations:").pack(anchor="w")
    entry_operations = tk.Entry(left_frame)
    entry_operations.pack(fill=tk.X, pady=5)

    label_step = tk.Label(left_frame, text="")
    label_step.pack(pady=10)

    frame_operations = tk.Frame(left_frame)
    frame_operations.pack(pady=10, fill=tk.X)

    btn_config = {"width": 18}
    tk.Button(frame_operations, text="Add (+)", command=lambda: apply_operation(1), **btn_config).pack(pady=3)
    tk.Button(frame_operations, text="Multiply (×)", command=lambda: apply_operation(2), **btn_config).pack(pady=3)
    tk.Button(frame_operations, text="Subtract (-)", command=lambda: apply_operation(3), **btn_config).pack(pady=3)
    tk.Button(frame_operations, text="Divide (÷)", command=lambda: apply_operation(4), **btn_config).pack(pady=3)
    tk.Button(frame_operations, text="Power (xʸ)", command=lambda: apply_operation(5), **btn_config).pack(pady=3)
    tk.Button(frame_operations, text="Log base 10", command=lambda: apply_operation(6), **btn_config).pack(pady=3)
    tk.Button(frame_operations, text="Square Root", command=lambda: apply_operation(7), **btn_config).pack(pady=3)
    tk.Button(frame_operations, text="Round Off", command=lambda: apply_operation(8), **btn_config).pack(pady=3)

    label_result = tk.Label(left_frame, text="Final Result:")
    label_result.pack(pady=15)

    button_start = tk.Button(left_frame, text="Start", command=lambda: start_operations())
    button_start.pack(pady=5)

    right_frame_seq = tk.Frame(seq_win)
    right_frame_seq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)

    canvas = tk.Canvas(right_frame_seq, bg="#f0f0f0", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    def start_operations():
        try:
            user_input = float(entry_input.get())
            total = int(entry_operations.get())
            if total <= 0:
                messagebox.showerror("Input Error", "Number of operations must be positive.")
                return
            state["result"] = user_input
            state["total_steps"] = total
            state["current_step"] = 0
            canvas.delete("all")
            draw_step_circle(0, state["result"])
            label_step.config(text=f"Step 1: Choose operation")
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
        operation_func = operation_functions.get(op_choice)
        if not operation_func:
            messagebox.showerror("Invalid Choice", "Choose a valid operation.")
            return
        try:
            if op_choice in operations_need_operand:
                operand = simpledialog.askfloat("Input", f"Enter the number for the operation:")
                if operand is None:
                    return
                state["result"] = operation_func(state["result"], operand)
            else:
                state["result"] = operation_func(state["result"], None)

            state["current_step"] += 1
            draw_step_circle(state["current_step"], state["result"])
            ask_next_operation()
        except Exception as e:
            messagebox.showerror("Error", f"Operation failed: {e}")

    def draw_step_circle(step_num, value):
        radius_x = 70
        radius_y = 35
        spacing_x = 190
        spacing_y = 120
        max_per_row = 4

        row = step_num // max_per_row
        col = step_num % max_per_row
        y = 80 + row * spacing_y
        x_center = 110 + col * spacing_x

        gradient_color1 = "#e74c3c"
        gradient_color2 = "#c0392b"

        # Outer oval
        canvas.create_oval(
            x_center - radius_x, y - radius_y,
            x_center + radius_x, y + radius_y,
            fill=gradient_color2, outline="black", width=2
        )
        # Inner oval
        canvas.create_oval(
            x_center - radius_x + 5, y - radius_y + 5,
            x_center + radius_x - 5, y + radius_y - 5,
            fill=gradient_color1, outline=""
        )

        display_value = round(value, 6) if isinstance(value, float) else value
        canvas.create_text(
            x_center, y,
            text=f"{display_value}",
            fill="white"
        )

        if step_num > 0:
            prev_step = step_num - 1
            prev_row = prev_step // max_per_row
            prev_col = prev_step % max_per_row
            prev_x = 110 + prev_col * spacing_x
            prev_y = 80 + prev_row * spacing_y

            if row == prev_row:
                # Same row - horizontal arrow longer for spacing
                canvas.create_line(
                    prev_x + radius_x, prev_y,
                    x_center - radius_x, y,
                    arrow=tk.LAST,
                    width=4,
                    fill="black",
                    arrowshape=(20, 25, 10),
                    smooth=True
                )
            else:
                offset_x = 25
                offset_y = 15

                start_x = prev_x + radius_x
                start_y = prev_y
                line1_end_x = start_x + offset_x
                line1_end_y = start_y

                canvas.create_line(
                    start_x, start_y,
                    line1_end_x, line1_end_y,
                    width=4,
                    fill="black",
                    smooth=True
                )

                line2_start_x = line1_end_x
                line2_start_y = line1_end_y
                line2_end_x = line2_start_x
                line2_end_y = y - radius_y - offset_y

                canvas.create_line(
                    line2_start_x, line2_start_y,
                    line2_end_x, line2_end_y,
                    width=4,
                    fill="black",
                    smooth=True
                )

                line3_start_x = line2_end_x
                line3_start_y = line2_end_y
                line3_end_x = x_center - radius_x
                line3_end_y = line3_start_y

                canvas.create_line(
                    line3_start_x, line3_start_y,
                    line3_end_x, line3_end_y,
                    arrow=tk.LAST,
                    width=4,
                    fill="black",
                    arrowshape=(20, 25, 10),
                    smooth=True
                )

    frame_operations.pack_forget()

root = tk.Tk()
root.title("Agentic AI")
root.geometry("900x550")

paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
paned.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(paned)
tree = ttk.Treeview(left_frame)
tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
create_tree(tree)
tree.bind("<<TreeviewSelect>>", on_tree_select)
tree.bind("<Double-1>", on_tree_double_click)
paned.add(left_frame, width=300)

right_frame = tk.Frame(paned)
description_text = tk.Text(right_frame, wrap="word", state="disabled")
description_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
paned.add(right_frame)

root.mainloop()
