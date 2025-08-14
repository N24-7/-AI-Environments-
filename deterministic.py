import tkinter as tk
from tkinter import messagebox, simpledialog, font as tkfont
import math
import random
from tkinter import filedialog  


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

class DeterministicEnvironment(tk.Tk):
    def __init__(self):
        self.export_log = []  # Store session log entries
        super().__init__()
        self.state('zoomed')
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
            export_entry += "\nShape Coords (outline):"
            for pt in outline:
                export_entry += f"\n  {pt}"

        export_entry += "\nState Coords:"
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

if __name__ == "__main__":
    app = DeterministicEnvironment()
    app.mainloop()