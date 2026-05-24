import customtkinter as ctk
from tkinter import messagebox
import re
import requests

from database.banco import conectar


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class TelaAlunos(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Sistema RAD - Cadastro de Aluno")

        largura, altura = 550, 750
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

        self.grab_set()
        self.focus_set()

        self.container = ctk.CTkScrollableFrame(
            self,
            width=520,
            height=730,
            fg_color="transparent"
        )
        self.container.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkLabel(
            self.container,
            text="CADASTRO DE ALUNO",
            font=("Roboto", 24, "bold")
        ).pack(pady=20)

        # CAMPOS
        self.entry_cpf = self.criar_campo("CPF *", "000.000.000-00")
        self.entry_cpf.bind("<FocusOut>", self.validar_ao_sair_cpf)

        self.entry_nome = self.criar_campo("Nome Completo *", "Nome do aluno")

        self.entry_nasc = self.criar_campo("Data de Nascimento *", "DD/MM/AAAA")
        self.entry_nasc.bind("<KeyRelease>", self.formatar_data)

        frame1 = ctk.CTkFrame(self.container, fg_color="transparent")
        frame1.pack(padx=40, fill="x")

        ctk.CTkLabel(frame1, text="Sexo *").grid(row=0, column=0, sticky="w")
        self.combo_sexo = ctk.CTkComboBox(
            frame1,
            values=["Masculino", "Feminino", "Outro"]
        )
        self.combo_sexo.set("Selecione")
        self.combo_sexo.grid(row=1, column=0, padx=10)

        ctk.CTkLabel(frame1, text="Telefone *").grid(row=0, column=1, sticky="w")
        self.entry_fone = ctk.CTkEntry(frame1, placeholder_text="(00) 00000-0000")
        self.entry_fone.grid(row=1, column=1)
        self.entry_fone.bind("<KeyRelease>", self.formatar_telefone)

        self.entry_email = self.criar_campo("E-mail *", "email@exemplo.com")

        self.entry_cep = self.criar_campo("CEP *", "00000-000")
        self.entry_cep.bind("<FocusOut>", self.buscar_cep)

        self.entry_rua = self.criar_campo("Endereço *", "")

        frame2 = ctk.CTkFrame(self.container, fg_color="transparent")
        frame2.pack(padx=40, fill="x")

        ctk.CTkLabel(frame2, text="Número *").grid(row=0, column=0)
        self.entry_numero = ctk.CTkEntry(frame2, width=100)
        self.entry_numero.grid(row=1, column=0)

        ctk.CTkLabel(frame2, text="Complemento").grid(row=0, column=1)
        self.entry_comp = ctk.CTkEntry(frame2, width=250)
        self.entry_comp.grid(row=1, column=1)

        self.entry_bairro = self.criar_campo("Bairro *", "")
        self.entry_cidade = self.criar_campo("Cidade *", "")
        self.entry_uf = self.criar_campo("UF *", "")

        ctk.CTkButton(
            self.container,
            text="SALVAR",
            command=self.salvar,
            fg_color="green"
        ).pack(pady=30, fill="x", padx=40)

    # ----------------------
    # CAMPOS
    # ----------------------
    def criar_campo(self, label, placeholder):
        ctk.CTkLabel(self.container, text=label).pack(anchor="w", padx=40)
        entry = ctk.CTkEntry(self.container, placeholder_text=placeholder)
        entry.pack(pady=5, padx=40, fill="x")
        return entry

    # ----------------------
    # MÁSCARAS
    # ----------------------
    def formatar_data(self, event):
        t = re.sub(r'\D', '', self.entry_nasc.get())[:8]
        novo = ""
        for i, c in enumerate(t):
            if i in [2, 4]:
                novo += "/"
            novo += c
        self.entry_nasc.delete(0, "end")
        self.entry_nasc.insert(0, novo)

    def formatar_telefone(self, event):
        t = re.sub(r'\D', '', self.entry_fone.get())[:11]
        novo = ""
        if len(t) > 0:
            novo = "(" + t[:2]
        if len(t) > 2:
            novo += ") " + t[2:7]
        if len(t) > 7:
            novo += "-" + t[7:]

        self.entry_fone.delete(0, "end")
        self.entry_fone.insert(0, novo)

    # ----------------------
    # VALIDAÇÕES
    # ----------------------
    def validar_email(self, email):
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

    def validar_cpf(self, cpf):
        cpf = re.sub(r'\D', '', cpf)
        return len(cpf) == 11

    def validar_ao_sair_cpf(self, event):
        if not self.validar_cpf(self.entry_cpf.get()):
            messagebox.showerror("Erro", "CPF inválido")

    # ----------------------
    # CEP
    # ----------------------
    def buscar_cep(self, event):
        cep = re.sub(r'\D', '', self.entry_cep.get())

        if len(cep) == 8:
            try:
                r = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()

                if "erro" not in r:
                    self.entry_rua.delete(0, "end")
                    self.entry_rua.insert(0, r.get("logradouro", ""))

                    self.entry_bairro.delete(0, "end")
                    self.entry_bairro.insert(0, r.get("bairro", ""))

                    self.entry_cidade.delete(0, "end")
                    self.entry_cidade.insert(0, r.get("localidade", ""))

                    self.entry_uf.delete(0, "end")
                    self.entry_uf.insert(0, r.get("uf", ""))

            except:
                pass

    # ----------------------
    # SALVAR NO BANCO
    # ----------------------
    def salvar(self):

        campos = [
            self.entry_cpf,
            self.entry_nome,
            self.entry_nasc,
            self.entry_fone,
            self.entry_email,
            self.entry_cep,
            self.entry_rua,
            self.entry_numero,
            self.entry_bairro,
            self.entry_cidade,
            self.entry_uf
        ]

        for c in campos:
            if not c.get().strip():
                messagebox.showwarning("Erro", "Preencha todos os campos")
                return

        if self.combo_sexo.get() == "Selecione":
            messagebox.showwarning("Erro", "Selecione o sexo")
            return

        if not self.validar_email(self.entry_email.get()):
            messagebox.showerror("Erro", "Email inválido")
            return

        try:
            conn = conectar()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO alunos (
                    cpf, nome, nascimento, sexo,
                    telefone, email, cep, rua,
                    numero, complemento, bairro,
                    cidade, uf
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.entry_cpf.get(),
                self.entry_nome.get(),
                self.entry_nasc.get(),
                self.combo_sexo.get(),
                self.entry_fone.get(),
                self.entry_email.get(),
                self.entry_cep.get(),
                self.entry_rua.get(),
                self.entry_numero.get(),
                self.entry_comp.get(),
                self.entry_bairro.get(),
                self.entry_cidade.get(),
                self.entry_uf.get()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Aluno salvo com sucesso")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Erro", str(e))