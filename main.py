from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
#  (colors obtained from https://colorhunt.co/)
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REPS = 0
TIMER = 0

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global REPS
    # stop the timer
    window.after_cancel(TIMER)
    # timer text 00:00
    canvas.itemconfig(timer_text, text="00:00")
    # timer title "Timer"
    time_label.config(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 48))
    # reset checks
    check_label.config(text="")
    # clear reps
    REPS = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global REPS
    # increment reps every time you call the start_timer()
    REPS+=1
    # the number of seconds needed to calculate the work periods is
    # 25 * 60 = 1,500
    work_sec = WORK_MIN * 60
    # the number of seconds needed to calculate the short break periods is
    # 5 * 60 = 300
    short_break_sec = SHORT_BREAK_MIN * 60
    # the number of seconds needed to calculate the long work periods is
    # 20 * 60 = 1,200
    long_break_sec = LONG_BREAK_MIN * 60
    # if the user is on a long break or the 8th rep
    # (25, 5, 25, 5, 25, 20)
    if REPS % 8 == 0:
        time_label.config(text="Long Break", fg=RED, bg=YELLOW, font=(FONT_NAME, 48))
        count_down(long_break_sec)
    # if the user is on a short break
    elif REPS % 2 == 0:
        time_label.config(text="Short Break", fg=PINK, bg=YELLOW, font=(FONT_NAME, 48))
        count_down(short_break_sec)
    # if the user is on a work period
    else:
        count_down(work_sec)
        time_label.config(text="WORK", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 48))


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    """needs to be in terms 00:00"""
    # this obtains the largest whole number
    count_min = math.floor(count / 60)
    # this obtains the seconds relative for the minute
    count_sec = count % 60
    # if the seconds are within the last 10 of the minute format it appropriately
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    # other wise just make sure the format is correct in general
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    # if the count is greater than zero we'll continue to count down
    # the .after counts in milli seconds, recursively counts down by 1
    if count > 0:
        global TIMER
        TIMER = window.after(1000, count_down, count - 1)
    # else start the timer
    else:
        start_timer() # start
        marks = "" # marks will hold all check marks
        # a work session is going to be: 1 work session for every 2 reps
        # floor rounds down to the nearest integer
        work_sessions = math.floor(REPS/2)
        # from (0,2)
        for _ in range(work_sessions):
            # increment the label
            marks += "✔"
        # update check label
        check_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
# adjust padding
window.config(padx=100, pady=50, bg=YELLOW)

# ---------------------------- LABELS ------------------------------- #
# TIMER label
time_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 48))
time_label.grid(column=1, row=1)
# CHECKMARK label
check_label = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30))
check_label.grid(column=1, row=4)

# ---------------------------- CANVAS ------------------------------- #
# create a canvas, canvas controls the shape of the window
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# create a tomato image using photo image
tomato_img = PhotoImage(file="tomato.png")
# you need to set the y and x axis of where the image should be on the screen
# you can use roughly half of the screen width and height to center the image
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
# use grid instead of pack
canvas.grid(column=1, row=2)

# -------------------------- BUTTONS ---------------------------------- #
# start button
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=3)
# reset button
reset_button = Button(text="Reset", bg=YELLOW, highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=3)



window.mainloop()