import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from tkinter import messagebox
from UsersDados.CPF import verificar_cpf

# Configuração de Aparência
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema RAD - Cadastro Moderno")
        self.geometry("450x600")

        # Título
        self.label_titulo = ctk.CTkLabel(
            self, text="CADASTRO DE ALUNO", font=("Roboto", 24, "bold")
        )
        self.label_titulo.pack(pady=30)

        # Campos
        self.criar_campo("CPF", "Ex: 000.000.000-00")
        self.entry_cpf = self.last_entry
        
        self.criar_campo("Nome Completo", "Digite o nome do aluno")
        self.entry_nome = self.last_entry

        self.criar_campo("Data de Nascimento", "DD/MM/AAAA")
        self.entry_nasc = self.last_entry

        self.criar_campo("Telefone", "(00) 00000-0000")
        self.entry_fone = self.last_entry

        self.criar_campo("E-mail", "aluno@escola.com")
        self.entry_email = self.last_entry

        # Botão
        self.btn_salvar = ctk.CTkButton(
            self,
            text="SALVAR ALUNO",
            command=self.salvar,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            font=("Roboto", 14, "bold"),
            height=45
        )
        self.btn_salvar.pack(pady=40, padx=40, fill="x")

    def criar_campo(self, texto, placeholder):
        label = ctk.CTkLabel(self, text=texto, font=("Roboto", 12))
        label.pack(anchor="w", padx=40)

        entry = ctk.CTkEntry(self, placeholder_text=placeholder, width=350, height=35)
        entry.pack(pady=(0, 15), padx=40)

        self.last_entry = entry

    def salvar(self):
        numero = self.entry_cpf.get()

        if verificar_cpf(numero):
            messagebox.showinfo("Validação", "CPF válido")
        else:
            messagebox.showerror("Erro", "CPF inválido")


if __name__ == "__main__":
    app = App()
    app.mainloop()