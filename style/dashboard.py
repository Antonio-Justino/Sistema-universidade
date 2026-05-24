import sys
import os


# PATH DO PROJETO
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
PASTA_RAIZ = os.path.dirname(PASTA_ATUAL)

if PASTA_RAIZ not in sys.path:
    sys.path.append(PASTA_RAIZ)


import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

from database.banco import criar_tabelas

# cria banco automaticamente
criar_tabelas()


# IMPORTAÇÕES SEGURAS

def safe_import(module, classe):
    try:
        mod = __import__(module, fromlist=[classe])
        return getattr(mod, classe)
    except:
        return None


TelaAlunos = safe_import("alunos", "TelaAlunos")
TelaDisciplinas = safe_import("disciplinas", "TelaDisciplinas")
TelaProfessores = safe_import("dadosprof", "TelaProfessores")
TelaCursos = safe_import("cursos", "TelaCursos")
TelaMatricula = safe_import("matricula", "TelaMatricula")
TelaProfessor = safe_import("professor", "TelaProfessor")

# DASHBOARD

class Dashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title("Sistema Gestão Acadêmica")

        largura = 900
        altura = 600

        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)

        self.geometry(f"{largura}x{altura}+{x}+{y}")

        # TÍTULO
        ctk.CTkLabel(
            self,
            text="SISTEMA DE GESTÃO ACADÊMICA",
            font=("Roboto", 24, "bold")
        ).pack(pady=30)

        # BOTÕES
        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=50, pady=20)

        self.frame.columnconfigure((0, 1), weight=1)

        botoes = [
            ("CADASTRAR ALUNOS", self.abrir_alunos),
            ("CADASTRAR DISCIPLINAS", self.abrir_disciplinas),
            ("CADASTRAR PROFESSORES", self.abrir_professores),
            ("CADASTRAR CURSOS", self.abrir_cursos),
            ("MATRÍCULAS", self.abrir_matriculas),
            ("PAINEL PROFESSOR", self.abrir_professor),
            ("TURMAS", self.abrir_turmas),
        ]

        for i, (texto, funcao) in enumerate(botoes):

            ctk.CTkButton(
                self.frame,
                text=texto,
                command=funcao,
                height=50,
                font=("Roboto", 14, "bold")
            ).grid(
                row=i // 2,
                column=i % 2,
                padx=10,
                pady=10,
                sticky="ew"
            )

        self.barra_status()
        self.atualizar_relogio()

    # STATUS BAR

    def barra_status(self):

        self.status = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.status.pack(side="bottom", fill="x")

        self.usuario = ctk.CTkLabel(self.status, text="Usuário: admin")
        self.usuario.pack(side="left", padx=20)

        self.relogio = ctk.CTkLabel(self.status, text="")
        self.relogio.pack(side="right", padx=20)

        self.data = ctk.CTkLabel(self.status, text="")
        self.data.pack(side="right", padx=20)

    def atualizar_relogio(self):

        agora = datetime.now()

        self.data.configure(text=agora.strftime("%d/%m/%Y"))
        self.relogio.configure(text=agora.strftime("%H:%M:%S"))

        self.after(1000, self.atualizar_relogio)

    # ABERTURA DE TELAS

    def abrir_alunos(self):
        if TelaAlunos:
            TelaAlunos(self)
        else:
            messagebox.showerror("Erro", "Tela alunos não encontrada")

    def abrir_disciplinas(self):
        if TelaDisciplinas:
            TelaDisciplinas(self)
        else:
            messagebox.showerror("Erro", "Tela disciplinas não encontrada")

    def abrir_professores(self):
        if TelaProfessores:
            TelaProfessores(self)
        else:
            messagebox.showerror("Erro", "Tela professores não encontrada")

    def abrir_cursos(self):
        if TelaCursos:
            TelaCursos(self)
        else:
            messagebox.showerror("Erro", "Tela cursos não encontrada")

    def abrir_matriculas(self):
        if TelaMatricula:
            TelaMatricula(self)
        else:
            messagebox.showerror("Erro", "Tela matrícula não encontrada")

    def abrir_professor(self):
        if TelaProfessor:
            TelaProfessor(self)
        else:
            messagebox.showerror("Erro", "Tela professor não encontrada")

    def abrir_turmas(self):
        messagebox.showinfo("Aviso", "Turmas ainda não implementadas")


# EXECUÇÃO COM LOGIN

if __name__ == "__main__":
    from login import TelaLogin

    app = TelaLogin()
    app.mainloop()