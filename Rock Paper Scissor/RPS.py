import tkinter as tk
import random
from tkinter import messagebox

choices = ['Rock', 'Paper', 'Scissors']
rules = {"Rock": "Scissors", "Scissors": "Paper", "Paper": "Rock"}

user_score = 0
computer_score = 0

def play(user_choice):
    global user_score, computer_score
    computer_choice = random.choice(choices)

    user_label.config(text=f"You picked: {user_choice}")
    comp_label.config(text=f"Computer picked: {computer_choice}")

    if user_choice == computer_choice:
        result_label.config(text="It's a TIE", fg="blue")
    elif rules[user_choice] == computer_choice:
        result_label.config(text=f"{user_choice} beats {computer_choice}! You WIN!", fg="green")
        user_score += 1
    else:
        result_label.config(text=f"{computer_choice} beats {user_choice}! Computer Wins!", fg="red")
        computer_score += 1

    score_label.config(text=f"Score: You {user_score} - {computer_score} Computer")

    if not messagebox.askyesno("Play Again?", "Wanna try again?"):
        quit_game()

def quit_game():
    if user_score > computer_score:
        winner_msg = f"You win!\nFinal Score: You {user_score} - {computer_score} Computer"
    elif computer_score > user_score:
        winner_msg = f"Computer wins!\nFinal Score: You {user_score} - {computer_score} Computer"
    else:
        winner_msg = f"It's a DRAW\nFinal Score: You {user_score} - {computer_score} Computer"

    messagebox.showinfo("Game Over", winner_msg)
    root.destroy()

root = tk.Tk()
root.title("Rock-Paper-Scissors")
root.geometry("400x450")
root.resizable(False, False)

title_label = tk.Label(root, text="Rock-Paper-Scissors", font=("Comic Sans MS", 16, "bold"))
title_label.pack(pady=10)

instructions = tk.Label(root, text="Pick Rock, Paper or Scissors and see if you win!", 
                        font=("Arial", 10), wraplength=350, justify="center", fg="gray")
instructions.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Rock", width=10, height=2, bg="lightgray", command=lambda: play("Rock")).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Paper", width=10, height=2, bg="lightyellow", command=lambda: play("Paper")).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Scissors", width=10, height=2, bg="lightpink", command=lambda: play("Scissors")).grid(row=0, column=2, padx=10)

user_label = tk.Label(root, text="", font=("Arial", 12))
user_label.pack()

comp_label = tk.Label(root, text="", font=("Arial", 12))
comp_label.pack()

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
result_label.pack(pady=10)

score_label = tk.Label(root, text="Score: You 0 - 0 Computer", font=("Arial", 12))
score_label.pack()

quit_btn = tk.Button(root, text="Quit Game", width=12, command=quit_game, bg="orange")
quit_btn.pack(pady=15)

root.mainloop()