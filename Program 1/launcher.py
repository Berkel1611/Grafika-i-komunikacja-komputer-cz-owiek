import tkinter as tk
import subprocess
import os
import sys


class Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Program Launcher")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        # Tytuł
        title_label = tk.Label(root, text="Program Launcher", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=20)

        # Ramka na przyciski
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        # Przyciski
        self.create_button(button_frame, "Uruchom program: KrzyweBeziera", self.run_program1, "#4CAF50")
        self.create_button(button_frame, "Uruchom program: PowierzchnieBieziera", self.run_program2, "#2196F3")
        self.create_button(button_frame, "Uruchom grę: Survivor", self.run_python_script, "#FFC107")
        self.create_button(button_frame, "Pokaż README", self.show_readme, "#9C27B0")

        # Pole statusu
        self.status_var = tk.StringVar()
        self.status_var.set("Gotowy...")
        status_label = tk.Label(root, textvariable=self.status_var, bg="#f0f0f0", fg="#666666")
        status_label.pack(side=tk.BOTTOM, pady=10)

        self.program_path = os.getcwd()

    def create_button(self, parent, text, command, color):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            font=("Arial", 10),
            width=30,
            height=2,
            relief=tk.RAISED,
            borderwidth=2
        )
        button.pack(pady=5)
        return button

    def run_program1(self):
        try:
            self.status_var.set("Uruchamianie Programu 1...")
            self.root.update()
            os.chdir("KrzyweBeziera/out/production/KrzyweBeziera")
            subprocess.run(["java", "Initials"])
            os.chdir(self.program_path)
            self.status_var.set("Program 1 uruchomiony")
        except Exception as e:
            self.status_var.set(f"Błąd: {e}")

    def run_program2(self):
        try:
            self.status_var.set("Uruchamianie Programu 2...")
            self.root.update()
            os.chdir("PowierzchniaBeziera/out/production/PowierzchniaBeziera")
            subprocess.run(["java", "Main"])
            os.chdir(self.program_path)
            self.status_var.set("Program 2 uruchomiony")
        except Exception as e:
            self.status_var.set(f"Błąd: {e}")

    def run_python_script(self):
        try:
            self.status_var.set("Uruchamianie skryptu Python...")
            self.root.update()
            subprocess.Popen([sys.executable, "Survivor/main.py"])
            self.status_var.set("Skrypt Python uruchomiony")
        except Exception as e:
            self.status_var.set(f"Błąd: {e}")

    def show_readme(self):
        try:
            readme_path = "README.txt"

            if not os.path.exists(readme_path):
                self.status_var.set(f"Błąd: Plik {readme_path} nie istnieje")
                return

            self.status_var.set("Wyświetlanie pliku README...")

            readme_window = tk.Toplevel(self.root)
            readme_window.title("README.txt")
            readme_window.geometry("600x400")

            text_frame = tk.Frame(readme_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            text_area = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)

            with open(readme_path, "r", encoding="utf-8") as file:
                content = file.read()
                text_area.insert(tk.END, content)

            text_area.config(state=tk.DISABLED)  # Tylko do odczytu
            text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar.config(command=text_area.yview)

            self.status_var.set("Plik README wyświetlony")
        except Exception as e:
            self.status_var.set(f"Błąd: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Launcher(root)
    root.mainloop()
