# ============================================================
# AI RECRUITMENT SYSTEM
# PART 2
#
# Features:
# - HR Login
# - Dashboard
# - Job Management
# - Candidate Management
# - PDF/DOCX Resume Upload
# - Resume Text Extraction
# - AI Resume Scoring
# - Automatic Shortlisting
# - Candidate Ranking
# - Reports
# - Interview Scheduler
# - Analytics
# - Excel Export
# - Resume Viewer
# ============================================================


import os
import sys
import subprocess
import webbrowser
from datetime import datetime


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


import pandas as pd


from database import (
    fetch_all,
    fetch_one,
    execute_query
)


from resume_parser import (
    read_resume,
    extract_email,
    extract_phone,
    extract_skills,
    extract_experience
)


from ai_engine import (
    calculate_score,
    get_status,
    get_recommendation,
    get_matched_skills,
    get_missing_skills
)


# ============================================================
# CONSTANTS
# ============================================================

RESUME_FOLDER = "resumes"

os.makedirs(
    RESUME_FOLDER,
    exist_ok=True
)


# ============================================================
# APPLICATION
# ============================================================

class RecruitmentApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "AI Recruitment System"
        )

        self.root.geometry(
            "1200x750"
        )

        self.root.minsize(
            1000,
            650
        )

        self.current_user = None

        self.current_role = None

        self.setup_style()

        self.show_login()


    # ========================================================
    # STYLE
    # ========================================================

    def setup_style(self):

        style = ttk.Style()

        try:

            style.theme_use("clam")

        except:

            pass


        style.configure(
            "Treeview",
            rowheight=30,
            font=("Arial", 10)
        )


        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )


        style.configure(
            "TButton",
            font=("Arial", 10),
            padding=6
        )


        style.configure(
            "TLabel",
            font=("Arial", 10)
        )


        style.configure(
            "TNotebook.Tab",
            padding=(12, 8)
        )


    # ========================================================
    # CLEAR WINDOW
    # ========================================================

    def clear_window(self):

        for widget in self.root.winfo_children():

            widget.destroy()


    # ========================================================
    # LOGIN
    # ========================================================

    def show_login(self):

        self.clear_window()

        frame = tk.Frame(
            self.root,
            padx=40,
            pady=40
        )

        frame.pack(
            expand=True
        )


        tk.Label(
            frame,
            text="AI RECRUITMENT SYSTEM",
            font=("Arial", 25, "bold")
        ).pack(
            pady=(0, 10)
        )


        tk.Label(
            frame,
            text="HR Management Portal",
            font=("Arial", 12)
        ).pack(
            pady=(0, 30)
        )


        tk.Label(
            frame,
            text="Username"
        ).pack(
            anchor="w"
        )


        self.login_username = tk.Entry(
            frame,
            width=35,
            font=("Arial", 11)
        )

        self.login_username.pack(
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Password"
        ).pack(
            anchor="w"
        )


        self.login_password = tk.Entry(
            frame,
            width=35,
            show="*",
            font=("Arial", 11)
        )

        self.login_password.pack(
            pady=(5, 20)
        )


        ttk.Button(
            frame,
            text="Login",
            command=self.login
        ).pack(
            fill="x"
        )


        ttk.Button(
            frame,
            text="Create HR Account",
            command=self.show_register
        ).pack(
            fill="x",
            pady=10
        )


        self.login_username.focus()


        self.root.bind(
            "<Return>",
            lambda event: self.login()
        )


    # ========================================================
    # LOGIN FUNCTION
    # ========================================================

    def login(self):

        username = (
            self.login_username
            .get()
            .strip()
        )

        password = (
            self.login_password
            .get()
        )


        if not username or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please enter username and password."
            )

            return


        user = fetch_one(
            """
            SELECT id, username, password, role
            FROM users
            WHERE username = %s
            """,
            (username,)
        )


        if user is None:

            messagebox.showerror(
                "Login Failed",
                "Username or password is incorrect."
            )

            return


        if password != user[2]:

            messagebox.showerror(
                "Login Failed",
                "Username or password is incorrect."
            )

            return


        self.current_user = user[1]

        self.current_role = user[3]


        self.root.unbind(
            "<Return>"
        )


        self.show_dashboard()


    # ========================================================
    # REGISTER
    # ========================================================

    def show_register(self):

        self.clear_window()

        frame = tk.Frame(
            self.root,
            padx=40,
            pady=40
        )

        frame.pack(
            expand=True
        )


        tk.Label(
            frame,
            text="CREATE HR ACCOUNT",
            font=("Arial", 22, "bold")
        ).pack(
            pady=(0, 25)
        )


        tk.Label(
            frame,
            text="Username"
        ).pack(
            anchor="w"
        )


        self.reg_username = tk.Entry(
            frame,
            width=35
        )

        self.reg_username.pack(
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Password"
        ).pack(
            anchor="w"
        )


        self.reg_password = tk.Entry(
            frame,
            width=35,
            show="*"
        )

        self.reg_password.pack(
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Confirm Password"
        ).pack(
            anchor="w"
        )


        self.reg_confirm = tk.Entry(
            frame,
            width=35,
            show="*"
        )

        self.reg_confirm.pack(
            pady=(5, 20)
        )


        ttk.Button(
            frame,
            text="Create Account",
            command=self.register_user
        ).pack(
            fill="x"
        )


        ttk.Button(
            frame,
            text="Back to Login",
            command=self.show_login
        ).pack(
            fill="x",
            pady=10
        )


    # ========================================================
    # REGISTER USER
    # ========================================================

    def register_user(self):

        username = (
            self.reg_username
            .get()
            .strip()
        )

        password = self.reg_password.get()

        confirm = self.reg_confirm.get()


        if not username or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )

            return


        if password != confirm:

            messagebox.showerror(
                "Password Error",
                "Passwords do not match."
            )

            return


        existing = fetch_one(
            """
            SELECT id
            FROM users
            WHERE username = %s
            """,
            (username,)
        )


        if existing:

            messagebox.showerror(
                "Registration Error",
                "Username already exists."
            )

            return


        success = execute_query(
            """
            INSERT INTO users
            (username, password, role)
            VALUES
            (%s, %s, %s)
            """,
            (
                username,
                password,
                "HR"
            )
        )


        if success:

            messagebox.showinfo(
                "Success",
                "HR account created successfully."
            )

            self.show_login()

        else:

            messagebox.showerror(
                "Error",
                "Unable to create account."
            )


    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.clear_window()


        top = tk.Frame(
            self.root,
            height=60
        )

        top.pack(
            fill="x"
        )


        tk.Label(
            top,
            text="AI Recruitment System",
            font=("Arial", 18, "bold")
        ).pack(
            side="left",
            padx=20,
            pady=15
        )


        tk.Label(
            top,
            text=f"Logged in as: {self.current_user}",
            font=("Arial", 10)
        ).pack(
            side="right",
            padx=20
        )


        nav = tk.Frame(
            self.root
        )

        nav.pack(
            fill="x",
            padx=15,
            pady=10
        )


        ttk.Button(
            nav,
            text="Dashboard",
            command=self.show_dashboard
        ).pack(
            side="left",
            padx=4
        )


        ttk.Button(
            nav,
            text="Jobs",
            command=self.show_jobs
        ).pack(
            side="left",
            padx=4
        )


        ttk.Button(
            nav,
            text="Candidates",
            command=self.show_candidates
        ).pack(
            side="left",
            padx=4
        )


        ttk.Button(
            nav,
            text="Interviews",
            command=self.show_interviews
        ).pack(
            side="left",
            padx=4
        )


        ttk.Button(
            nav,
            text="Reports",
            command=self.show_reports
        ).pack(
            side="left",
            padx=4
        )


        ttk.Button(
            nav,
            text="Analytics",
            command=self.show_analytics
        ).pack(
            side="left",
            padx=4
        )


        ttk.Button(
            nav,
            text="Logout",
            command=self.logout
        ).pack(
            side="right",
            padx=4
        )


        content = tk.Frame(
            self.root
        )

        content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )


        jobs = fetch_one(
            "SELECT COUNT(*) FROM jobs"
        )


        candidates = fetch_one(
            "SELECT COUNT(*) FROM candidates"
        )


        shortlisted = fetch_one(
            """
            SELECT COUNT(*)
            FROM candidates
            WHERE status = 'Shortlisted'
            """
        )


        rejected = fetch_one(
            """
            SELECT COUNT(*)
            FROM candidates
            WHERE status = 'Rejected'
            """
        )


        interviews = fetch_one(
            """
            SELECT COUNT(*)
            FROM interviews
            """
        )


        job_count = jobs[0] if jobs else 0

        candidate_count = (
            candidates[0]
            if candidates
            else 0
        )

        shortlisted_count = (
            shortlisted[0]
            if shortlisted
            else 0
        )

        rejected_count = (
            rejected[0]
            if rejected
            else 0
        )

        interview_count = (
            interviews[0]
            if interviews
            else 0
        )


        cards = [

            ("Total Jobs", job_count),

            ("Candidates", candidate_count),

            ("Shortlisted", shortlisted_count),

            ("Rejected", rejected_count),

            ("Interviews", interview_count)
        ]


        for index, (title, value) in enumerate(cards):

            frame = tk.Frame(
                content,
                relief="ridge",
                borderwidth=1,
                padx=20,
                pady=20
            )

            frame.grid(
                row=0,
                column=index,
                padx=8,
                sticky="nsew"
            )


            tk.Label(
                frame,
                text=title,
                font=("Arial", 10)
            ).pack()


            tk.Label(
                frame,
                text=str(value),
                font=("Arial", 24, "bold")
            ).pack(
                pady=10
            )


            content.grid_columnconfigure(
                index,
                weight=1
            )


        welcome = tk.Label(
            content,
            text=(
                "\nWelcome to the AI Recruitment System!\n\n"
                "Use the navigation buttons to manage jobs, "
                "candidates and interviews.\n\n"
                "AI Resume Screening:\n"
                "1. Upload a PDF/DOCX resume\n"
                "2. Select the relevant job\n"
                "3. Run AI Screening\n"
                "4. Candidate receives a score from 0–100\n"
                "5. Candidate is automatically ranked\n"
                "6. Status is automatically assigned"
            ),
            font=("Arial", 13),
            justify="left"
        )

        welcome.grid(
            row=1,
            column=0,
            columnspan=5,
            sticky="w",
            pady=40
        )


    # ========================================================
    # JOB MANAGEMENT
    # ========================================================

    def show_jobs(self):

        self.clear_window()


        header = tk.Frame(
            self.root
        )

        header.pack(
            fill="x",
            padx=20,
            pady=15
        )


        tk.Label(
            header,
            text="Job Management",
            font=("Arial", 20, "bold")
        ).pack(
            side="left"
        )


        ttk.Button(
            header,
            text="Back to Dashboard",
            command=self.show_dashboard
        ).pack(
            side="right"
        )


        buttons = tk.Frame(
            self.root
        )

        buttons.pack(
            fill="x",
            padx=20
        )


        ttk.Button(
            buttons,
            text="Add Job",
            command=self.add_job_window
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            buttons,
            text="Edit Selected",
            command=self.edit_selected_job
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            buttons,
            text="Delete Selected",
            command=self.delete_selected_job
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            buttons,
            text="Refresh",
            command=self.load_jobs
        ).pack(
            side="left",
            padx=5
        )


        search_frame = tk.Frame(
            self.root
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )


        tk.Label(
            search_frame,
            text="Search:"
        ).pack(
            side="left"
        )


        self.job_search = tk.Entry(
            search_frame,
            width=40
        )

        self.job_search.pack(
            side="left",
            padx=10
        )


        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_jobs
        ).pack(
            side="left"
        )


        table_frame = tk.Frame(
            self.root
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )


        columns = (
            "ID",
            "Job Title",
            "Skills",
            "Experience",
            "Qualification",
            "Status"
        )


        self.job_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )


        widths = {

            "ID": 60,

            "Job Title": 180,

            "Skills": 260,

            "Experience": 100,

            "Qualification": 180,

            "Status": 100
        }


        for column in columns:

            self.job_tree.heading(
                column,
                text=column
            )

            self.job_tree.column(
                column,
                width=widths[column]
            )


        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.job_tree.yview
        )


        self.job_tree.configure(
            yscrollcommand=scrollbar.set
        )


        self.job_tree.pack(
            side="left",
            fill="both",
            expand=True
        )


        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.load_jobs()


    # ========================================================
    # LOAD JOBS
    # ========================================================

    def load_jobs(self, search=""):

        for item in self.job_tree.get_children():

            self.job_tree.delete(item)


        if search:

            value = f"%{search}%"


            rows = fetch_all(
                """
                SELECT
                    job_id,
                    job_title,
                    required_skills,
                    experience,
                    qualification,
                    status
                FROM jobs
                WHERE job_title LIKE %s
                OR required_skills LIKE %s
                ORDER BY job_id DESC
                """,
                (value, value)
            )

        else:

            rows = fetch_all(
                """
                SELECT
                    job_id,
                    job_title,
                    required_skills,
                    experience,
                    qualification,
                    status
                FROM jobs
                ORDER BY job_id DESC
                """
            )


        for row in rows:

            self.job_tree.insert(
                "",
                "end",
                values=row
            )


    # ========================================================
    # SEARCH JOBS
    # ========================================================

    def search_jobs(self):

        search = (
            self.job_search
            .get()
            .strip()
        )

        self.load_jobs(
            search
        )


    # ========================================================
    # ADD JOB
    # ========================================================

    def add_job_window(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Add Job"
        )

        window.geometry(
            "550x600"
        )


        frame = tk.Frame(
            window,
            padx=25,
            pady=20
        )

        frame.pack(
            fill="both",
            expand=True
        )


        tk.Label(
            frame,
            text="Add New Job",
            font=("Arial", 18, "bold")
        ).pack(
            pady=(0, 20)
        )


        tk.Label(
            frame,
            text="Job Title"
        ).pack(
            anchor="w"
        )


        title_entry = tk.Entry(
            frame
        )

        title_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Required Skills"
        ).pack(
            anchor="w"
        )


        skills_entry = tk.Entry(
            frame
        )

        skills_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Experience (Years)"
        ).pack(
            anchor="w"
        )


        experience_entry = tk.Entry(
            frame
        )

        experience_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Qualification"
        ).pack(
            anchor="w"
        )


        qualification_entry = tk.Entry(
            frame
        )

        qualification_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Job Description"
        ).pack(
            anchor="w"
        )


        description_entry = tk.Text(
            frame,
            height=7
        )

        description_entry.pack(
            fill="both",
            pady=(5, 15)
        )


        def save_job():

            title = (
                title_entry
                .get()
                .strip()
            )

            skills = (
                skills_entry
                .get()
                .strip()
            )

            experience = (
                experience_entry
                .get()
                .strip()
            )

            qualification = (
                qualification_entry
                .get()
                .strip()
            )

            description = (
                description_entry
                .get(
                    "1.0",
                    "end"
                )
                .strip()
            )


            if not title or not skills:

                messagebox.showwarning(
                    "Missing Information",
                    "Job title and required skills are required.",
                    parent=window
                )

                return


            try:

                experience_value = int(
                    experience
                    if experience
                    else 0
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Experience",
                    "Experience must be a number.",
                    parent=window
                )

                return


            success = execute_query(
                """
                INSERT INTO jobs
                (
                    job_title,
                    required_skills,
                    experience,
                    qualification,
                    job_description
                )
                VALUES
                (%s, %s, %s, %s, %s)
                """,
                (
                    title,
                    skills,
                    experience_value,
                    qualification,
                    description
                )
            )


            if success:

                messagebox.showinfo(
                    "Success",
                    "Job added successfully.",
                    parent=window
                )

                window.destroy()

                self.load_jobs()

            else:

                messagebox.showerror(
                    "Error",
                    "Unable to add job.",
                    parent=window
                )


        ttk.Button(
            frame,
            text="Save Job",
            command=save_job
        ).pack(
            fill="x"
        )


    # ========================================================
    # EDIT JOB
    # ========================================================

    def edit_selected_job(self):

        selected = self.job_tree.selection()


        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a job first."
            )

            return


        values = self.job_tree.item(
            selected[0],
            "values"
        )


        job_id = values[0]


        existing = fetch_one(
            """
            SELECT
                job_title,
                required_skills,
                experience,
                qualification,
                job_description,
                status
            FROM jobs
            WHERE job_id = %s
            """,
            (job_id,)
        )


        if not existing:

            messagebox.showerror(
                "Error",
                "Unable to load job."
            )

            return


        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Edit Job"
        )

        window.geometry(
            "550x650"
        )


        frame = tk.Frame(
            window,
            padx=25,
            pady=20
        )

        frame.pack(
            fill="both",
            expand=True
        )


        tk.Label(
            frame,
            text="Edit Job",
            font=("Arial", 18, "bold")
        ).pack(
            pady=(0, 20)
        )


        tk.Label(
            frame,
            text="Job Title"
        ).pack(
            anchor="w"
        )


        title_entry = tk.Entry(frame)

        title_entry.insert(
            0,
            existing[0]
        )

        title_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Required Skills"
        ).pack(
            anchor="w"
        )


        skills_entry = tk.Entry(frame)

        skills_entry.insert(
            0,
            existing[1]
        )

        skills_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Experience"
        ).pack(
            anchor="w"
        )


        experience_entry = tk.Entry(frame)

        experience_entry.insert(
            0,
            existing[2]
        )

        experience_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Qualification"
        ).pack(
            anchor="w"
        )


        qualification_entry = tk.Entry(frame)

        qualification_entry.insert(
            0,
            existing[3] or ""
        )

        qualification_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Job Description"
        ).pack(
            anchor="w"
        )


        description_entry = tk.Text(
            frame,
            height=7
        )

        description_entry.insert(
            "1.0",
            existing[4] or ""
        )

        description_entry.pack(
            fill="both",
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Status"
        ).pack(
            anchor="w"
        )


        status_combo = ttk.Combobox(
            frame,
            values=[
                "Open",
                "Closed",
                "On Hold"
            ],
            state="readonly"
        )

        status_combo.set(
            existing[5] or "Open"
        )

        status_combo.pack(
            fill="x",
            pady=(5, 20)
        )


        def update_job():

            title = (
                title_entry
                .get()
                .strip()
            )

            skills = (
                skills_entry
                .get()
                .strip()
            )

            qualification = (
                qualification_entry
                .get()
                .strip()
            )

            description = (
                description_entry
                .get(
                    "1.0",
                    "end"
                )
                .strip()
            )

            status = status_combo.get()


            try:

                experience = int(
                    experience_entry
                    .get()
                    .strip()
                    or 0
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Experience",
                    "Experience must be a number.",
                    parent=window
                )

                return


            if not title or not skills:

                messagebox.showwarning(
                    "Missing Information",
                    "Job title and skills are required.",
                    parent=window
                )

                return


            success = execute_query(
                """
                UPDATE jobs
                SET
                    job_title = %s,
                    required_skills = %s,
                    experience = %s,
                    qualification = %s,
                    job_description = %s,
                    status = %s
                WHERE job_id = %s
                """,
                (
                    title,
                    skills,
                    experience,
                    qualification,
                    description,
                    status,
                    job_id
                )
            )


            if success:

                messagebox.showinfo(
                    "Success",
                    "Job updated successfully.",
                    parent=window
                )

                window.destroy()

                self.load_jobs()

            else:

                messagebox.showerror(
                    "Error",
                    "Unable to update job.",
                    parent=window
                )


        ttk.Button(
            frame,
            text="Update Job",
            command=update_job
        ).pack(
            fill="x"
        )


    # ========================================================
    # DELETE JOB
    # ========================================================

    def delete_selected_job(self):

        selected = self.job_tree.selection()


        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a job."
            )

            return


        values = self.job_tree.item(
            selected[0],
            "values"
        )


        job_id = values[0]

        job_title = values[1]


        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete job '{job_title}'?"
        )


        if not confirm:

            return


        success = execute_query(
            """
            DELETE FROM jobs
            WHERE job_id = %s
            """,
            (job_id,)
        )


        if success:

            messagebox.showinfo(
                "Deleted",
                "Job deleted successfully."
            )

            self.load_jobs()

        else:

            messagebox.showerror(
                "Error",
                "Unable to delete job."
            )


    # ========================================================
    # CANDIDATE MANAGEMENT
    # ========================================================

    def show_candidates(self):

        self.clear_window()


        header = tk.Frame(
            self.root
        )

        header.pack(
            fill="x",
            padx=20,
            pady=15
        )


        tk.Label(
            header,
            text="Candidate Management",
            font=("Arial", 20, "bold")
        ).pack(
            side="left"
        )


        ttk.Button(
            header,
            text="Back to Dashboard",
            command=self.show_dashboard
        ).pack(
            side="right"
        )


        buttons = tk.Frame(
            self.root
        )

        buttons.pack(
            fill="x",
            padx=20
        )


        ttk.Button(
            buttons,
            text="Add Candidate",
            command=self.add_candidate_window
        ).pack(
            side="left",
            padx=4
        )


        ttk.Button(
            buttons,
            text="Edit Selected",
            command=self.edit_selected_candidate
        ).pack(
            side="left",
            padx=4
        )


        ttk.Button(
            buttons,
            text="Delete Selected",
            command=self.delete_selected_candidate
        ).pack(
            side="left",
            padx=4
        )


        ttk.Button(
            buttons,
            text="AI Screen Resume",
            command=self.ai_screen_selected_candidate
        ).pack(
            side="left",
            padx=4
        )


        ttk.Button(
            buttons,
            text="View Resume",
            command=self.view_selected_resume
        ).pack(
            side="left",
            padx=4
        )


        ttk.Button(
            buttons,
            text="Refresh",
            command=self.load_candidates
        ).pack(
            side="left",
            padx=4
        )


        search_frame = tk.Frame(
            self.root
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )


        tk.Label(
            search_frame,
            text="Search:"
        ).pack(
            side="left"
        )


        self.candidate_search = tk.Entry(
            search_frame,
            width=40
        )

        self.candidate_search.pack(
            side="left",
            padx=10
        )


        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_candidates
        ).pack(
            side="left"
        )


        table_frame = tk.Frame(
            self.root
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )


        columns = (
            "ID",
            "Name",
            "Email",
            "Phone",
            "Qualification",
            "Skills",
            "Experience",
            "AI Score",
            "Status"
        )


        self.candidate_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )


        widths = {

            "ID": 50,

            "Name": 140,

            "Email": 180,

            "Phone": 110,

            "Qualification": 150,

            "Skills": 220,

            "Experience": 90,

            "AI Score": 90,

            "Status": 120
        }


        for column in columns:

            self.candidate_tree.heading(
                column,
                text=column
            )

            self.candidate_tree.column(
                column,
                width=widths[column]
            )


        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.candidate_tree.yview
        )


        self.candidate_tree.configure(
            yscrollcommand=scrollbar.set
        )


        self.candidate_tree.pack(
            side="left",
            fill="both",
            expand=True
        )


        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.load_candidates()


    # ========================================================
    # LOAD CANDIDATES
    # ========================================================

    def load_candidates(self, search=""):

        for item in self.candidate_tree.get_children():

            self.candidate_tree.delete(item)


        if search:

            value = f"%{search}%"


            rows = fetch_all(
                """
                SELECT
                    candidate_id,
                    name,
                    email,
                    phone,
                    qualification,
                    skills,
                    experience,
                    ai_score,
                    status
                FROM candidates
                WHERE name LIKE %s
                OR email LIKE %s
                OR skills LIKE %s
                OR qualification LIKE %s
                ORDER BY ai_score DESC, candidate_id
                """,
                (
                    value,
                    value,
                    value,
                    value
                )
            )

        else:

            rows = fetch_all(
                """
                SELECT
                    candidate_id,
                    name,
                    email,
                    phone,
                    qualification,
                    skills,
                    experience,
                    ai_score,
                    status
                FROM candidates
                ORDER BY ai_score DESC, candidate_id
                """
            )


        for row in rows:

            self.candidate_tree.insert(
                "",
                "end",
                values=row
            )


    # ========================================================
    # SEARCH CANDIDATES
    # ========================================================

    def search_candidates(self):

        search = (
            self.candidate_search
            .get()
            .strip()
        )

        self.load_candidates(
            search
        )


    # ========================================================
    # ADD CANDIDATE
    # ========================================================

    def add_candidate_window(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Add Candidate"
        )

        window.geometry(
            "600x750"
        )


        frame = tk.Frame(
            window,
            padx=25,
            pady=20
        )

        frame.pack(
            fill="both",
            expand=True
        )


        tk.Label(
            frame,
            text="Add Candidate",
            font=("Arial", 18, "bold")
        ).pack(
            pady=(0, 20)
        )


        fields = {}


        for label in [

            "Candidate Name",
            "Email",
            "Phone",
            "Qualification",
            "Skills",
            "Experience (Years)"

        ]:

            tk.Label(
                frame,
                text=label
            ).pack(
                anchor="w"
            )


            entry = tk.Entry(
                frame
            )

            entry.pack(
                fill="x",
                pady=(5, 12)
            )


            fields[label] = entry


        resume_frame = tk.Frame(
            frame
        )

        resume_frame.pack(
            fill="x",
            pady=10
        )


        resume_path_var = tk.StringVar()


        tk.Label(
            frame,
            text="Resume"
        ).pack(
            anchor="w"
        )


        tk.Entry(
            frame,
            textvariable=resume_path_var,
            state="readonly"
        ).pack(
            fill="x",
            pady=(5, 5)
        )


        def upload_resume():

            path = filedialog.askopenfilename(
                title="Select Resume",
                filetypes=[
                    (
                        "Resume Files",
                        "*.pdf *.docx"
                    ),
                    (
                        "PDF Files",
                        "*.pdf"
                    ),
                    (
                        "Word Files",
                        "*.docx"
                    )
                ]
            )


            if not path:

                return


            resume_path_var.set(
                path
            )


            resume_text = read_resume(
                path
            )


            if resume_text:

                email = extract_email(
                    resume_text
                )

                phone = extract_phone(
                    resume_text
                )

                skills = extract_skills(
                    resume_text
                )

                experience = extract_experience(
                    resume_text
                )


                if email:

                    fields["Email"].delete(
                        0,
                        "end"
                    )

                    fields["Email"].insert(
                        0,
                        email
                    )


                if phone:

                    fields["Phone"].delete(
                        0,
                        "end"
                    )

                    fields["Phone"].insert(
                        0,
                        phone
                    )


                if skills:

                    fields["Skills"].delete(
                        0,
                        "end"
                    )

                    fields["Skills"].insert(
                        0,
                        skills
                    )


                if experience:

                    fields["Experience (Years)"].delete(
                        0,
                        "end"
                    )

                    fields["Experience (Years)"].insert(
                        0,
                        experience
                    )


                messagebox.showinfo(
                    "Resume Read",
                    "Resume uploaded and information extracted.",
                    parent=window
                )

            else:

                messagebox.showwarning(
                    "Resume Error",
                    "Could not extract text from the selected resume.",
                    parent=window
                )


        ttk.Button(
            frame,
            text="Upload Resume",
            command=upload_resume
        ).pack(
            fill="x",
            pady=5
        )


        def save_candidate():

            name = (
                fields["Candidate Name"]
                .get()
                .strip()
            )

            email = (
                fields["Email"]
                .get()
                .strip()
            )

            phone = (
                fields["Phone"]
                .get()
                .strip()
            )

            qualification = (
                fields["Qualification"]
                .get()
                .strip()
            )

            skills = (
                fields["Skills"]
                .get()
                .strip()
            )

            experience = (
                fields["Experience (Years)"]
                .get()
                .strip()
            )

            resume_path = (
                resume_path_var
                .get()
                .strip()
            )


            if not name:

                messagebox.showwarning(
                    "Missing Information",
                    "Candidate name is required.",
                    parent=window
                )

                return


            try:

                experience_value = int(
                    experience
                    if experience
                    else 0
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Experience",
                    "Experience must be a number.",
                    parent=window
                )

                return


            success = execute_query(
                """
                INSERT INTO candidates
                (
                    name,
                    email,
                    phone,
                    qualification,
                    skills,
                    experience,
                    resume_path
                )
                VALUES
                (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    name,
                    email,
                    phone,
                    qualification,
                    skills,
                    experience_value,
                    resume_path
                )
            )


            if success:

                messagebox.showinfo(
                    "Success",
                    "Candidate added successfully.",
                    parent=window
                )

                window.destroy()

                self.load_candidates()

            else:

                messagebox.showerror(
                    "Error",
                    "Unable to add candidate.",
                    parent=window
                )


        ttk.Button(
            frame,
            text="Save Candidate",
            command=save_candidate
        ).pack(
            fill="x",
            pady=10
        )


    # ========================================================
    # EDIT CANDIDATE
    # ========================================================

    def edit_selected_candidate(self):

        selected = (
            self.candidate_tree
            .selection()
        )


        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a candidate."
            )

            return


        values = self.candidate_tree.item(
            selected[0],
            "values"
        )


        candidate_id = values[0]


        candidate = fetch_one(
            """
            SELECT
                name,
                email,
                phone,
                qualification,
                skills,
                experience,
                status
            FROM candidates
            WHERE candidate_id = %s
            """,
            (candidate_id,)
        )


        if not candidate:

            return


        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Edit Candidate"
        )

        window.geometry(
            "550x650"
        )


        frame = tk.Frame(
            window,
            padx=25,
            pady=20
        )

        frame.pack(
            fill="both",
            expand=True
        )


        entries = {}


        data = [

            ("Name", candidate[0]),

            ("Email", candidate[1] or ""),

            ("Phone", candidate[2] or ""),

            ("Qualification", candidate[3] or ""),

            ("Skills", candidate[4] or ""),

            ("Experience", candidate[5] or 0)
        ]


        for label, value in data:

            tk.Label(
                frame,
                text=label
            ).pack(
                anchor="w"
            )


            entry = tk.Entry(
                frame
            )

            entry.insert(
                0,
                value
            )

            entry.pack(
                fill="x",
                pady=(5, 12)
            )


            entries[label] = entry


        tk.Label(
            frame,
            text="Status"
        ).pack(
            anchor="w"
        )


        status_combo = ttk.Combobox(
            frame,
            values=[
                "Under Review",
                "Shortlisted",
                "Rejected",
                "Selected"
            ],
            state="readonly"
        )


        status_combo.set(
            candidate[6] or "Under Review"
        )


        status_combo.pack(
            fill="x",
            pady=(5, 20)
        )


        def update_candidate():

            try:

                experience = int(
                    entries["Experience"]
                    .get()
                    .strip()
                    or 0
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Experience",
                    "Experience must be a number.",
                    parent=window
                )

                return


            success = execute_query(
                """
                UPDATE candidates
                SET
                    name = %s,
                    email = %s,
                    phone = %s,
                    qualification = %s,
                    skills = %s,
                    experience = %s,
                    status = %s
                WHERE candidate_id = %s
                """,
                (
                    entries["Name"].get().strip(),
                    entries["Email"].get().strip(),
                    entries["Phone"].get().strip(),
                    entries["Qualification"].get().strip(),
                    entries["Skills"].get().strip(),
                    experience,
                    status_combo.get(),
                    candidate_id
                )
            )


            if success:

                messagebox.showinfo(
                    "Success",
                    "Candidate updated successfully.",
                    parent=window
                )

                window.destroy()

                self.load_candidates()

            else:

                messagebox.showerror(
                    "Error",
                    "Unable to update candidate.",
                    parent=window
                )


        ttk.Button(
            frame,
            text="Update Candidate",
            command=update_candidate
        ).pack(
            fill="x"
        )


    # ========================================================
    # DELETE CANDIDATE
    # ========================================================

    def delete_selected_candidate(self):

        selected = (
            self.candidate_tree
            .selection()
        )


        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a candidate."
            )

            return


        values = self.candidate_tree.item(
            selected[0],
            "values"
        )


        candidate_id = values[0]

        candidate_name = values[1]


        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete candidate '{candidate_name}'?"
        )


        if not confirm:

            return


        success = execute_query(
            """
            DELETE FROM candidates
            WHERE candidate_id = %s
            """,
            (candidate_id,)
        )


        if success:

            messagebox.showinfo(
                "Deleted",
                "Candidate deleted successfully."
            )

            self.load_candidates()

        else:

            messagebox.showerror(
                "Error",
                "Unable to delete candidate."
            )


    # ========================================================
    # AI SCREEN SELECTED CANDIDATE
    # ========================================================

    def ai_screen_selected_candidate(self):

        selected = (
            self.candidate_tree
            .selection()
        )


        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a candidate."
            )

            return


        values = self.candidate_tree.item(
            selected[0],
            "values"
        )


        candidate_id = values[0]


        candidate = fetch_one(
            """
            SELECT
                candidate_id,
                name,
                resume_path
            FROM candidates
            WHERE candidate_id = %s
            """,
            (candidate_id,)
        )


        if not candidate:

            messagebox.showerror(
                "Error",
                "Candidate not found."
            )

            return


        self.screen_candidate_window(
            candidate
        )


    # ========================================================
    # AI SCREEN WINDOW
    # ========================================================

    def screen_candidate_window(
        self,
        candidate
    ):

        candidate_id = candidate[0]

        candidate_name = candidate[1]

        resume_path = candidate[2]


        window = tk.Toplevel(
            self.root
        )

        window.title(
            "AI Resume Screening"
        )

        window.geometry(
            "700x650"
        )


        frame = tk.Frame(
            window,
            padx=25,
            pady=20
        )

        frame.pack(
            fill="both",
            expand=True
        )


        tk.Label(
            frame,
            text="AI RESUME SCREENING",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(0, 10)
        )


        tk.Label(
            frame,
            text=f"Candidate: {candidate_name}",
            font=("Arial", 12)
        ).pack(
            pady=(0, 20)
        )


        tk.Label(
            frame,
            text="Select Job"
        ).pack(
            anchor="w"
        )


        jobs = fetch_all(
            """
            SELECT
                job_id,
                job_title
            FROM jobs
            WHERE status = 'Open'
            ORDER BY job_title
            """
        )


        if not jobs:

            messagebox.showwarning(
                "No Jobs",
                "Please create an open job first.",
                parent=window
            )

            window.destroy()

            return


        job_map = {}

        job_values = []


        for job in jobs:

            display = f"{job[0]} - {job[1]}"

            job_values.append(
                display
            )

            job_map[display] = job[0]


        job_combo = ttk.Combobox(
            frame,
            values=job_values,
            state="readonly"
        )

        job_combo.pack(
            fill="x",
            pady=(5, 20)
        )


        job_combo.current(0)


        result_frame = tk.Frame(
            frame
        )

        result_frame.pack(
            fill="both",
            expand=True,
            pady=10
        )


        result_text = tk.Text(
            result_frame,
            height=20,
            wrap="word"
        )

        result_text.pack(
            fill="both",
            expand=True
        )


        def run_screening():

            selected_job = job_combo.get()


            if not selected_job:

                return


            job_id = job_map[
                selected_job
            ]


            job = fetch_one(
                """
                SELECT
                    job_title,
                    required_skills,
                    experience,
                    qualification,
                    job_description
                FROM jobs
                WHERE job_id = %s
                """,
                (job_id,)
            )


            if not job:

                messagebox.showerror(
                    "Error",
                    "Unable to load job.",
                    parent=window
                )

                return


            if not resume_path:

                messagebox.showwarning(
                    "No Resume",
                    "This candidate does not have a resume uploaded.",
                    parent=window
                )

                return


            resume_text = read_resume(
                resume_path
            )


            if not resume_text:

                messagebox.showerror(
                    "Resume Error",
                    "Unable to extract text from resume.",
                    parent=window
                )

                return


            score = calculate_score(
                job[4] or job[1],
                job[1],
                resume_text
            )


            status = get_status(
                score
            )


            recommendation = get_recommendation(
                score
            )


            matched = get_matched_skills(
                job[1],
                resume_text
            )


            missing = get_missing_skills(
                job[1],
                resume_text
            )


            success = execute_query(
                """
                UPDATE candidates
                SET
                    ai_score = %s,
                    status = %s
                WHERE candidate_id = %s
                """,
                (
                    score,
                    status,
                    candidate_id
                )
            )


            if not success:

                messagebox.showerror(
                    "Database Error",
                    "Unable to save AI score.",
                    parent=window
                )

                return


            result_text.delete(
                "1.0",
                "end"
            )


            result_text.insert(
                "end",
                "AI RESUME SCREENING RESULT\n"
            )

            result_text.insert(
                "end",
                "=" * 45
                + "\n\n"
            )


            result_text.insert(
                "end",
                f"Candidate: {candidate_name}\n"
            )

            result_text.insert(
                "end",
                f"Job: {job[0]}\n\n"
            )


            result_text.insert(
                "end",
                f"AI MATCH SCORE: {score:.2f}%\n\n"
            )


            result_text.insert(
                "end",
                f"STATUS: {status}\n\n"
            )


            result_text.insert(
                "end",
                f"RECOMMENDATION: {recommendation}\n\n"
            )


            result_text.insert(
                "end",
                "MATCHED SKILLS:\n"
            )


            if matched:

                result_text.insert(
                    "end",
                    ", ".join(matched)
                    + "\n\n"
                )

            else:

                result_text.insert(
                    "end",
                    "No required skills matched.\n\n"
                )


            result_text.insert(
                "end",
                "MISSING SKILLS:\n"
            )


            if missing:

                result_text.insert(
                    "end",
                    ", ".join(missing)
                    + "\n\n"
                )

            else:

                result_text.insert(
                    "end",
                    "No major missing skills detected.\n\n"
                )


            result_text.insert(
                "end",
                "SCREENING RULES:\n"
                "80% and above → Shortlisted\n"
                "60%–79% → Under Review\n"
                "Below 60% → Rejected\n"
            )


            self.load_candidates()


            messagebox.showinfo(
                "AI Screening Complete",
                f"Resume scored {score:.2f}%\n\nStatus: {status}",
                parent=window
            )


        ttk.Button(
            frame,
            text="RUN AI SCREENING",
            command=run_screening
        ).pack(
            fill="x",
            pady=10
        )


    # ========================================================
    # VIEW RESUME
    # ========================================================

    def view_selected_resume(self):

        selected = (
            self.candidate_tree
            .selection()
        )


        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a candidate."
            )

            return


        values = self.candidate_tree.item(
            selected[0],
            "values"
        )


        candidate_id = values[0]


        candidate = fetch_one(
            """
            SELECT
                name,
                resume_path
            FROM candidates
            WHERE candidate_id = %s
            """,
            (candidate_id,)
        )


        if not candidate:

            return


        path = candidate[1]


        if not path:

            messagebox.showinfo(
                "No Resume",
                "No resume has been uploaded for this candidate."
            )

            return


        if not os.path.exists(path):

            messagebox.showerror(
                "File Not Found",
                "The resume file could not be found."
            )

            return


        try:

            if sys.platform.startswith(
                "win"
            ):

                os.startfile(path)

            elif sys.platform == "darwin":

                subprocess.call(
                    ["open", path]
                )

            else:

                subprocess.call(
                    ["xdg-open", path]
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to open resume.\n\n{e}"
            )


    # ========================================================
    # INTERVIEW MANAGEMENT
    # ========================================================

    def show_interviews(self):

        self.clear_window()


        header = tk.Frame(
            self.root
        )

        header.pack(
            fill="x",
            padx=20,
            pady=15
        )


        tk.Label(
            header,
            text="Interview Management",
            font=("Arial", 20, "bold")
        ).pack(
            side="left"
        )


        ttk.Button(
            header,
            text="Back to Dashboard",
            command=self.show_dashboard
        ).pack(
            side="right"
        )


        buttons = tk.Frame(
            self.root
        )

        buttons.pack(
            fill="x",
            padx=20
        )


        ttk.Button(
            buttons,
            text="Schedule Interview",
            command=self.schedule_interview
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            buttons,
            text="Update Status",
            command=self.update_interview_status
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            buttons,
            text="Delete Interview",
            command=self.delete_interview
        ).pack(
            side="left",
            padx=5
        )


        ttk.Button(
            buttons,
            text="Refresh",
            command=self.load_interviews
        ).pack(
            side="left",
            padx=5
        )


        table_frame = tk.Frame(
            self.root
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )


        columns = (

            "ID",

            "Candidate",

            "Date",

            "Time",

            "Interviewer",

            "Status",

            "Notes"
        )


        self.interview_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )


        widths = {

            "ID": 60,

            "Candidate": 180,

            "Date": 110,

            "Time": 100,

            "Interviewer": 170,

            "Status": 120,

            "Notes": 250
        }


        for column in columns:

            self.interview_tree.heading(
                column,
                text=column
            )

            self.interview_tree.column(
                column,
                width=widths[column]
            )


        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.interview_tree.yview
        )


        self.interview_tree.configure(
            yscrollcommand=scrollbar.set
        )


        self.interview_tree.pack(
            side="left",
            fill="both",
            expand=True
        )


        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.load_interviews()


    # ========================================================
    # LOAD INTERVIEWS
    # ========================================================

    def load_interviews(self):

        for item in self.interview_tree.get_children():

            self.interview_tree.delete(item)


        rows = fetch_all(
            """
            SELECT
                i.interview_id,
                c.name,
                i.interview_date,
                i.interview_time,
                i.interviewer,
                i.status,
                i.notes
            FROM interviews i
            JOIN candidates c
            ON i.candidate_id = c.candidate_id
            ORDER BY
                i.interview_date,
                i.interview_time
            """
        )


        for row in rows:

            self.interview_tree.insert(
                "",
                "end",
                values=row
            )


    # ========================================================
    # SCHEDULE INTERVIEW
    # ========================================================

    def schedule_interview(self):

        candidates = fetch_all(
            """
            SELECT
                candidate_id,
                name
            FROM candidates
            WHERE status IN
            ('Shortlisted', 'Selected')
            ORDER BY name
            """
        )


        if not candidates:

            messagebox.showinfo(
                "No Candidates",
                "There are no shortlisted or selected candidates."
            )

            return


        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Schedule Interview"
        )

        window.geometry(
            "500x550"
        )


        frame = tk.Frame(
            window,
            padx=25,
            pady=20
        )

        frame.pack(
            fill="both",
            expand=True
        )


        tk.Label(
            frame,
            text="Schedule Interview",
            font=("Arial", 18, "bold")
        ).pack(
            pady=(0, 20)
        )


        tk.Label(
            frame,
            text="Candidate"
        ).pack(
            anchor="w"
        )


        candidate_map = {}

        candidate_values = []


        for candidate in candidates:

            display = (
                f"{candidate[0]} - "
                f"{candidate[1]}"
            )

            candidate_values.append(
                display
            )

            candidate_map[
                display
            ] = candidate[0]


        candidate_combo = ttk.Combobox(
            frame,
            values=candidate_values,
            state="readonly"
        )

        candidate_combo.pack(
            fill="x",
            pady=(5, 15)
        )


        candidate_combo.current(0)


        tk.Label(
            frame,
            text="Interview Date (YYYY-MM-DD)"
        ).pack(
            anchor="w"
        )


        date_entry = tk.Entry(
            frame
        )

        date_entry.insert(
            0,
            datetime.now().strftime(
                "%Y-%m-%d"
            )
        )

        date_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Interview Time (HH:MM)"
        ).pack(
            anchor="w"
        )


        time_entry = tk.Entry(
            frame
        )

        time_entry.insert(
            0,
            "10:00"
        )

        time_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Interviewer"
        ).pack(
            anchor="w"
        )


        interviewer_entry = tk.Entry(
            frame
        )

        interviewer_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        tk.Label(
            frame,
            text="Notes"
        ).pack(
            anchor="w"
        )


        notes_entry = tk.Text(
            frame,
            height=6
        )

        notes_entry.pack(
            fill="both",
            pady=(5, 15)
        )


        def save_interview():

            candidate_selection = (
                candidate_combo.get()
            )


            if not candidate_selection:

                return


            candidate_id = candidate_map[
                candidate_selection
            ]


            date_value = (
                date_entry
                .get()
                .strip()
            )

            time_value = (
                time_entry
                .get()
                .strip()
            )

            interviewer = (
                interviewer_entry
                .get()
                .strip()
            )

            notes = (
                notes_entry
                .get(
                    "1.0",
                    "end"
                )
                .strip()
            )


            if not date_value or not time_value:

                messagebox.showwarning(
                    "Missing Information",
                    "Date and time are required.",
                    parent=window
                )

                return


            try:

                datetime.strptime(
                    date_value,
                    "%Y-%m-%d"
                )

                datetime.strptime(
                    time_value,
                    "%H:%M"
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Date/Time",
                    "Use date YYYY-MM-DD and time HH:MM.",
                    parent=window
                )

                return


            success = execute_query(
                """
                INSERT INTO interviews
                (
                    candidate_id,
                    interview_date,
                    interview_time,
                    interviewer,
                    status,
                    notes
                )
                VALUES
                (%s, %s, %s, %s, %s, %s)
                """,
                (
                    candidate_id,
                    date_value,
                    time_value,
                    interviewer,
                    "Scheduled",
                    notes
                )
            )


            if success:

                messagebox.showinfo(
                    "Success",
                    "Interview scheduled successfully.",
                    parent=window
                )

                window.destroy()

                self.load_interviews()

            else:

                messagebox.showerror(
                    "Error",
                    "Unable to schedule interview.",
                    parent=window
                )


        ttk.Button(
            frame,
            text="Schedule Interview",
            command=save_interview
        ).pack(
            fill="x"
        )


    # ========================================================
    # UPDATE INTERVIEW STATUS
    # ========================================================

    def update_interview_status(self):

        selected = (
            self.interview_tree
            .selection()
        )


        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an interview."
            )

            return


        values = self.interview_tree.item(
            selected[0],
            "values"
        )


        interview_id = values[0]


        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Update Interview"
        )

        window.geometry(
            "400x250"
        )


        frame = tk.Frame(
            window,
            padx=25,
            pady=25
        )

        frame.pack(
            fill="both",
            expand=True
        )


        tk.Label(
            frame,
            text="Interview Status",
            font=("Arial", 12, "bold")
        ).pack(
            pady=10
        )


        combo = ttk.Combobox(
            frame,
            values=[
                "Scheduled",
                "Completed",
                "Cancelled",
                "Rescheduled",
                "No Show"
            ],
            state="readonly"
        )

        combo.set(
            values[5]
        )

        combo.pack(
            fill="x",
            pady=10
        )


        def update():

            success = execute_query(
                """
                UPDATE interviews
                SET status = %s
                WHERE interview_id = %s
                """,
                (
                    combo.get(),
                    interview_id
                )
            )


            if success:

                messagebox.showinfo(
                    "Updated",
                    "Interview status updated.",
                    parent=window
                )

                window.destroy()

                self.load_interviews()

            else:

                messagebox.showerror(
                    "Error",
                    "Unable to update interview.",
                    parent=window
                )


        ttk.Button(
            frame,
            text="Update",
            command=update
        ).pack(
            fill="x"
        )


    # ========================================================
    # DELETE INTERVIEW
    # ========================================================

    def delete_interview(self):

        selected = (
            self.interview_tree
            .selection()
        )


        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an interview."
            )

            return


        values = self.interview_tree.item(
            selected[0],
            "values"
        )


        interview_id = values[0]


        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this interview?"
        )


        if not confirm:

            return


        success = execute_query(
            """
            DELETE FROM interviews
            WHERE interview_id = %s
            """,
            (interview_id,)
        )


        if success:

            messagebox.showinfo(
                "Deleted",
                "Interview deleted successfully."
            )

            self.load_interviews()

        else:

            messagebox.showerror(
                "Error",
                "Unable to delete interview."
            )


    # ========================================================
    # REPORTS
    # ========================================================

    def show_reports(self):

        self.clear_window()


        header = tk.Frame(
            self.root
        )

        header.pack(
            fill="x",
            padx=20,
            pady=15
        )


        tk.Label(
            header,
            text="Recruitment Reports",
            font=("Arial", 20, "bold")
        ).pack(
            side="left"
        )


        ttk.Button(
            header,
            text="Back to Dashboard",
            command=self.show_dashboard
        ).pack(
            side="right"
        )


        content = tk.Frame(
            self.root,
            padx=30,
            pady=30
        )

        content.pack(
            fill="both",
            expand=True
        )


        total = fetch_one(
            "SELECT COUNT(*) FROM candidates"
        )


        shortlisted = fetch_one(
            """
            SELECT COUNT(*)
            FROM candidates
            WHERE status = 'Shortlisted'
            """
        )


        rejected = fetch_one(
            """
            SELECT COUNT(*)
            FROM candidates
            WHERE status = 'Rejected'
            """
        )


        under_review = fetch_one(
            """
            SELECT COUNT(*)
            FROM candidates
            WHERE status = 'Under Review'
            """
        )


        average = fetch_one(
            """
            SELECT AVG(ai_score)
            FROM candidates
            WHERE ai_score > 0
            """
        )


        total_jobs = fetch_one(
            "SELECT COUNT(*) FROM jobs"
        )


        total_interviews = fetch_one(
            "SELECT COUNT(*) FROM interviews"
        )


        total_value = (
            total[0]
            if total
            else 0
        )


        shortlisted_value = (
            shortlisted[0]
            if shortlisted
            else 0
        )


        rejected_value = (
            rejected[0]
            if rejected
            else 0
        )


        under_review_value = (
            under_review[0]
            if under_review
            else 0
        )


        average_value = (
            float(average[0])
            if average and average[0]
            else 0
        )


        jobs_value = (
            total_jobs[0]
            if total_jobs
            else 0
        )


        interviews_value = (
            total_interviews[0]
            if total_interviews
            else 0
        )


        report_text = f"""
RECRUITMENT REPORT
==============================

Total Job Openings       : {jobs_value}

Total Applicants         : {total_value}

Shortlisted Candidates   : {shortlisted_value}

Under Review             : {under_review_value}

Rejected Candidates      : {rejected_value}

Average AI Score         : {average_value:.2f}%

Total Interviews        : {interviews_value}

==============================

SELECTION RATIO
"""


        if total_value > 0:

            ratio = (
                shortlisted_value
                /
                total_value
            ) * 100

        else:

            ratio = 0


        report_text += (
            f"\nShortlisting Ratio     : "
            f"{ratio:.2f}%\n"
        )


        text = tk.Text(
            content,
            font=("Courier New", 12)
        )

        text.pack(
            fill="both",
            expand=True
        )


        text.insert(
            "1.0",
            report_text
        )


        text.configure(
            state="disabled"
        )


        ttk.Button(
            content,
            text="Export Candidate Report to Excel",
            command=self.export_candidates_excel
        ).pack(
            fill="x",
            pady=15
        )


        ttk.Button(
            content,
            text="Export Interview Report to Excel",
            command=self.export_interviews_excel
        ).pack(
            fill="x"
        )


    # ========================================================
    # EXPORT CANDIDATES TO EXCEL
    # ========================================================

    def export_candidates_excel(self):

        rows = fetch_all(
            """
            SELECT
                candidate_id AS ID,
                name AS Name,
                email AS Email,
                phone AS Phone,
                qualification AS Qualification,
                skills AS Skills,
                experience AS Experience,
                ai_score AS AI_Score,
                status AS Status
            FROM candidates
            ORDER BY ai_score DESC
            """
        )


        if not rows:

            messagebox.showinfo(
                "No Data",
                "There are no candidates to export."
            )

            return


        columns = [

            "ID",

            "Name",

            "Email",

            "Phone",

            "Qualification",

            "Skills",

            "Experience",

            "AI Score",

            "Status"
        ]


        data = pd.DataFrame(
            rows,
            columns=columns
        )


        path = filedialog.asksaveasfilename(
            title="Save Candidate Report",
            defaultextension=".xlsx",
            filetypes=[
                (
                    "Excel Files",
                    "*.xlsx"
                )
            ]
        )


        if not path:

            return


        try:

            data.to_excel(
                path,
                index=False
            )


            messagebox.showinfo(
                "Export Successful",
                f"Candidate report saved to:\n{path}"
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )


    # ========================================================
    # EXPORT INTERVIEWS TO EXCEL
    # ========================================================

    def export_interviews_excel(self):

        rows = fetch_all(
            """
            SELECT
                i.interview_id AS ID,
                c.name AS Candidate,
                i.interview_date AS Date,
                i.interview_time AS Time,
                i.interviewer AS Interviewer,
                i.status AS Status,
                i.notes AS Notes
            FROM interviews i
            JOIN candidates c
            ON i.candidate_id = c.candidate_id
            ORDER BY i.interview_date
            """
        )


        if not rows:

            messagebox.showinfo(
                "No Data",
                "There are no interviews to export."
            )

            return


        columns = [

            "ID",

            "Candidate",

            "Date",

            "Time",

            "Interviewer",

            "Status",

            "Notes"
        ]


        data = pd.DataFrame(
            rows,
            columns=columns
        )


        path = filedialog.asksaveasfilename(
            title="Save Interview Report",
            defaultextension=".xlsx",
            filetypes=[
                (
                    "Excel Files",
                    "*.xlsx"
                )
            ]
        )


        if not path:

            return


        try:

            data.to_excel(
                path,
                index=False
            )


            messagebox.showinfo(
                "Export Successful",
                f"Interview report saved to:\n{path}"
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )


    # ========================================================
    # ANALYTICS
    # ========================================================

    def show_analytics(self):

        self.clear_window()


        header = tk.Frame(
            self.root
        )

        header.pack(
            fill="x",
            padx=20,
            pady=15
        )


        tk.Label(
            header,
            text="Recruitment Analytics",
            font=("Arial", 20, "bold")
        ).pack(
            side="left"
        )


        ttk.Button(
            header,
            text="Back to Dashboard",
            command=self.show_dashboard
        ).pack(
            side="right"
        )


        content = tk.Frame(
            self.root,
            padx=25,
            pady=25
        )

        content.pack(
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # STATUS DISTRIBUTION
        # ----------------------------------------------------

        statuses = fetch_all(
            """
            SELECT
                status,
                COUNT(*)
            FROM candidates
            GROUP BY status
            ORDER BY COUNT(*) DESC
            """
        )


        # ----------------------------------------------------
        # EXPERIENCE DISTRIBUTION
        # ----------------------------------------------------

        experiences = fetch_all(
            """
            SELECT
                experience,
                COUNT(*)
            FROM candidates
            GROUP BY experience
            ORDER BY experience
            """
        )


        # ----------------------------------------------------
        # SKILL DISTRIBUTION
        # ----------------------------------------------------

        candidates = fetch_all(
            """
            SELECT skills
            FROM candidates
            WHERE skills IS NOT NULL
            AND skills <> ''
            """
        )


        skill_count = {}


        for candidate in candidates:

            skills = candidate[0]

            if not skills:

                continue


            for skill in skills.split(","):

                skill = skill.strip()

                if not skill:

                    continue


                skill_lower = skill.lower()


                if skill_lower not in skill_count:

                    skill_count[
                        skill_lower
                    ] = 0


                skill_count[
                    skill_lower
                ] += 1


        sorted_skills = sorted(
            skill_count.items(),
            key=lambda x: x[1],
            reverse=True
        )


        total_candidates = sum(
            row[1]
            for row in statuses
        )


        text = tk.Text(
            content,
            font=("Courier New", 11)
        )

        text.pack(
            fill="both",
            expand=True
        )


        analytics_text = (
            "RECRUITMENT ANALYTICS\n"
            "============================================\n\n"
        )


        analytics_text += (
            f"TOTAL CANDIDATES: "
            f"{total_candidates}\n\n"
        )


        analytics_text += (
            "CANDIDATE STATUS DISTRIBUTION\n"
            "--------------------------------------------\n"
        )


        for status, count in statuses:

            percentage = (
                count / total_candidates * 100
                if total_candidates
                else 0
            )


            analytics_text += (
                f"{status:<20}"
                f"{count:>5} "
                f"({percentage:.2f}%)\n"
            )


        analytics_text += (
            "\n\n"
            "EXPERIENCE DISTRIBUTION\n"
            "--------------------------------------------\n"
        )


        for experience, count in experiences:

            analytics_text += (
                f"{experience} years"
                f"{' ':<10}"
                f"{count} candidate(s)\n"
            )


        analytics_text += (
            "\n\n"
            "TOP SKILLS\n"
            "--------------------------------------------\n"
        )


        if sorted_skills:

            for skill, count in sorted_skills[:15]:

                analytics_text += (
                    f"{skill.title():<25}"
                    f"{count} candidate(s)\n"
                )

        else:

            analytics_text += (
                "No skill information available.\n"
            )


        text.insert(
            "1.0",
            analytics_text
        )


        text.configure(
            state="disabled"
        )


    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )


        if confirm:

            self.current_user = None

            self.current_role = None

            self.show_login()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = RecruitmentApp(
        root
    )

    root.mainloop()