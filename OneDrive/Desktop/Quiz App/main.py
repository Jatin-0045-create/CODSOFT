import customtkinter as ctk
import random
import json

with open("questions.json", "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

ctk.set_appearance_mode("dark")

class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Quiz App")
        self.geometry("750x550")
        self.subject = ctk.StringVar(value="Computer")
        self.difficulty = ctk.StringVar(value="Hard")
        self.questions = []
        self.current_q = 0
        self.score = 0
        self.time_left = 20
        self.running = False
        self.setup_ui()
    
    def setup_ui(self):
        header = ctk.CTkFrame(self, height=80)
        header.pack(fill="x", padx=20, pady=10)
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="Quiz App", font=("Arial", 20, "bold")).pack(pady=5)
        controls = ctk.CTkFrame(header)
        controls.pack()
        ctk.CTkLabel(controls, text="Subject:").grid(row=0, column=0, padx=5)
        ctk.CTkComboBox(controls, values=["Math", "Science", "Computer", "General Knowledge"], variable=self.subject, width=120).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(controls, text="Level:").grid(row=0, column=2, padx=5)
        ctk.CTkComboBox(controls, values=["Easy", "Medium", "Hard"], variable=self.difficulty, width=100).grid(row=0, column=3, padx=5)
        ctk.CTkButton(controls, text="Start", command=self.start_quiz, width=80).grid(row=0, column=4, padx=10)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=(0,10))
        self.welcome = ctk.CTkLabel(self.main_frame, text="📚\n\nSelect subject and difficulty\nthen click Start!", font=("Arial", 18), justify="center")
        self.welcome.pack(expand=True)
        self.quiz_frame = ctk.CTkFrame(self.main_frame)

        info = ctk.CTkFrame(self.quiz_frame, height=50)
        info.pack(fill="x", padx=10, pady=10)
        info.pack_propagate(False)
        self.timer_label = ctk.CTkLabel(info, text="Time: 20s", font=("Arial", 14, "bold"))
        self.timer_label.pack(side="left", padx=20, pady=15)
        self.progress_label = ctk.CTkLabel(info, text="Q1/5 | Score: 0", font=("Arial", 14))
        self.progress_label.pack(side="right", padx=20, pady=15)

        self.question_label = ctk.CTkLabel(self.quiz_frame, text="", font=("Arial", 16), wraplength=600, height=60)
        self.question_label.pack(padx=20, pady=10)

        self.buttons = []
        for i in range(4):
            btn = ctk.CTkButton(self.quiz_frame, text="", height=40, command=lambda x=i: self.answer_click(x))
            btn.pack(fill="x", padx=40, pady=5)
            self.buttons.append(btn)

        self.bottom_frame = ctk.CTkFrame(self, height=50)
        self.bottom_frame.pack(side="bottom", fill="x")
        self.bottom_frame.pack_propagate(False)
        self.stop_btn = ctk.CTkButton(self.bottom_frame, text="Stop", command=self.stop_quiz, fg_color="red")
        self.restart_btn = ctk.CTkButton(self.bottom_frame, text="Restart", command=self.restart, fg_color="orange")
        self.exit_btn = ctk.CTkButton(self.bottom_frame, text="Exit", command=self.quit, fg_color="gray")
        self.stop_btn.grid_remove()
        self.restart_btn.grid_remove()
        self.exit_btn.grid_remove()
    
    def start_quiz(self):
        subject_questions = QUESTIONS[self.subject.get()][self.difficulty.get()]
        self.questions = random.sample(subject_questions, 5)
        for i, (q, opts, ans) in enumerate(self.questions):
            shuffled_opts = opts.copy()
            random.shuffle(shuffled_opts)
            self.questions[i] = (q, shuffled_opts, ans)
        self.current_q = 0
        self.score = 0
        self.time_left = 20
        self.running = True
        self.welcome.pack_forget()
        self.quiz_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.stop_btn.grid(row=0, column=0, padx=5, pady=5)
        self.restart_btn.grid_remove()
        self.exit_btn.grid_remove()
        self.load_question()
        self.update_timer()
    
    def load_question(self):
        if self.current_q >= 5:
            self.end_quiz()
            return
        q, opts, _ = self.questions[self.current_q]
        self.question_label.configure(text=f"Q{self.current_q+1}: {q}")
        for i, opt in enumerate(opts):
            self.buttons[i].configure(text=f"{chr(65+i)}) {opt}", state="normal", fg_color="#1f538d")
        self.progress_label.configure(text=f"Q{self.current_q+1}/5 | Score: {self.score}")
        self.time_left = 20
        for btn in self.buttons:
            btn.pack(fill="x", padx=40, pady=5)

    def answer_click(self, idx):
        if not self.running:
            return
        _, opts, correct = self.questions[self.current_q]
        if opts[idx] == correct:
            self.score += 1
            self.buttons[idx].configure(fg_color="green")
        else:
            self.buttons[idx].configure(fg_color="red")
            for i, opt in enumerate(opts):
                if opt == correct:
                    self.buttons[i].configure(fg_color="green")
        for btn in self.buttons:
            btn.configure(state="disabled")
        self.after(1000, self.next_question)
    
    def next_question(self):
        self.current_q += 1
        self.load_question()
    
    def update_timer(self):
        if not self.running:
            return
        self.timer_label.configure(text=f"Time: {self.time_left}s", text_color="red" if self.time_left <=5 else "white")
        if self.time_left > 0:
            self.time_left -=1
            self.after(1000, self.update_timer)
        else:
            self.next_question()
    
    def stop_quiz(self):
        self.running = False
        attempted = max(0, self.current_q)
        if attempted == 0:
            result_text = "Quiz Stopped!\nNo questions attempted."
        else:
            percentage = (self.score / attempted) * 100
            result_text = f"Quiz Stopped!\nScore: {self.score}/{attempted} ({percentage:.0f}%)"
        self.question_label.configure(text=result_text, font=("Arial", 20, "bold"), justify="center")
        for btn in self.buttons:
            btn.pack_forget()
        self.progress_label.configure(text="")
        self.timer_label.configure(text="")
        self.show_end_buttons()
    
    def end_quiz(self):
        self.running = False
        percentage = (self.score / 5) * 100
        result = "Excellent! 🌟" if percentage >= 80 else "Good! 👍" if percentage >= 60 else "Try again! 💪"
        result_text = f"Quiz Complete!\n{result}\nScore: {self.score}/5 ({percentage:.0f}%)"
        self.question_label.configure(text=result_text, font=("Arial", 20, "bold"), justify="center")
        for btn in self.buttons:
            btn.pack_forget()
        self.progress_label.configure(text="")
        self.timer_label.configure(text="")
        self.show_end_buttons()

    def show_end_buttons(self):
        self.stop_btn.grid_remove()
        for widget in self.bottom_frame.winfo_children():
            widget.grid_forget()
        self.restart_btn.configure(fg_color="orange", hover_color="#cc7000")
        self.restart_btn.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.exit_btn.configure(fg_color="red", hover_color="#990000")
        self.exit_btn.grid(row=0, column=1, padx=20, pady=10, sticky="e")

    def restart(self):
        self.running = False
        self.quiz_frame.pack_forget()
        self.welcome.pack(expand=True)
        self.question_label.configure(text="")
        for btn in self.buttons:
            btn.configure(text="", state="normal", fg_color="#1f538d")
            btn.pack_forget()
        self.restart_btn.grid_remove()
        self.exit_btn.grid_remove()

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
