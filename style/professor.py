import customtkinter as ctk
from tkinter import messagebox
import re
import requests
# Importa a segunda tela

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
        
        # Container com Scroll para acomodar todos os campos
        self.container = ctk.CTkScrollableFrame(self, width=520, height=730, fg_color="transparent")
        self.container.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkLabel(self.container, text="CADASTRO DE PROFESSOR", font=("Roboto", 24, "bold")).pack(pady=20)

        # --- SEÇÃO DE CAMPOS ---
        self.entry_cpf = self.criar_campo("CPF *", "000.000.000-00")
        self.entry_cpf.bind("<FocusOut>", self.validar_ao_sair_cpf) 
        
        self.entry_nome = self.criar_campo("Nome Completo *", "Nome do professor")
        
        self.entry_nasc = self.criar_campo("Data de Nascimento *", "DD/MM/AAAA")
        self.entry_nasc.bind("<KeyRelease>", self.formatar_data)

        # Frame Sexo e Telefone (Lado a Lado)
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

    # --- NAVEGAÇÃO ---
    def abrir_dados_academicos(self):
        # Validação de campos críticos antes de mudar de tela
        if not self.entry_nome.get() or not self.entry_cpf.get() or self.combo_sexo.get() == "Selecione":
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha o Nome, CPF e Sexo.")
            return
            
        # Empacotamento dos dados para a tabela 'professores'
        dados_pessoais = {
            "cpf": self.entry_cpf.get(),
            "nome": self.entry_nome.get(),
            "nasc": self.entry_nasc.get(),
            "sexo": self.combo_sexo.get(),
            "fone": self.entry_fone.get(),
            "email": self.entry_email.get(),
            "cep": self.entry_cep.get(),
            "rua": self.entry_rua.get(),
            "numero": self.entry_numero.get(),
            "comp": self.entry_comp.get(),
            "bairro": self.entry_bairro.get(),
            "cidade": self.entry_cidade.get(),
            "uf": self.entry_uf.get()
        }
            
        # Passa os dados para a próxima classe
        TelaDadosAcad(self.master, dados_fase1=dados_pessoais)
        self.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    app = TelaProfessores(root)
    root.mainloop()


import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import re

