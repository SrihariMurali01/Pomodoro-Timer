from tkinter import *
import pygame
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#F43B86"
RED = "#CD1818"
GREEN = "#519259"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 1
timer = ""
pygame.mixer.init()


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    global reps
    reps = 1


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    error_label.config(text="")

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # 8 rep:
    if reps == 8:
        timer_label.config(text="Break", fg=RED)
        count_down(long_break_sec)
    # 2/4/6 rep:
    elif reps % 2 == 0:
        timer_label.config(text="Break", fg=PINK)
        count_down(short_break_sec)
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)
        mark = ""
        work_sess = math.floor(reps / 2)
        for _ in range(work_sess):
            mark += "✔  "
            check_marks.config(text=mark)
            window.lift()
            window.attributes('-topmost', True)
            window.after_idle(window.attributes, '-topmost', False)
            pygame.mixer.music.load("1.mp3")
            pygame.mixer.music.play()
    reps += 1


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        # Capturing timer count so that it doesn't end just once
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=100, bg=YELLOW)

timer_label = Label(text="Timer", highlightthickness=0, bg=YELLOW)
timer_label.config(font=(FONT_NAME, 35, 'bold'), fg=GREEN)
timer_label.grid(row=0, column=1)

canvas = Canvas(width=200, height=224, bg=YELLOW,
                highlightthickness=0)  # "highlight-thickness" keyword is used for removing border around image
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 30, 'bold'))
canvas.grid(column=1, row=1)

start_btn = Button(text="Start", borderwidth=5, highlightthickness=0, command=start_timer)
start_btn.grid(row=2, column=0)

reset_btn = Button(text="Reset", borderwidth=5, highlightthickness=0, command=reset_timer)
reset_btn.grid(row=2, column=2)

check_marks = Label(fg="GREEN", bg=YELLOW, highlightthickness=0)
check_marks.grid(column=1, row=3)

error_label = Label(text="*Cannot press reset without starting the timer!", highlightthickness=0)
error_label.config(font=("Futura", 10, 'bold'), fg=RED, bg=YELLOW)
error_label.grid(column=1, row=4)

window.mainloop()
