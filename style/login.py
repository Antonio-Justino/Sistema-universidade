import customtkinter as ctk
from tkinter import messagebox

from database.banco import conectar, criar_tabelas

from dashboard import Dashboard
from aluno_area import TelaAluno
from area_professor import TelaProfessor


class TelaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        criar_tabelas()

        self.title("Login - Sistema Universitário")
        self.geometry("400x350")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(
            self,
            text="Sistema Universitário",
            font=("Arial", 26, "bold")
        ).pack(pady=30)

        self.entry_login = ctk.CTkEntry(
            self,
            placeholder_text="Login"
        )
        self.entry_login.pack(pady=10, padx=40, fill="x")

        self.entry_senha = ctk.CTkEntry(
            self,
            placeholder_text="Senha",
            show="*"
        )
        self.entry_senha.pack(pady=10, padx=40, fill="x")

        ctk.CTkButton(
            self,
            text="Entrar",
            command=self.fazer_login
        ).pack(pady=25)

    def fazer_login(self):
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not login or not senha:
            messagebox.showwarning("Aviso", "Preencha login e senha.")
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nome, tipo
            FROM usuarios
            WHERE login = ? AND senha = ?
        """, (login, senha))

        usuario = cursor.fetchone()
        conn.close()

        if usuario is None:
            messagebox.showerror("Erro", "Login ou senha inválidos.")
            return

        usuario_id, nome, tipo = usuario
        tipo = tipo.lower()

        self.withdraw()

        if tipo == "admin":
            Dashboard()

        elif tipo == "aluno":
            TelaAluno(
                self,
                nome_aluno=nome,
                usuario_id=usuario_id
            )

        elif tipo == "professor":
            TelaProfessor(
                self,
                nome_professor=nome
            )

        else:
            messagebox.showerror("Erro", "Tipo de usuário inválido.")
            self.deiconify()


if __name__ == "__main__":
    app = TelaLogin()
    app.mainloop()