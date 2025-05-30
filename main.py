import customtkinter as ctk
import os
import json
from datetime import datetime
import time
from PIL import Image 
import pygame
# Set theme and appearance
ctk.set_appearance_mode("dark")  # Dark mode looks modern and slick
ctk.set_default_color_theme("dark-blue")  # We'll override colors later

app = ctk.CTk()
app.title("📚 Study Tracker")
app.geometry("800x650")

# Globals for timer
timer_running = False
start_time = 0
elapsed_time = 0

# Frames
home_frame = ctk.CTkFrame(app)
today_frame = ctk.CTkFrame(app)
history_frame = ctk.CTkFrame(app)

def show_frame(frame):
    for f in (home_frame, today_frame, history_frame):
        f.pack_forget()
    frame.pack(fill="both", expand=True)

# --- Home Screen Setup ---
def setup_home():
    home_frame.configure(fg_color="#2B1B3B")  # Deep purple background
    label = ctk.CTkLabel(home_frame, text="📚 Welcome to Study Tracker", font=("Helvetica", 28, "bold"), text_color="#FF69B4")  # Hot pink text
    label.pack(pady=40)

    btn_today = ctk.CTkButton(home_frame, text="➕ Today's Plan", command=lambda: show_frame(today_frame), fg_color="#FF69B4", hover_color="#FF85C1")
    btn_today.pack(pady=10)

    btn_history = ctk.CTkButton(home_frame, text="📅 View History", command=lambda: show_frame(history_frame), fg_color="#FF69B4", hover_color="#FF85C1")
    btn_history.pack(pady=10)
        # Initialize pygame mixer
    pygame.mixer.init()

    def play_click_sound(event=None):
        try:
            pygame.mixer.music.load("alakh-sir-motivation (1).mp3")  # Replace with your sound file
            pygame.mixer.music.play()
        except Exception as e:
            print("Error playing sound:", e)

    image_path = "download.jpg"  # Make sure the file exists
    if os.path.exists(image_path):
        loaded_image = Image.open(image_path)
        resized_image = ctk.CTkImage(light_image=loaded_image, dark_image=loaded_image, size=(120, 120))

        image_label = ctk.CTkLabel(home_frame, image=resized_image, text="")  # No text, just image
        image_label.pack(side="bottom", pady=20)
        image_label.bind("<Button-1>", play_click_sound)  # Left mouse click
    else:
        print("Image not found:", image_path)


# --- Timer Functions ---
def start_timer():
    global timer_running, start_time
    if not timer_running:
        start_time = time.time() - elapsed_time
        timer_running = True
        update_timer()

def stop_timer():
    global timer_running
    timer_running = False

def update_timer():
    global elapsed_time
    if timer_running:
        elapsed_time = time.time() - start_time
        formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        timer_label.configure(text=f"⏱️ {formatted}")
        app.after(1000, update_timer)

# --- Save Today's Data ---
def save_today_data():
    global elapsed_time

    tasks = tasks_entry.get("0.0", "end").strip()
    thought = thought_entry.get("0.0", "end").strip()

    if not tasks and not thought:
        print("⚠️ No input to save.")
        return

    study_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tasks": tasks,
        "thought": thought,
        "study_time": study_time
    }

    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/{data['date']}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    import tkinter.messagebox as msgbox
    msgbox.showinfo("Saved!", "Your study data for today is saved successfully! 🥳")

# --- Today's Plan Screen ---
def setup_today():
    today_frame.configure(fg_color="#2B1B3B")

    label = ctk.CTkLabel(today_frame, text="📝 Today's Plan", font=("Arial", 22, "bold"), text_color="#FF69B4")
    label.pack(pady=20)

    global tasks_entry, thought_entry, timer_label, timer_running, start_time, elapsed_time
    timer_running = False
    start_time = 0
    elapsed_time = 0

    tasks_label = ctk.CTkLabel(today_frame, text="📌 Your Daily Targets:", text_color="#FF85C1")
    tasks_label.pack()
    tasks_entry = ctk.CTkTextbox(today_frame, width=550, height=100, corner_radius=8)
    tasks_entry.pack(pady=10)

    thought_label = ctk.CTkLabel(today_frame, text="💭 Thought of the Day:", text_color="#FF85C1")
    thought_label.pack()
    thought_entry = ctk.CTkTextbox(today_frame, width=550, height=80, corner_radius=8)
    thought_entry.pack(pady=10)

    timer_label = ctk.CTkLabel(today_frame, text="⏱️ 00:00:00", font=("Arial", 20), text_color="#FF69B4")
    timer_label.pack(pady=10)

    start_btn = ctk.CTkButton(today_frame, text="▶ Start Timer", command=start_timer, fg_color="#FF69B4", hover_color="#FF85C1")
    start_btn.pack(pady=5)

    stop_btn = ctk.CTkButton(today_frame, text="⏹ Stop Timer", command=stop_timer, fg_color="#FF69B4", hover_color="#FF85C1")
    stop_btn.pack(pady=5)

    save_btn = ctk.CTkButton(today_frame, text="💾 Save Today's Data", command=save_today_data, fg_color="#FF69B4", hover_color="#FF85C1")
    save_btn.pack(pady=10)

    back_btn = ctk.CTkButton(today_frame, text="⬅ Back to Home", command=lambda: show_frame(home_frame), fg_color="#FF69B4", hover_color="#FF85C1")
    back_btn.pack(pady=20)

        # --- Motivational Quotes ---
    left_quote = ctk.CTkLabel(today_frame, text="🌟 Keep going, you're getting closer!", font=("Arial", 12, "italic"), text_color="#C085FF")
    left_quote.place(relx=0.01, rely=0.95, anchor="sw")  # Bottom-left

    right_quote = ctk.CTkLabel(today_frame, text="💪 Discipline is the shortcut to success!", font=("Arial", 12, "italic"), text_color="#C085FF")
    right_quote.place(relx=0.99, rely=0.95, anchor="se")  # Bottom-right

