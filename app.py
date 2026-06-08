import tkinter as tk
from tkinter import ttk

class Beginner531App:
    def __init__(self, root):
        self.root = root
        self.root.title("5/3/1 Beginner Mobile-Style Tracker")
        self.root.geometry("450x700")
        self.root.configure(bg="#0f172a")  # Dark Slate Background

        # Custom Dark Theme Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", background="#0f172a", foreground="#f8fafc", font=("Segoe UI", 10))
        self.style.configure("TCombobox", fieldbackground="#334155", background="#1e293b", foreground="#ffffff")
        
        # Program Configurations
        self.week_data = {
            "Week 1 (5/5/5)": {"w": [0.4, 0.5, 0.6], "s": [0.65, 0.75, 0.85], "reps": ["5", "5", "5+"], "fsl": 0.65},
            "Week 2 (3/3/3)": {"w": [0.4, 0.5, 0.6], "s": [0.70, 0.80, 0.90], "reps": ["3", "3", "3+"], "fsl": 0.70},
            "Week 3 (5/3/1)": {"w": [0.4, 0.5, 0.6], "s": [0.75, 0.85, 0.95], "reps": ["5", "3", "1+"], "fsl": 0.75},
            "Week 4 (Deload)": {"w": [0.4, 0.5, 0.6], "s": [0.40, 0.50, 0.60], "reps": ["5", "5", "5"], "fsl": None}
        }

        self.accessory_matrix = {
            "Week 1 (5/5/5)": {
                "Day 1": [["Lat Pulldowns", "3x8-12", "Pull"], ["Incline DB Press", "3x10-12", "Push"], ["Bulgarian Split Squats", "3x8-10", "Leg/Core"]],
                "Day 2": [["Barbell Rows", "3x8", "Pull"], ["Dips", "3x10-15", "Push"], ["Hanging Leg Raises", "3x12-15", "Leg/Core"]],
                "Day 3": [["Face Pulls", "3x15-20", "Pull"], ["DB Shoulder Press", "3x10", "Push"], ["DB Romanian Deadlifts", "3x10-12", "Leg/Core"]]
            },
            "Week 2 (3/3/3)": {
                "Day 1": [["Seated Cable Rows", "3x10-12", "Pull"], ["Push-ups", "3xMax", "Push"], ["Walking Lunges", "3x12/l", "Leg/Core"]],
                "Day 2": [["DB Single-Arm Rows", "3x10", "Pull"], ["Close-Grip Bench", "3x8-10", "Push"], ["Ab Wheel Rollouts", "3x8-10", "Leg/Core"]],
                "Day 3": [["Hammer Curls", "3x12", "Pull"], ["Cable Chest Flies", "3x12-15", "Push"], ["Leg Press", "3x10-12", "Leg/Core"]]
            },
            "Week 3 (5/3/1)": {
                "Day 1": [["Chin-ups", "3x6-10", "Pull"], ["Overhead Tricep Ext.", "3x12", "Push"], ["Planks", "3x45-60s", "Leg/Core"]],
                "Day 2": [["T-Bar Rows", "3x8-10", "Pull"], ["DB Lateral Raises", "3x12-15", "Push"], ["Step-ups onto Bench", "3x10/l", "Leg/Core"]],
                "Day 3": [["Chest-Supported Rows", "3x10", "Pull"], ["Incline DB Flyes", "3x12", "Push"], ["Leg Curls", "3x10-12", "Leg/Core"]]
            },
            "Week 4 (Deload)": {
                "Day 1": [["Lat Pulldowns (Light)", "2x10", "Pull"], ["Incline DB Press (Light)", "2x10", "Push"], ["Bodyweight Squats", "2x12", "Leg/Core"]],
                "Day 2": [["Barbell Rows (Light)", "2x8", "Pull"], ["Push-ups (Easy)", "2x10", "Push"], ["Stir the Pot Core", "2x8/s", "Leg/Core"]],
                "Day 3": [["Face Pulls", "2x15", "Pull"], ["DB Lateral Raises (Light)", "2x10", "Push"], ["Planks", "2x30s", "Leg/Core"]]
            }
        }

        # App Setup Initialization
        self.create_widgets()
        self.update_workout()

    def create_widgets(self):
        # Header Canvas App Bar
        header = tk.Label(self.root, text="5/3/1 BEGINNER TRACKER", bg="#1e293b", fg="#38bdf8", font=("Segoe UI", 12, "bold"), py=10)
        header.pack(fill="x")

        # ------------------- SECTION 1: 1RM INPUTS -------------------
        input_frame = tk.LabelFrame(self.root, text=" 1-Rep Max Controls ", bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 9, "bold"), bd=1, padx=10, pady=10)
        input_frame.pack(fill="x", padx=15, pady=10)

        maxes = [("Squat:", "70"), ("Bench:", "60"), ("Deadlift:", "90"), ("OHP:", "35")]
        self.inputs = {}

        for i, (label, default) in enumerate(maxes):
            row = i // 2
            col = (i % 2) * 2
            
            lbl = tk.Label(input_frame, text=label, bg="#1e293b", fg="#f8fafc", font=("Segoe UI", 10))
            lbl.grid(row=row, column=col, sticky="w", padx=5, pady=5)
            
            entry = tk.Entry(input_frame, width=8, bg="#334155", fg="#ffffff", insertbackground="white", font=("Segoe UI", 10, "bold"), justify="center", bd=0, highlightthickness=1, highlightbackground="#475569")
            entry.insert(0, default)
            entry.bind("<KeyRelease>", lambda e: self.update_workout())
            entry.grid(row=row, column=col+1, padx=5, pady=5)
            self.inputs[label.replace(":", "")] = entry

        # ------------------- SECTION 2: FILTERS -------------------
        filter_frame = tk.Frame(self.root, bg="#0f172a")
        filter_frame.pack(fill="x", padx=15, pady=5)

        self.week_var = tk.StringVar(value="Week 1 (5/5/5)")
        self.week_combo = ttk.Combobox(filter_frame, textvariable=self.week_var, values=list(self.week_data.keys()), state="readonly", font=("Segoe UI", 10))
        self.week_combo.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.week_combo.bind("<<ComboboxSelected>>", lambda e: self.update_workout())

        self.day_var = tk.StringVar(value="Day 1")
        self.day_combo = ttk.Combobox(filter_frame, textvariable=self.day_var, values=["Day 1", "Day 2", "Day 3"], state="readonly", font=("Segoe UI", 10))
        self.day_combo.pack(side="left", expand=True, fill="x", padx=(5, 0))
        self.day_combo.bind("<<ComboboxSelected>>", lambda e: self.update_workout())

        # ------------------- SECTION 3: DISPLAY CANVAS -------------------
        # Scrollable output area to look and feel like an app feed
        canvas_container = tk.Frame(self.root, bg="#0f172a")
        canvas_container.pack(fill="both", expand=True, padx=15, pady=10)

        self.canvas = tk.Canvas(canvas_container, bg="#0f172a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#0f172a")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def round_weight(self, weight):
        # MROUND-style execution safely rounding to nearest 0.5 units
        return round(weight * 2) / 2

    def update_workout(self):
        # Wipe old widgets clean
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Grab context parameters
        week = self.week_var.get()
        day = self.day_var.get()
        meta = self.week_data[week]

        try:
            tms = {
                "Squat": float(self.inputs["Squat"].get() or 0) * 0.9,
                "Bench": float(self.inputs["Bench"].get() or 0) * 0.9,
                "Deadlift": float(self.inputs["Deadlift"].get() or 0) * 0.9,
                "OHP": float(self.inputs["OHP"].get() or 0) * 0.9
            }
        except ValueError:
            return # Block calculations if user enters letters or symbols cleanly

        # Determine daily main lifts split configuration
        current_lifts = ["Squat", "Bench"] if day in ["Day 1", "Day 3"] else ["Deadlift", "OHP"]

        # Step 1 Display: Mobility Prompt
        mob_lbl = tk.Label(self.scrollable_frame, text="➔ Step 1: Mobility Warmup (10 Mins done)", bg="#064e3b", fg="#a7f3d0", font=("Segoe UI", 9, "italic"), anchor="w", padx=5, pady=3)
        mob_lbl.pack(fill="x", pady=(0, 10))

        # Step 2 Display: Main Barbell Blocks
        for lift in current_lifts:
            lift_frame = tk.Frame(self.scrollable_frame, bg="#1e293b", bd=1, highlightthickness=1, highlightbackground="#334155", padx=8, pady=8)
            lift_frame.pack(fill="x", pady=5)

            tm = tms[lift]
            tk.Label(lift_frame, text=f"{lift.upper()} (TM: {self.round_weight(tm)})", bg="#1e293b", fg="#38bdf8", font=("Segoe UI", 10, "bold")).pack(anchor="w")

            # Warmups Render loop
            for idx, pct in enumerate(meta["w"]):
                reps = "3" if idx == 2 else "5"
                wt = self.round_weight(tm * pct)
                tk.Label(lift_frame, text=f"  Warmup {idx+1}:  {int(pct*100)}%  ➔  {wt} kg/lbs  x  {reps}", bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 9)).pack(anchor="w")

            # Working Sets Render loop
            for idx, pct in enumerate(meta["s"]):
                is_amrap = idx == 2 and week != "Week 4 (Deload)"
                reps = meta["reps"][idx]
                label = f"  Work Set {idx+1} (+):" if is_amrap else f"  Work Set {idx+1}:  "
                color = "#f59e0b" if is_amrap else "#e2e8f0"
                wt = self.round_weight(tm * pct)
                tk.Label(lift_frame, text=f"{label}  {int(pct*100)}%  ➔  {wt} kg/lbs  x  {reps}", bg="#1e293b", fg=color, font=("Segoe UI", 9, "bold" if is_amrap else "normal")).pack(anchor="w")

            # First Set Last Volume append
            if meta["fsl"]:
                fsl_wt = self.round_weight(tm * meta["fsl"])
                tk.Label(lift_frame, text=f"  FSL Volume:  {int(meta['fsl']*100)}%  ➔  {fsl_wt} kg/lbs  x  5x5", bg="#1e293b", fg="#34d399", font=("Segoe UI", 9, "bold")).pack(anchor="w")

        # Step 3 Display: Rotating Dynamic Accessories
        acc_frame = tk.Frame(self.scrollable_frame, bg="#1e293b", bd=1, highlightthickness=1, highlightbackground="#334155", padx=8, pady=8)
        acc_frame.pack(fill="x", pady=10)
        tk.Label(acc_frame, text="STEP 3: DAILY ACCESSORIES", bg="#1e293b", fg="#c084fc", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))

        for name, sets, cat in self.accessory_matrix[week][day]:
            tk.Label(acc_frame, text=f" • [{cat}] {name} ➔ {sets}", bg="#1e293b", fg="#e2e8f0", font=("Segoe UI", 9)).pack(anchor="w", pady=2)

        # Step 4 Display: Recovery Stretch Prompt
        str_lbl = tk.Label(self.scrollable_frame, text="➔ Step 4: Post-Workout Static Stretching (Done)", bg="#7f1d1d", fg="#fca5a5", font=("Segoe UI", 9, "italic"), anchor="w", padx=5, pady=3)
        str_lbl.pack(fill="x", pady=(5, 0))

if __name__ == "__main__":
    window = tk.Tk()
    app = Beginner531App(window)
    window.mainloop()
