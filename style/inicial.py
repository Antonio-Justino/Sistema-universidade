import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
import os

# --- IMPORTAÇÕES DAS SUAS TELAS ---
try:
    from style.Cadastro import cadluno
except ImportError:
    cadluno = None
    print("Aviso: Arquivo Cadastro.py não encontrado.")

try:
    import disciplinas
except ImportError:
    class Dummy: TelaDisciplinas = None
    disciplinas = Dummy()
    print("Aviso: Arquivo disciplinas.py não encontrado.")

try:
    from Professores import TelaProfessores
except ImportError:
    TelaProfessores = None
    print("Aviso: Arquivo Professores.py não encontrado.")

# --- NOVO: IMPORTAÇÃO DE CURSOS ---
try:
    from Cursos import TelaCursos
except ImportError:
    TelaCursos = None
    print("Aviso: Arquivo Cursos.py não encontrado.")

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title("Sistema de Gestão Acadêmica - RAD")
        largura, altura = 800, 500
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

        ctk.CTkLabel(self, text="SISTEMA DE GESTÃO ACADÊMICA",
                     font=("Roboto", 24, "bold")).pack(pady=30)

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(expand=True, fill="both", padx=50, pady=20)
        self.frame_botoes.columnconfigure((0, 1), weight=1)

        # --- LISTA DE BOTÕES ATUALIZADA ---
        botoes = [
            ("CADASTRAR ALUNOS", self.abrir_app),
            ("CADASTRAR DISCIPLINAS", self.abrir_disciplinas),
            ("CADASTRAR PROFESSORES", self.abrir_professores),
            ("CADASTRAR CURSOS", self.abrir_cursos),
            ("CADASTRAR TURMAS", self.abrir_turmas),
            ("MATRÍCULAS", self.abrir_matriculas),
        ]

        for i, (texto, comando) in enumerate(botoes):
            btn = ctk.CTkButton(self.frame_botoes, text=texto,
                                command=comando,
                                height=50, font=("Roboto", 14, "bold"))
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")

        self.barra_status()
        self.atualizar_relogio()

    def barra_status(self):
        self.status_bar = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.status_bar.pack(side="bottom", fill="x")
        self.lbl_usuario = ctk.CTkLabel(self.status_bar, text="Usuário: root", font=("Roboto", 11))
        self.lbl_usuario.pack(side="left", padx=20)
        self.lbl_relogio = ctk.CTkLabel(self.status_bar, text="", font=("Roboto", 11))
        self.lbl_relogio.pack(side="right", padx=20)
        self.lbl_data = ctk.CTkLabel(self.status_bar, text="", font=("Roboto", 11))
        self.lbl_data.pack(side="right", padx=20)

    def atualizar_relogio(self):
        agora = datetime.now()
        self.lbl_data.configure(text=agora.strftime("%d/%m/%Y"))
        self.lbl_relogio.configure(text=agora.strftime("%H:%M:%S"))
        self.after(1000, self.atualizar_relogio)

    # --- MÉTODOS DE ABERTURA ---
    def abrir_app(self):
        if cadluno:
            cadluno(self)
        else:
            print("Erro: Tela de Alunos não carregada.")

    def abrir_disciplinas(self):
        if hasattr(disciplinas, 'TelaDisciplinas') and disciplinas.TelaDisciplinas:
            disciplinas.TelaDisciplinas(self)
        else:
            print("Erro: Tela de Disciplinas não carregada.")

    def abrir_professores(self):
        if TelaProfessores:
            TelaProfessores(self)
        else:
            print("Erro: Tela de Professores não carregada.")

    def abrir_cursos(self):
        if TelaCursos:
            TelaCursos(self)
        else:
            messagebox.showerror("Erro de Sistema", "Arquivo cursos.py não encontrado ou classe TelaCursos não definida.")
            
    def abrir_disciplinas(self):
        from disciplinas import TelaDisciplinas
        TelaDisciplinas(self)
        
    def abrir_turmas(self):
        from turmas import TelaTurmas
        TelaTurmas(self)
        
    def abrir_matriculas(self):
        from matriculas import TelaMatriculas
        TelaMatriculas(self)
    
if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()