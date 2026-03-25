import customtkinter as ctk
from tkinter import messagebox
import random

class TelaDisciplinas(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Gestão de Disciplinas - Sistema RAD")
        
        # --- UI DESIGN ---
        largura, altura = 450, 400
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

        # Configurações de Modalidade
        self.grab_set()
        self.focus_set()

        ctk.CTkLabel(self, text="CADASTRO DE DISCIPLINA", font=("Roboto", 20, "bold")).pack(pady=20)

        # --- CAMPO: ID DA DISCIPLINA (AUTOMÁTICO/BLOQUEADO) ---
        ctk.CTkLabel(self, text="ID da Disciplina (Automático)", font=("Roboto", 12)).pack(anchor="w", padx=45)
        
        self.entry_id = ctk.CTkEntry(self, width=360, height=35, 
                                     fg_color="#dcdde1", 
                                     text_color="#2f3640")
        self.entry_id.pack(pady=(0, 15))
        
        id_gerado = f"DISC-{random.randint(1000, 9999)}"
        self.entry_id.insert(0, id_gerado)
        self.entry_id.configure(state="readonly")

        # --- CAMPO: NOME DA DISCIPLINA ---
        ctk.CTkLabel(self, text="Nome da Disciplina *", font=("Roboto", 12)).pack(anchor="w", padx=45)
        self.entry_nome_disc = ctk.CTkEntry(self, placeholder_text="Ex: Algoritmos e Programação", width=360, height=35)
        self.entry_nome_disc.pack(pady=(0, 15))

        # --- BOTÕES ---
        self.btn_salvar = ctk.CTkButton(self, text="CADASTRAR DISCIPLINA", 
                                        command=self.salvar_disciplina, 
                                        fg_color="#3498db", 
                                        hover_color="#2980b9", 
                                        font=("Roboto", 16, "bold"), height=45)
        self.btn_salvar.pack(pady=30, padx=45, fill="x")

    # --- MÉTODOS ---

    def salvar_disciplina(self):
        nome = self.entry_nome_disc.get().strip()
        id_disc = self.entry_id.get()

        if not nome:
            messagebox.showwarning("Campo Vazio", "Por favor, informe o nome da disciplina!")
            return

        print(f"Disciplina Salva: {id_disc} - {nome}")
        messagebox.showinfo("Sucesso", f"Disciplina '{nome}' cadastrada com sucesso!")
        self.destroy()

# --- BLOCO DE EXECUÇÃO ---
if __name__ == "__main__":
    # Inicializa a janela principal (obrigatório para o CustomTkinter funcionar)
    root = ctk.CTk()
    
    # Escondemos a janela principal "vazia" para que apareça apenas o seu formulário
    root.withdraw() 
    
    # Criamos a sua tela de disciplinas
    app = TelaDisciplinas(root)
    
    # Mantém o programa rodando
    root.mainloop()