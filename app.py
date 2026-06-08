import streamlit as st
import pandas as pd
import math

# Page Configuration
st.set_page_config(
    page_title="Dynamic Powerlifting Tracker",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Gym Interface
st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: bold; color: #2C4A5E; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 1.1rem; color: #555; text-align: center; margin-bottom: 25px; }
    .section-header { font-size: 1.5rem; font-weight: bold; color: #1C2E3A; border-bottom: 2px solid #4A708B; padding-bottom: 5px; margin-top: 20px; }
    .warmup-text { color: #B8860B; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🏋️‍♂️ 8-Week Dynamic Powerlifting App</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Auto-regulated warmups, progressive main lifts, and daily dynamic accessories</div>", unsafe_allow_html=True)

# Sidebar - User Inputs (1RMs)
st.sidebar.header("🎯 Enter Current 1-Rep Maxes")
unit = st.sidebar.radio("Preferred Weight Unit", ["lbs", "kg"])
squat_1rm = st.sidebar.number_input(f"Squat 1RM ({unit})", min_value=0, value=315, step=5)
bench_1rm = st.sidebar.number_input(f"Bench Press 1RM ({unit})", min_value=0, value=225, step=5)
deadlift_1rm = st.sidebar.number_input(f"Deadlift 1RM ({unit})", min_value=0, value=405, step=5)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Daily Mobility Routine")
st.sidebar.info("""
**Mandatory 10-15 Min Warm-Up:**
1. **Agile 8 Foam Roll** - 5 mins
2. **World's Greatest Stretch** - 2x5/side
3. **90/90 Hip Switches** - 2x8/side
4. **Band Pass-Throughs** - 2x12
5. **Scapular Pull/Push-ups** - 2x10
6. **Goblet Squat Hold** - 1x30s
""")

# Plate rounding function (to nearest 5 lbs/kg)
def round_weight(weight):
    return int(math.ceil(weight / 5.0)) * 5 if (weight % 5 >= 2.5) else int(math.floor(weight / 5.0)) * 5

# Program Parameter Maps
week_configs = {
    1: {"intensity": 0.70, "sets": 4, "reps": 6, "desc": "Volume Phase - Week 1"},
    2: {"intensity": 0.73, "sets": 4, "reps": 6, "desc": "Volume Phase - Week 2"},
    3: {"intensity": 0.76, "sets": 4, "reps": 5, "desc": "Volume Phase - Week 3"},
    4: {"intensity": 0.65, "sets": 3, "reps": 5, "desc": "Deload Phase - Week 4"},
    5: {"intensity": 0.80, "sets": 5, "reps": 3, "desc": "Strength Phase - Week 5"},
    6: {"intensity": 0.84, "sets": 4, "reps": 3, "desc": "Strength Phase - Week 6"},
    7: {"intensity": 0.88, "sets": 3, "reps": 2, "desc": "Peaking Phase - Week 7"},
    8: {"intensity": 1.00, "sets": 1, "reps": 1, "desc": "1RM MAX TESTING WEEK"}
}

accessories_pool = {
    1: {
        "Day 1": [("Leg Press", "3", "10", "RPE 7"), ("Romanian Deadlift", "3", "8", "RPE 7"), ("Plank", "3", "45s", "BW")],
        "Day 2": [("Incline DB Bench", "3", "10", "RPE 7"), ("Barbell Rows", "4", "8", "RPE 8"), ("Face Pulls", "3", "15", "RPE 7")],
        "Day 3": [("Bulgarian Split Squat", "3", "8/side", "RPE 7"), ("Lat Pulldowns", "3", "12", "RPE 8"), ("Hanging Knee Raises", "3", "12", "BW")]
    },
    2: {
        "Day 1": [("Hack Squat", "3", "10", "RPE 7.5"), ("Good Mornings", "3", "8", "RPE 7"), ("Ab Wheel Rollouts", "3", "10", "BW")],
        "Day 2": [("Dumbbell Flat Bench", "3", "10", "RPE 7.5"), ("Weighted Pull-ups", "4", "6", "RPE 8"), ("Cable Lateral Raises", "3", "12", "RPE 8")],
        "Day 3": [("Goblet Squat", "3", "12", "RPE 7"), ("Chest Supported Rows", "3", "10", "RPE 8"), ("Toes to Bar", "3", "8", "BW")]
    },
    3: {
        "Day 1": [("Safety Bar Squat", "3", "8", "RPE 8"), ("Deficit Deadlift", "3", "5", "RPE 7.5"), ("Pallof Press", "3", "12/side", "Tension")],
        "Day 2": [("Floor Press", "3", "6", "RPE 8"), ("T-Bar Rows", "4", "8", "RPE 8"), ("Reverse Flyes", "3", "15", "RPE 7")],
        "Day 3": [("Dumbbell Lunges", "3", "10/side", "RPE 8"), ("Seated Cable Rows", "3", "10", "RPE 8"), ("Dragon Flags", "3", "6", "BW")]
    },
    4: {
        "Day 1": [("Leg Extensions", "2", "12", "Light"), ("Lying Leg Curls", "2", "12", "Light"), ("Dead Bug", "2", "10/side", "BW")],
        "Day 2": [("DB Shoulder Press", "2", "12", "Light"), ("Lat Pulldowns", "2", "12", "Light"), ("Band Pull-Aparts", "2", "20", "Light")],
        "Day 3": [("Bodyweight Squats", "2", "20", "Mobility"), ("Back Extensions", "2", "12", "Light"), ("Plank", "2", "45s", "BW")]
    },
    5: {
        "Day 1": [("Paused Squat (2s)", "3", "4", "RPE 8"), ("Snatch-Grip Deadlift", "3", "5", "RPE 7.5"), ("Cable Crunch", "3", "12", "Heavy")],
        "Day 2": [("Close-Grip Bench", "3", "5", "RPE 8"), ("Pendlay Rows", "4", "6", "RPE 8.5"), ("DB Lateral Raises", "3", "12", "RPE 8")],
        "Day 3": [("Front Squat", "3", "5", "RPE 8"), ("Chin-Ups", "3", "Max-1", "BW"), ("Garhammer Raise", "3", "15", "BW")]
    },
    6: {
        "Day 1": [("Pin Squat", "3", "3", "RPE 8.5"), ("Block Pulls", "3", "4", "RPE 8"), ("Weighted Plank", "3", "60s", "Load")],
        "Day 2": [("Spoto Press", "3", "4", "RPE 8.5"), ("One-Arm DB Rows", "4", "8", "RPE 8.5"), ("Rear Delt Pulls", "3", "15", "RPE 8")],
        "Day 3": [("Leg Press", "3", "6", "RPE 8.5"), ("Meadows Rows", "3", "8", "RPE 8.5"), ("Hanging Leg Raises", "3", "10", "BW")]
    },
    7: {
        "Day 1": [("Box Squat", "3", "3", "RPE 8"), ("Stiff-Legged DL", "2", "5", "RPE 8"), ("Ab Wheel Rollouts", "3", "8", "Control")],
        "Day 2": [("Board Bench Press", "3", "3", "RPE 9"), ("Weighted Pull-ups", "3", "5", "RPE 8.5"), ("Band Face Pulls", "3", "20", "Pump")],
        "Day 3": [("Leg Press (Heavy)", "3", "6", "RPE 8"), ("Lat Pulldowns", "3", "8", "RPE 8.5"), ("Toes to Bar", "3", "10", "BW")]
    },
    8: { 
        "Day 1": [("Light Leg Curls", "2", "12", "Fluff"), ("Plank", "2", "30s", "Relaxed")],
        "Day 2": [("Light Lat Pulldowns", "2", "12", "Fluff"), ("Band Pull-Aparts", "2", "15", "Easy")],
        "Day 3": [("Full Recovery Protocols", "-", "-", "Rest & Hydrate")]
    }
}

# Initialize session state for tracking user input data across re-runs
if "logged_data" not in st.session_state:
    st.session_state.logged_data = {}

# Week Selection Header Slider
selected_week = st.selectbox("📅 Choose Your Training Week", [f"Week {i} - {week_configs[i]['desc']}" for i in range(1, 9)])
w_num = int(selected_week.split(" ")[1])

# Individual Workout Day Selectors
selected_day = st.tabs(["📆 Day 1: Squat Focus", "📆 Day 2: Bench Focus", "📆 Day 3: Deadlift Focus"])

for idx, day_name in enumerate(["Day 1", "Day 2", "Day 3"]):
    with selected_day[idx]:
        if day_name == "Day 1":
            lift_name, base_1rm = "Squat", squat_1rm
        elif day_name == "Day 2":
            lift_name, base_1rm = "Bench Press", bench_1rm
        else:
            lift_name, base_1rm = "Deadlift", deadlift_1rm
            
        st.markdown(f"<div class='section-header'>{day_name} Primary Protocol: {lift_name}</div>", unsafe_allow_html=True)
        
        # State keys specifically mapped to current week and day
        main_state_key = f"main_input_{w_num}_{day_name}"
        acc_state_key = f"acc_input_{w_num}_{day_name}"
        
        # --- PRIMARY LIFTS GENERATION ---
        rows = []
        if w_num < 8:
            intensity = week_configs[w_num]["intensity"]
            rows.append({"Type": "Warmup 1", "Exercise": f"Warmup: {lift_name}", "Sets": 1, "Reps": 8, "Target %": f"{round(intensity * 50)}%", "Calculated Weight": f"{round_weight(base_1rm * intensity * 0.50)} {unit}", "Completed Weight": "", "Rest": "2 min", "Notes": "Focus on clean bar path"})
            rows.append({"Type": "Warmup 2", "Exercise": f"Warmup: {lift_name}", "Sets": 1, "Reps": 5, "Target %": f"{round(intensity * 70)}%", "Calculated Weight": f"{round_weight(base_1rm * intensity * 0.70)} {unit}", "Completed Weight": "", "Rest": "2 min", "Notes": "Lock in tight abdominal bracing"})
            rows.append({"Type": "Warmup 3", "Exercise": f"Warmup: {lift_name}", "Sets": 1, "Reps": 3, "Target %": f"{round(intensity * 85)}%", "Calculated Weight": f"{round_weight(base_1rm * intensity * 0.85)} {unit}", "Completed Weight": "", "Rest": "3 min", "Notes": "Match your explosive intent"})
            rows.append({"Type": "MAIN WORKING SET", "Exercise": lift_name, "Sets": week_configs[w_num]["sets"], "Reps": week_configs[w_num]["reps"], "Target %": f"{round(intensity * 100)}%", "Calculated Weight": f"{round_weight(base_1rm * intensity)} {unit}", "Completed Weight": "", "Rest": "3-5 min", "Notes": "Full working volume load"})
        else:
            test_protocol = [
                ("Test Warmup 1", 5, 0.40, "2 min", "Bar speed evaluation"),
                ("Test Warmup 2", 3, 0.60, "2 min", "Lock down setup mechanics"),
                ("Test Warmup 3", 2, 0.75, "3 min", "Neurological priming single"),
                ("Test Warmup 4", 1, 0.85, "3 min", "Last heavy feel check"),
                ("1RM ATTEMPT 1", 1, 0.92, "4 min", "The Opener - Easy confident token"),
                ("1RM ATTEMPT 2", 1, 1.00, "5 min", "PR Match - Ties historical record"),
                ("1RM ATTEMPT 3", 1, 1.03, "5 min", "New PR Attempt - Overload boundary")
            ]
            for t_name, t_reps, t_pct, t_rest, t_note in test_protocol:
                rows.append({"Type": t_name, "Exercise": f"Max Protocol: {lift_name}", "Sets": 1, "Reps": t_reps, "Target %": f"{round(t_pct * 100)}%", "Calculated Weight": f"{round_weight(base_1rm * t_pct)} {unit}", "Completed Weight": "", "Rest": t_rest, "Notes": t_note})

        df_main = pd.DataFrame(rows)
        
        # Load previously saved main-lift data if it exists
        if main_state_key in st.session_state.logged_data:
            for idx_row, saved_val in st.session_state.logged_data[main_state_key].items():
                if idx_row < len(df_main):
                    df_main.at[idx_row, "Completed Weight"] = saved_val

        # Display Main Lift Table
        edited_df_main = st.data_editor(
            df_main, 
            use_container_width=True, 
            hide_index=True,
            key=f"editor_main_{w_num}_{day_name}",
            disabled=["Type", "Exercise", "Sets", "Reps", "Target %", "Calculated Weight", "Rest", "Notes"]
        )
        
        # Save updates dynamically back to state dictionary
        for index, row in edited_df_main.iterrows():
            if row["Completed Weight"] != "":
                if main_state_key not in st.session_state.logged_data:
                    st.session_state.logged_data[main_state_key] = {}
                st.session_state.logged_data[main_state_key][index] = row["Completed Weight"]


        # --- ACCESSORY LIFTS GENERATION ---
        st.markdown("<div class='section-header'>🔬 Daily Varied Accessory Targets</div>", unsafe_allow_html=True)
        acc_rows = []
        for acc in accessories_pool[w_num][day_name]:
            acc_rows.append({
                "Accessory Exercise": acc[0],
                "Target Sets": acc[1],
                "Target Reps": acc[2],
                "Intensity Metric": acc[3],
                "Weight Lifted": "",
                "Suggested Rest": "1-2 min" if acc[1] != "-" else "-"
            })
        df_acc = pd.DataFrame(acc_rows)
        
        # Load previously saved accessory data if it exists
        if acc_state_key in st.session_state.logged_data:
            for idx_row, saved_val in st.session_state.logged_data[acc_state_key].items():
                if idx_row < len(df_acc):
                    df_acc.at[idx_row, "Weight Lifted"] = saved_val

        # Display Accessory Table
        edited_df_acc = st.data_editor(
            df_acc, 
            use_container_width=True, 
            hide_index=True,
            key=f"editor_acc_{w_num}_{day_name}",
            disabled=["Accessory Exercise", "Target Sets", "Target Reps", "Intensity Metric", "Suggested Rest"]
        )

        # Save updates dynamically back to state dictionary
        for index, row in edited_df_acc.iterrows():
            if row["Weight Lifted"] != "":
                if acc_state_key not in st.session_state.logged_data:
                    st.session_state.logged_data[acc_state_key] = {}
                st.session_state.logged_data[acc_state_key][index] = row["Weight Lifted"]

st.markdown("---")
st.caption("💪 Handcrafted for Powerlifters. Update your 1RM values in the sidebar panel anytime to instantly recalculate your targets.")