class TelaDadosAcad(ctk.CTkToplevel):
    def __init__(self, parent, dados_fase1=None):
        super().__init__(parent)
        self.dados_fase1 = dados_fase1 

        self.title("Dados Acadêmicos - Módulo Adicional")
        
        # --- UI DESIGN ---
        largura, altura = 500, 600
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

        self.grab_set()
        self.focus_set()
        self.after(10, self.lift) 

        ctk.CTkLabel(self, text="FORMAÇÃO DO DOCENTE", font=("Roboto", 20, "bold")).pack(pady=20)

        # --- CAMPOS ---
        self.entry_inst = self.criar_campo("Instituição *", "Ex: Universidade Federal...")
        self.entry_curso = self.criar_campo("Nome do Curso *", "Ex: Licenciatura em História")

        ctk.CTkLabel(self, text="Grau *", font=("Roboto", 12)).pack(anchor="w", padx=45)
        self.combo_grau = ctk.CTkComboBox(self, 
                                          values=["Graduação", "Especialização", "Mestrado", "Doutorado", "Pós-Doutorado"], 
                                          width=410)
        self.combo_grau.set("Selecione")
        self.combo_grau.pack(pady=(0, 15))

        # --- LAYOUT EM GRID (DATAS) ---
        frame_datas = ctk.CTkFrame(self, fg_color="transparent")
        frame_datas.pack(padx=45, fill="x")

        ctk.CTkLabel(frame_datas, text="Início (MM/AAAA) *", font=("Roboto", 12)).grid(row=0, column=0, sticky="w")
        self.entry_ini = ctk.CTkEntry(frame_datas, placeholder_text="00/0000", width=200)
        self.entry_ini.grid(row=1, column=0, padx=(0, 10), pady=(0, 10))
        self.entry_ini.bind("<KeyRelease>", lambda e: self.mascara_mes_ano(self.entry_ini))

        ctk.CTkLabel(frame_datas, text="Fim (MM/AAAA) *", font=("Roboto", 12)).grid(row=0, column=1, sticky="w")
        self.entry_fim = ctk.CTkEntry(frame_datas, placeholder_text="00/0000", width=200)
        self.entry_fim.grid(row=1, column=1, pady=(0, 10))
        self.entry_fim.bind("<KeyRelease>", lambda e: self.mascara_mes_ano(self.entry_fim))

        # --- BOTÃO FINALIZAR ---
        self.btn_confirmar = ctk.CTkButton(self, text="FINALIZAR CADASTRO", 
                                           command=self.confirmar, fg_color="#2ecc71", 
                                           hover_color="#27ae60", font=("Roboto", 16, "bold"), height=45)
        self.btn_confirmar.pack(pady=40, padx=45, fill="x")

    def criar_campo(self, texto, placeholder):
        label = ctk.CTkLabel(self, text=texto, font=("Roboto", 12))
        label.pack(anchor="w", padx=45)
        entry = ctk.CTkEntry(self, placeholder_text=placeholder, width=410, height=35)
        entry.pack(pady=(0, 15))
        return entry

    def mascara_mes_ano(self, campo):
        t = re.sub(r'\D', '', campo.get())[:6]
        novo = ""
        for i, c in enumerate(t):
            if i == 2: novo += "/"
            novo += c
        campo.delete(0, "end")
        campo.insert(0, novo)

    # --- SALVAMENTO RELACIONAL ---
    def confirmar(self):
        inst = self.entry_inst.get().strip()
        curso = self.entry_curso.get().strip()
        grau = self.combo_grau.get()

        if not inst or not curso or grau == "Selecione":
            messagebox.showwarning("Validação", "Preencha os campos acadêmicos!")
            return

        try:
            conn = sqlite3.connect('sistema_escolar.db')
            cursor = conn.cursor()

            # 1. Inserir na tabela PROFESSORES
            sql_prof = """
            INSERT INTO professores (
                cpf, nome, nascimento, sexo, telefone, email, 
                cep, logradouro, numero, complemento, bairro, cidade, uf
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            valores_prof = (
                self.dados_fase1['cpf'], self.dados_fase1['nome'], self.dados_fase1['nasc'],
                self.dados_fase1['sexo'], self.dados_fase1['fone'], self.dados_fase1['email'],
                self.dados_fase1['cep'], self.dados_fase1['rua'], self.dados_fase1['numero'],
                self.dados_fase1['comp'], self.dados_fase1['bairro'], self.dados_fase1['cidade'],
                self.dados_fase1['uf']
            )
            cursor.execute(sql_prof, valores_prof)
            
            # 2. Pegar o ID gerado para esse professor
            professor_id = cursor.lastrowid

            # 3. Inserir na tabela FORMACAO_ACADEMICA vinculando ao ID
            sql_acad = """
            INSERT INTO formacao_academica (
                professor_id, instituicao, curso, grau, data_inicio, data_fim
            ) VALUES (?, ?, ?, ?, ?, ?)
            """
            valores_acad = (professor_id, inst, curso, grau, self.entry_ini.get(), self.entry_fim.get())
            cursor.execute(sql_acad, valores_acad)

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", f"Professor {self.dados_fase1['nome']} cadastrado com formação!")
            self.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este CPF já está cadastrado no sistema!")
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Erro ao gravar no banco: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    dados_fake = {"cpf":"000.000.000-00","nome":"Teste","nasc":"","sexo":"","fone":"","email":"","cep":"","rua":"","numero":"","comp":"","bairro":"","cidade":"","uf":""}
    app = TelaDadosAcad(root, dados_fase1=dados_fake)
    root.mainloop()