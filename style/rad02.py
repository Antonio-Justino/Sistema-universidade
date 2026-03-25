import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# Configurações globais (opcional, já que o main.py também as terá)
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TelaAlunos(ctk.CTkToplevel): # Alterado de ctk.CTk para ctk.CTkToplevel
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Sistema RAD - Cadastro de Aluno")
        
        # --- UI DESIGN ---
        largura, altura = 550, 750 # Ajustado para melhor visualização
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")
        
        # Foco e Modalidade
        self.grab_set()
        self.focus_set()

        # Container com Scroll
        self.container = ctk.CTkScrollableFrame(self, width=520, height=730, fg_color="transparent")
        self.container.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkLabel(self.container, text="CADASTRO DE ALUNO", font=("Roboto", 24, "bold")).pack(pady=20)

        # --- CAMPOS ---
        self.entry_cpf = self.criar_campo("CPF *", "000.000.000-00")
        self.entry_cpf.bind("<FocusOut>", self.validar_ao_sair_cpf)
        
        self.entry_nome = self.criar_campo("Nome Completo *", "Nome do aluno")
        
        self.entry_nasc = self.criar_campo("Data de Nascimento *", "DD/MM/AAAA")
        self.entry_nasc.bind("<KeyRelease>", self.formatar_data)

        # Sexo e Telefone
        frame_linha1 = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_linha1.pack(padx=40, fill="x")
        
        ctk.CTkLabel(frame_linha1, text="Sexo *", font=("Roboto", 12)).grid(row=0, column=0, sticky="w")
        self.combo_sexo = ctk.CTkComboBox(frame_linha1, values=["Masculino", "Feminino", "Outro"], width=150)
        self.combo_sexo.set("Selecione")
        self.combo_sexo.grid(row=1, column=0, padx=(0, 20), pady=(0, 10), sticky="w")

        ctk.CTkLabel(frame_linha1, text="Telefone *", font=("Roboto", 12)).grid(row=0, column=1, sticky="w")
        self.entry_fone = ctk.CTkEntry(frame_linha1, placeholder_text="(00) 00000-0000", width=230)
        self.entry_fone.grid(row=1, column=1, pady=(0, 10), sticky="w")
        self.entry_fone.bind("<KeyRelease>", self.formatar_telefone)

        self.entry_email = self.criar_campo("E-mail *", "exemplo@email.com")

        self.entry_cep = self.criar_campo("CEP *", "00000-000")
        self.entry_cep.bind("<FocusOut>", self.buscar_cep)
        
        self.entry_rua = self.criar_campo("Endereço *", "Rua, Avenida...")

        # Número e Complemento
        frame_casa = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_casa.pack(padx=40, fill="x")
        
        ctk.CTkLabel(frame_casa, text="Número *", font=("Roboto", 12)).grid(row=0, column=0, sticky="w")
        self.entry_numero = ctk.CTkEntry(frame_casa, width=100)
        self.entry_numero.grid(row=1, column=0, padx=(0, 10), pady=(0, 10), sticky="w")

        ctk.CTkLabel(frame_casa, text="Complemento", font=("Roboto", 12)).grid(row=0, column=1, sticky="w")
        self.entry_comp = ctk.CTkEntry(frame_casa, width=290)
        self.entry_comp.grid(row=1, column=1, pady=(0, 10), sticky="w")

        self.entry_bairro = self.criar_campo("Bairro *", "Bairro")
        self.entry_cidade = self.criar_campo("Cidade *", "Cidade")
        self.entry_uf = self.criar_campo("Estado (UF) *", "UF")

        self.btn_salvar = ctk.CTkButton(self.container, text="FINALIZAR CADASTRO", 
                                        command=self.salvar, fg_color="#2ecc71", 
                                        hover_color="#27ae60", font=("Roboto", 16, "bold"), height=50)
        self.btn_salvar.pack(pady=40, padx=40, fill="x")

    def criar_campo(self, texto, placeholder):
        label = ctk.CTkLabel(self.container, text=texto, font=("Roboto", 12))
        label.pack(anchor="w", padx=40)
        entry = ctk.CTkEntry(self.container, placeholder_text=placeholder, width=400, height=35)
        entry.pack(pady=(0, 10), padx=40, anchor="w")
        return entry

    # --- MÁSCARAS ---
    def formatar_data(self, event):
        t = re.sub(r'\D', '', self.entry_nasc.get())[:8]
        novo = ""
        for i, c in enumerate(t):
            if i in [2, 4]: novo += "/"
            novo += c
        self.entry_nasc.delete(0, "end")
        self.entry_nasc.insert(0, novo)

    def formatar_telefone(self, event):
        t = re.sub(r'\D', '', self.entry_fone.get())[:11]
        novo = ""
        if len(t) > 0: novo = "(" + t[:2]
        if len(t) > 2: novo += ") " + t[2:7]
        if len(t) > 7: novo += "-" + t[7:]
        self.entry_fone.delete(0, "end")
        self.entry_fone.insert(0, novo)

    # --- VALIDAÇÕES ---
    def validar_email(self, email):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        return re.search(regex, email)

    def validar_cpf_completo(self, cpf):
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11: return False
        for i in range(9, 11):
            soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
            digito = (soma * 10 % 11) % 10
            if digito != int(cpf[i]): return False
        return True

    def validar_ao_sair_cpf(self, event):
        val = self.entry_cpf.get()
        if val and not self.validar_cpf_completo(val):
            messagebox.showerror("Erro", "CPF Inválido!")
            self.after(100, lambda: self.entry_cpf.focus_set())

    def buscar_cep(self, event):
        cep = re.sub(r'\D', '', self.entry_cep.get())
        if len(cep) == 8:
            try:
                d = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
                if "erro" not in d:
                    self.preencher(self.entry_rua, d.get('logradouro'))
                    self.preencher(self.entry_bairro, d.get('bairro'))
                    self.preencher(self.entry_cidade, d.get('localidade'))
                    self.preencher(self.entry_uf, d.get('uf'))
                    self.entry_numero.delete(0, "end")
                    self.entry_comp.delete(0, "end")
                    self.entry_numero.focus_set()
            except: pass

    def preencher(self, campo, texto):
        campo.delete(0, "end")
        campo.insert(0, texto)

    def salvar(self):
        obrigatorios = [
            (self.entry_cpf, "CPF"), (self.entry_nome, "Nome"), 
            (self.entry_nasc, "Data de Nascimento"), (self.entry_fone, "Telefone"),
            (self.entry_email, "E-mail"), (self.entry_cep, "CEP"),
            (self.entry_rua, "Endereço"), (self.entry_numero, "Número"),
            (self.entry_bairro, "Bairro"), (self.entry_cidade, "Cidade"), (self.entry_uf, "UF")
        ]

        for campo, nome in obrigatorios:
            if not campo.get().strip():
                messagebox.showwarning("Campo Vazio", f"O campo {nome} é obrigatório!")
                campo.focus_set()
                campo.configure(border_color="red")
                return
            campo.configure(border_color=["#979DA2", "#565B5E"])

        if self.combo_sexo.get() == "Selecione":
            messagebox.showwarning("Atenção", "Selecione o Sexo!")
            self.combo_sexo.focus_set()
            return

        if not self.validar_email(self.entry_email.get()):
            messagebox.showerror("Erro", "E-mail com formato inválido!")
            self.entry_email.focus_set()
            return

        print("Aluno cadastrado com sucesso!")
        messagebox.showinfo("Sucesso", "Cadastro finalizado com sucesso!")
        self.destroy() # Importante: fecha a janela de cadastro e volta para o main

# --- BLOCO DE TESTE ---
if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw() # Esconde a principal para testar só esta
    app = TelaAlunos(root)
    root.mainloop()