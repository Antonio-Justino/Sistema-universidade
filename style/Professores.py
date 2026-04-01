import customtkinter as ctk
from tkinter import messagebox
import sys
import os
# IMPORTANTE: Importa a segunda tela do seu outro arquivo
from professores_dadosacad import TelaDadosAcad 

class TelaProfessores(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Sistema RAD - Cadastro de Professores")
        
        # --- LÓGICA DE CENTRALIZAÇÃO ---
        largura, altura = 550, 750
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")
        
        self.grab_set()
        self.focus_set()
        
        # Container com Scroll
        self.container = ctk.CTkScrollableFrame(self, width=520, height=730, fg_color="transparent")
        self.container.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkLabel(self.container, text="CADASTRO DE PROFESSOR", font=("Roboto", 24, "bold")).pack(pady=20)

        # --- SEÇÃO DE CAMPOS ---
        self.entry_cpf = self.criar_campo("CPF *", "000.000.000-00")
        self.entry_cpf.bind("<FocusOut>", self.validar_ao_sair_cpf) 
        
        self.entry_nome = self.criar_campo("Nome Completo *", "Nome do professor")
        self.entry_nasc = self.criar_campo("Data de Nascimento *", "DD/MM/AAAA")
        self.entry_nasc.bind("<KeyRelease>", self.formatar_data)

        # Frame Sexo e Telefone
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

        # Frame Número e Complemento
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

        # BOTÃO ATUALIZADO: Agora chama a função que abre a próxima tela
        self.btn_proximo = ctk.CTkButton(self.container, text="PRÓXIMA ETAPA: DADOS ACADÊMICOS", 
                                         command=self.abrir_dados_academicos, fg_color="#3498db", 
                                         hover_color="#2980b9", font=("Roboto", 16, "bold"), height=50)
        self.btn_proximo.pack(pady=(20, 40), padx=40, fill="x")

    # --- MÉTODOS AUXILIARES ---
    def criar_campo(self, texto, placeholder):
        label = ctk.CTkLabel(self.container, text=texto, font=("Roboto", 12))
        label.pack(anchor="w", padx=40)
        entry = ctk.CTkEntry(self.container, placeholder_text=placeholder, width=400, height=35)
        entry.pack(pady=(0, 10), padx=40, anchor="w")
        return entry

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
            messagebox.showerror("Erro de Validação", "CPF digitado é inválido!")
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
                    self.entry_numero.focus_set()
            except: pass

    def preencher(self, campo, texto):
        campo.delete(0, "end")
        campo.insert(0, texto)

    # FUNÇÃO QUE CHAMA A PRÓXIMA TELA
    def abrir_dados_academicos(self):
        # Validação simples
        if not self.entry_nome.get() or not self.entry_cpf.get():
            messagebox.showwarning("Atenção", "Preencha o Nome e CPF antes de prosseguir.")
            return
            
        # Instancia a tela de dados acadêmicos
        TelaDadosAcad(self.master)
        # Fecha a tela atual
        self.destroy()

# --- BLOCO PARA TESTAR ---
if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    app = TelaProfessores(root)
    root.mainloop()


#DADOS ACADEMICOS

import customtkinter as ctk
from tkinter import messagebox
import re

# No RAD, a modularidade permite que diferentes desenvolvedores trabalhem 
# em telas diferentes simultaneamente.
class TelaDadosAcad(ctk.CTkToplevel):
    def __init__(self, parent):
        # O 'parent' permite que esta janela saiba quem é a 'mãe' (App Principal)
        super().__init__(parent)

        self.title("Dados Acadêmicos - Módulo Adicional")
        
        # --- DESIGN DE INTERFACE (UI) ---
        largura, altura = 500, 600
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

        # --- COMPORTAMENTO MODAL (CRÍTICO NO RAD) ---
        # grab_set() impede o usuário de clicar na janela principal.
        # Isso garante a INTEGRIDADE DOS DADOS: o usuário deve terminar aqui antes de seguir.
        self.grab_set()
        self.focus_set()
        self.after(10, self.lift) # Garante que a janela suba para o topo

        ctk.CTkLabel(self, text="FORMAÇÃO DO DOCENTE", font=("Roboto", 20, "bold")).pack(pady=20)

        # --- CAMPOS DINÂMICOS ---
        self.entry_inst = self.criar_campo("Instituição *", "Ex: Universidade Federal...")
        self.entry_curso = self.criar_campo("Nome do Curso *", "Ex: Licenciatura em História")

        # ComboBox: Reduz erro de digitação oferecendo opções pré-definidas
        ctk.CTkLabel(self, text="Grau *", font=("Roboto", 12)).pack(anchor="w", padx=45)
        self.combo_grau = ctk.CTkComboBox(self, 
                                          values=["Graduação", "Especialização", "Mestrado", "Doutorado", "Pós-Doutorado"], 
                                          width=410)
        self.combo_grau.set("Selecione")
        self.combo_grau.pack(pady=(0, 15))

        # --- LAYOUT EM GRID (ORGANIZAÇÃO DE ESPAÇO) ---
        # Criamos um sub-container (Frame) para colocar as datas lado a lado.
        frame_datas = ctk.CTkFrame(self, fg_color="transparent")
        frame_datas.pack(padx=45, fill="x")

        ctk.CTkLabel(frame_datas, text="Início (MM/AAAA) *", font=("Roboto", 12)).grid(row=0, column=0, sticky="w")
        self.entry_ini = ctk.CTkEntry(frame_datas, placeholder_text="00/0000", width=200)
        self.entry_ini.grid(row=1, column=0, padx=(0, 10), pady=(0, 10))
        # Lambda permite passar o próprio campo como argumento para a função de máscara
        self.entry_ini.bind("<KeyRelease>", lambda e: self.mascara_mes_ano(self.entry_ini))

        ctk.CTkLabel(frame_datas, text="Fim (MM/AAAA) *", font=("Roboto", 12)).grid(row=0, column=1, sticky="w")
        self.entry_fim = ctk.CTkEntry(frame_datas, placeholder_text="00/0000", width=200)
        self.entry_fim.grid(row=1, column=1, pady=(0, 10))
        self.entry_fim.bind("<KeyRelease>", lambda e: self.mascara_mes_ano(self.entry_fim))

        # --- BOTÃO DE CONFIRMAÇÃO ---
        self.btn_confirmar = ctk.CTkButton(self, text="SALVAR DADOS ACADÊMICOS", 
                                           command=self.confirmar, fg_color="#2ecc71", 
                                           hover_color="#27ae60", font=("Roboto", 16, "bold"), height=45)
        self.btn_confirmar.pack(pady=40, padx=45, fill="x")

    # --- MÉTODOS DE SUPORTE ---

    def criar_campo(self, texto, placeholder):
        """Padronização visual: Todos os campos seguem o mesmo estilo."""
        label = ctk.CTkLabel(self, text=texto, font=("Roboto", 12))
        label.pack(anchor="w", padx=45)
        entry = ctk.CTkEntry(self, placeholder_text=placeholder, width=410, height=35)
        entry.pack(pady=(0, 15))
        return entry

    def mascara_mes_ano(self, campo):
        """Regex e Formatação: Melhora a experiência do usuário (UX)."""
        t = re.sub(r'\D', '', campo.get())[:6]
        novo = ""
        for i, c in enumerate(t):
            if i == 2: novo += "/"
            novo += c
        campo.delete(0, "end")
        campo.insert(0, novo)

    def confirmar(self):
        """Validação Final: O RAD preza pela velocidade, mas nunca sem validação."""
        if not self.entry_inst.get() or self.combo_grau.get() == "Selecione":
            messagebox.showwarning("Validação", "Os campos Instituição e Grau são obrigatórios!")
            return
        
        # Sucesso: Informa o usuário e 'mata' a janela para voltar à principal.
        messagebox.showinfo("Módulo Acadêmico", "Dados capturados com sucesso!")
        self.destroy()

