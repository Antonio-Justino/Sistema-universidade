import customtkinter as ctk
from tkinter import messagebox
from database.banco import conectar


class TelaMatricula(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Matrícula de Alunos")

        largura, altura = 500, 450
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

        self.grab_set()
        self.focus_set()

        ctk.CTkLabel(
            self,
            text="MATRÍCULA",
            font=("Roboto", 24, "bold")
        ).pack(pady=20)

        # ==========================
        # CARREGAR DADOS DO BANCO
        # ==========================
        self.alunos = self.carregar_alunos()
        self.disciplinas = self.carregar_disciplinas()

        # ==========================
        # ALUNO
        # ==========================
        ctk.CTkLabel(self, text="Aluno").pack(anchor="w", padx=40)
        self.combo_aluno = ctk.CTkComboBox(
            self,
            values=[f"{a[0]} - {a[1]}" for a in self.alunos]
        )
        self.combo_aluno.pack(padx=40, fill="x")

        # ==========================
        # DISCIPLINA
        # ==========================
        ctk.CTkLabel(self, text="Disciplina").pack(anchor="w", padx=40, pady=(10, 0))
        self.combo_disciplina = ctk.CTkComboBox(
            self,
            values=[f"{d[0]} - {d[1]}" for d in self.disciplinas]
        )
        self.combo_disciplina.pack(padx=40, fill="x")

        # ==========================
        # BOTÃO
        # ==========================
        ctk.CTkButton(
            self,
            text="Matricular",
            fg_color="green",
            command=self.salvar_matricula
        ).pack(pady=30, fill="x", padx=40)

    # ==========================
    # CARREGAR ALUNOS
    # ==========================
    def carregar_alunos(self):
        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT id, nome FROM alunos")
        dados = cur.fetchall()

        conn.close()
        return dados

    # ==========================
    # CARREGAR DISCIPLINAS
    # ==========================
    def carregar_disciplinas(self):
        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT id, nome FROM disciplinas")
        dados = cur.fetchall()

        conn.close()
        return dados

    # ==========================
    # SALVAR MATRÍCULA
    # ==========================
    def salvar_matricula(self):

        if not self.combo_aluno.get() or not self.combo_disciplina.get():
            messagebox.showwarning("Erro", "Selecione aluno e disciplina")
            return

        aluno_id = int(self.combo_aluno.get().split(" - ")[0])
        disciplina_id = int(self.combo_disciplina.get().split(" - ")[0])

        conn = conectar()
        cur = conn.cursor()

        # evita duplicação simples
        cur.execute("""
            SELECT * FROM matriculas
            WHERE aluno_id = ? AND disciplina_id = ?
        """, (aluno_id, disciplina_id))

        if cur.fetchone():
            messagebox.showwarning("Aviso", "Aluno já matriculado nesta disciplina")
            conn.close()
            return

        cur.execute("""
            INSERT INTO matriculas (aluno_id, disciplina_id)
            VALUES (?, ?)
        """, (aluno_id, disciplina_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Matrícula realizada com sucesso!")
        self.destroy()


# ==========================
# TESTE
# ==========================
if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    TelaMatricula(app)
    app.mainloop()