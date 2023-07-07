from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#FFB3B3"
RED = "#F55C47"
GREEN = "#8BDB81"
YELLOW = "#FFF9C9"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
time_current = 0
timer = None
is_paused = False


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, time_current, is_paused
    window.after_cancel(timer)
    timer_lab.config(text="Timer", fg=GREEN)
    button_pau.config(text="Pause")
    checkmark.config(text="")
    canvas.itemconfig(timer_text, text="00:00")
    time_current = 0
    reps = 0
    is_paused = False


# ---------------------------- PAUSE MECHANISM -------------------------------- #
def pause_timer():
    global is_paused, time_current
    if time_current != 0:  # at the beginning hitting the pause button will not cause any changes
        if not is_paused:  # if initially is_pause is not True (if False)
            is_paused = True
            button_pau.config(text="Resume")
        else:
            is_paused = False
            button_pau.config(text="Pause")
            count_down(time_current)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, is_paused, time_current
    is_paused = False
    reps += 1
    if not is_paused:  # if the timer is not paused (not true), start from the beginning
        if reps % 2 != 0:
            count_down(WORK_MIN * 60)
            timer_lab.config(text="Work", fg=GREEN)
        elif reps % 8 == 0:
            count_down(LONG_BREAK_MIN * 60)
            timer_lab.config(text="Long Break", fg=RED)
        else:
            count_down(SHORT_BREAK_MIN * 60)
            timer_lab.config(text="Break", fg=PINK)
    else:  # if the timer is resumed, start from the current time
        count_down(time_current)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(num):
    global reps, time_current, timer
    if not is_paused:  # if the timer is not paused (not true)
        num_min = math.floor(num / 60)
        num_sec = int(num % 60)
        if num_sec < 10:
            num_sec = f'0{num_sec}'
        if num_min == 0:
            num_min = "00"
        canvas.itemconfig(timer_text, text=f"{num_min}:{num_sec}")
        if num > 0:
            timer = window.after(1000, count_down,
                                 num - 1)  # take the amount of time in ms to wait, then call a function
            # with args being the args to be passed into the function
            time_current = num  # pass the current counting down time to time_current
        else:
            start_timer()  # start the clock for the next session
            if reps % 2 == 0:
                checkmark.config(text="✔")
            else:
                checkmark.config(text="")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=100, pady=50, bg=YELLOW)
window.title("Pomodoro")

# CANVAS
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato = PhotoImage(file="tomato.png")  # create the photo
canvas.create_image(100, 112, image=tomato)  # coordinate at the center of the canvas
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))  # add text on top
canvas.grid(column=1, row=2)

# BUTTONS START RESET AND PAUSE
button_start = Button(text="Start", highlightthickness=0, command=start_timer)
button_start.grid(column=0, row=3)

button_reset = Button(text="Reset", highlightthickness=0, command=reset_timer)
button_reset.grid(column=2, row=3)

button_pau = Button(text="Pause", highlightthickness=0, command=pause_timer)
button_pau.grid(column=1, row=5)

# LABELS
timer_lab = Label(text="Timer", background=YELLOW, font=(FONT_NAME, 30, "bold"), fg=GREEN)
timer_lab.grid(column=1, row=0)

checkmark = Label(bg=YELLOW, fg=GREEN)
checkmark.grid(column=1, row=4)

window.mainloop()
