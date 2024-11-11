import tkinter as tk
from tkinter import messagebox

def calculate_cgpa():
    try:
        totalCredits = 0
        totalWeightedGradePoints = 0

        for i, course in enumerate(course_entries):
            credit = int(course['credit'].get())
            score = int(course['score'].get())

            if credit <= 0:
                raise ValueError(f"Credits for Course {i + 1} must be positive.")
            if score < 0 or score > 100:
                raise ValueError(f"Score for Course {i + 1} must be between 0 and 100.")
            
            if score >= 90:
                grade = 10
            elif score >= 80:
                grade = 9
            elif score >= 70:
                grade = 8
            elif score >= 60:
                grade = 7
            elif score >= 50:
                grade = 6
            elif score >= 45:
                grade = 5
            elif score >= 40:
                grade = 4
            else:
                grade = 0

            totalCredits += credit
            totalWeightedGradePoints += credit * grade

        if totalCredits == 0:
            messagebox.showerror("Error", "Total credits cannot be zero.")
        else:
            Cgpa = totalWeightedGradePoints / totalCredits
            messagebox.showinfo("Result", f"Your CGPA is: {Cgpa:.2f}")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def create_course_entries():
    try:
        for widget in course_frame.winfo_children():
            widget.destroy()
        
        num_courses = int(num_courses_entry.get())
        if num_courses <= 0:
            raise ValueError("Number of courses must be positive.")

        global course_entries
        course_entries = []

        for i in range(num_courses):
            tk.Label(course_frame, text=f"Course {i + 1} - Credits:", bg="#FAFAFA", font=("Helvetica Neue", 10)).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            credit_entry = tk.Entry(course_frame, width=10, font=("Helvetica Neue", 10), relief="flat")
            credit_entry.grid(row=i, column=1, padx=5, pady=5)
            credit_entry.configure(bg="#E9ECEF", borderwidth=1)

            tk.Label(course_frame, text="Score:", bg="#FAFAFA", font=("Helvetica Neue", 10)).grid(row=i, column=2, padx=5, pady=5, sticky="e")
            score_entry = tk.Entry(course_frame, width=10, font=("Helvetica Neue", 10), relief="flat")
            score_entry.grid(row=i, column=3, padx=5, pady=5)
            score_entry.configure(bg="#E9ECEF", borderwidth=1)

            course_entries.append({'credit': credit_entry, 'score': score_entry})
        
        calculate_button.config(state="normal")

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def clear_all():
    num_courses_entry.delete(0, tk.END)
    for widget in course_frame.winfo_children():
        widget.destroy()
    calculate_button.config(state="disabled")

# Set up the main application window
root = tk.Tk()
root.title("CGPA Calculator")
root.geometry("480x480")
root.configure(bg="#FAFAFA")

# Modern title label
title_label = tk.Label(root, text="CGPA Calculator", font=("Helvetica Neue", 20, "bold"), bg="#FAFAFA", fg="#2D3436")
title_label.pack(pady=15)

# Instruction label
instructions_label = tk.Label(root, text="Step 1: Enter the number of courses and click 'Create Entries'.", 
                              font=("Helvetica Neue", 10), bg="#FAFAFA", fg="#636E72")
instructions_label.pack(pady=5)

# Input for number of courses
num_courses_entry = tk.Entry(root, width=10, font=("Helvetica Neue", 12), justify="center", relief="flat", bg="#E9ECEF")
num_courses_entry.pack(pady=5)

# Modern styled buttons
create_button = tk.Button(root, text="Create Course Entries", command=create_course_entries, 
                          font=("Helvetica Neue", 10, "bold"), bg="#74B9FF", fg="white", activebackground="#0984E3",
                          relief="flat", padx=5, pady=5)
create_button.pack(pady=10)

# Frame to hold course entries dynamically
course_frame = tk.Frame(root, bg="#FAFAFA")
course_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Calculate button with modern style
calculate_button = tk.Button(root, text="Calculate CGPA", state="disabled", command=calculate_cgpa, 
                             font=("Helvetica Neue", 12, "bold"), bg="#55EFC4", fg="white", activebackground="#00B894",
                             relief="flat", padx=5, pady=5)
calculate_button.pack(pady=20)

# Clear All button with modern style
clear_button = tk.Button(root, text="Clear All", command=clear_all, 
                         font=("Helvetica Neue", 10, "bold"), bg="#FF7675", fg="white", activebackground="#D63031",
                         relief="flat", padx=5, pady=5)
clear_button.pack(pady=5)

# Run the application
root.mainloop()

