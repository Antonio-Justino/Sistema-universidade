import customtkinter as ctk
from tkinter import messagebox
import random # Usado aqui para simular um ID gerado pelo banco

class TelaCursos(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # --- CONFIGURAÇÃO DA JANELA ---
        self.title("Sistema RAD - Cadastro de Cursos")
        largura, altura = 450, 500
        
        # Lógica de centralização na tela do usuário
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

        # --- COMPORTAMENTO MODAL ---
        self.grab_set()      # Bloqueia interação com a janela principal
        self.focus_set()     # Foca o teclado nesta janela
        
        # --- TÍTULO ---
        ctk.CTkLabel(self, text="CADASTRO DE CURSO", font=("Roboto", 22, "bold")).pack(pady=30)

        # --- CAMPO: ID DO CURSO (AUTOMÁTICO) ---
        # No RAD, campos automáticos devem ser exibidos, mas travados (state="disabled")
        ctk.CTkLabel(self, text="ID do Curso (Gerado pelo Sistema):", font=("Roboto", 12)).pack(anchor="w", padx=45)
        self.entry_id = ctk.CTkEntry(self, width=360, height=35, fg_color="#dcdde1")
        
        # Simulando um ID automático (ex: 101)
        id_automatico = random.randint(100, 999) 
        self.entry_id.insert(0, f"CURSO-{id_automatico}")
        
        self.entry_id.configure(state="disabled") # Impede que o usuário altere o ID
        self.entry_id.pack(pady=(0, 20))

        # --- CAMPO: NOME DO CURSO ---
        ctk.CTkLabel(self, text="Nome do Curso *", font=("Roboto", 12)).pack(anchor="w", padx=45)
        self.entry_nome_curso = ctk.CTkEntry(self, placeholder_text="Ex: Engenharia de Software", width=360, height=35)
        self.entry_nome_curso.pack(pady=(0, 20))

        # --- CAMPO: CARGA HORÁRIA ---
        ctk.CTkLabel(self, text="Carga Horária (Horas) *", font=("Roboto", 12)).pack(anchor="w", padx=45)
        self.entry_carga = ctk.CTkEntry(self, placeholder_text="Ex: 120", width=360, height=35)
        self.entry_carga.pack(pady=(0, 30))

        # --- BOTÕES DE AÇÃO ---
        # Botão para salvar
        self.btn_salvar = ctk.CTkButton(self, text="SALVAR CURSO", 
                                        command=self.salvar_curso, 
                                        fg_color="#2ecc71", hover_color="#27ae60",
                                        font=("Roboto", 16, "bold"), height=45)
        self.btn_salvar.pack(pady=10, padx=45, fill="x")

        # Botão para cancelar/fechar
        self.btn_cancelar = ctk.CTkButton(self, text="CANCELAR", 
                                          command=self.destroy, 
                                          fg_color="#e74c3c", hover_color="#c0392b",
                                          font=("Roboto", 14))
        self.btn_cancelar.pack(pady=10, padx=45, fill="x")

    # --- LÓGICA DE NEGÓCIO ---

    def salvar_curso(self):
        """
        Função responsável por validar os dados e simular o salvamento.
        """
        nome = self.entry_nome_curso.get()
        carga = self.entry_carga.get()

        # Validação simples de campos vazios
        if not nome or not carga:
            messagebox.showwarning("Erro de Cadastro", "Por favor, preencha todos os campos obrigatórios (*)")
            return

        # Validação se a carga horária é apenas números
        if not carga.isdigit():
            messagebox.showerror("Erro de Formato", "A carga horária deve conter apenas números!")
            return

        # Feedback de Sucesso para o aluno
        messagebox.showinfo("Sistema RAD", f"Curso '{nome}' cadastrado com sucesso!\nID: {self.entry_id.get()}")
        
        # Fecha a janela após o sucesso
        self.destroy()

# --- TESTE INDEPENDENTE ---
if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw() # Esconde a janela principal para abrir apenas o módulo de cursos
    app = TelaCursos(root)
    root.mainloop()