# --- History Screen with Search Bar ---
def setup_history():
    history_frame.configure(fg_color="#2B1B3B")

    label = ctk.CTkLabel(history_frame, text="📖 Past Study Logs", font=("Arial", 22, "bold"), text_color="#FF69B4")
    label.pack(pady=20)

    global search_entry, log_buttons_frame

    # Search bar frame
    # Search bar frame
    search_frame = ctk.CTkFrame(history_frame, fg_color="#3E2B5B", corner_radius=10, width=300,height=40)
    search_frame.pack_propagate(False)
    search_frame.pack(pady=10, padx=10)  # Remove fill="x"
    search_frame.pack_propagate(False)  # Prevent auto resizing
    search_frame.configure(width=300)  # Adjust width as needed

    search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Search by date (YYYY-MM-DD)...", corner_radius=8)
    search_entry.pack(side="left", padx=(10, 5), pady=10)

    search_entry.bind("<KeyRelease>", lambda e: filter_history())

    clear_btn = ctk.CTkButton(search_frame, text="❌ Clear", width=70, command=clear_search, fg_color="#FF69B4", hover_color="#FF85C1")
    clear_btn.pack(side="left", padx=5, pady=10)

    # Scrollable frame for log buttons
    log_buttons_frame = ctk.CTkScrollableFrame(history_frame, width=750, height=300, fg_color="#2B1B3B", corner_radius=8)
    log_buttons_frame.pack(pady=10, padx=20)

    # Back button
    back_btn_history = ctk.CTkButton(history_frame, text="⬅ Back to Home", command=lambda: show_frame(home_frame), fg_color="#FF69B4", hover_color="#FF85C1")
    back_btn_history.pack(pady=20)



    load_history_list()

def clear_search():
    search_entry.delete(0, "end")
    filter_history()

def load_history_list():
    # Load all JSON filenames
    if not os.path.exists("data"):
        os.makedirs("data")

    files = sorted([f for f in os.listdir("data") if f.endswith(".json")], reverse=True)
    return files

def filter_history():
    query = search_entry.get().strip()
    all_files = load_history_list()

    # Clear existing buttons
    for widget in log_buttons_frame.winfo_children():
        widget.destroy()

    filtered_files = []
    if query == "":
        filtered_files = all_files
    else:
        # Filter by substring match (date format YYYY-MM-DD)
        filtered_files = [f for f in all_files if query in f]

    if not filtered_files:
        no_label = ctk.CTkLabel(log_buttons_frame, text="No logs found for that date!", font=("Arial", 16), text_color="#FF85C1")
        no_label.pack(pady=20)
        return

    # Create buttons for filtered files
    for file in filtered_files:
        date_str = file[:-5]
        btn = ctk.CTkButton(log_buttons_frame, text=date_str, width=200, fg_color="#FF69B4", hover_color="#FF85C1",
                             command=lambda d=date_str: show_log(d))
        btn.pack(pady=5)

def show_log(date_str):
    # Remove previous log widgets if any
    for widget in history_frame.winfo_children():
        if hasattr(widget, 'is_log_widget') and widget.is_log_widget:
            widget.destroy()

    filepath = f"data/{date_str}.json"
    if not os.path.exists(filepath):
        return

    with open(filepath, "r") as f:
        data = json.load(f)

    tasks = data.get("tasks", "No tasks found.")
    thought = data.get("thought", "No thoughts found.")
    study_time = data.get("study_time", "00:00:00")

    # Display the info below log_buttons_frame
    # To avoid overlap, create a new frame for log details

    if hasattr(show_log, 'log_detail_frame'):
        show_log.log_detail_frame.destroy()

    show_log.log_detail_frame = ctk.CTkFrame(history_frame, fg_color="#3E2B5B", corner_radius=10)
    show_log.log_detail_frame.pack(padx=20, pady=10, fill="both", expand=False)

    tasks_label = ctk.CTkLabel(show_log.log_detail_frame, text="📌 Tasks:", font=("Arial", 14, "bold"), text_color="#FF85C1")
    tasks_label.pack(pady=(10,0))

    tasks_text = ctk.CTkTextbox(show_log.log_detail_frame, width=700, height=100, corner_radius=8)
    tasks_text.insert("0.0", tasks)
    tasks_text.configure(state="disabled")
    tasks_text.pack()

    thought_label = ctk.CTkLabel(show_log.log_detail_frame, text="💭 Thought of the Day:", font=("Arial", 14, "bold"), text_color="#FF85C1")
    thought_label.pack(pady=(10,0))

    thought_text = ctk.CTkTextbox(show_log.log_detail_frame, width=700, height=80, corner_radius=8)
    thought_text.insert("0.0", thought)
    thought_text.configure(state="disabled")
    thought_text.pack()

    time_label = ctk.CTkLabel(show_log.log_detail_frame, text=f"⏱️ Study Time: {study_time}", font=("Arial", 14, "bold"), text_color="#FF69B4")
    time_label.pack(pady=15)

def on_resize(event):
    print("Window size:", event.width, event.height)

app.bind("<Configure>", on_resize)

# Setup screens
setup_home()
setup_today()
setup_history()

show_frame(home_frame)

app.mainloop()