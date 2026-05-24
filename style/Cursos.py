import customtkinter as ctk
from tkinter import messagebox
from banco import conectar


class TelaCursos(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Sistema RAD - Cadastro de Cursos")

        largura = 450
        altura = 400

        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)

        self.geometry(f"{largura}x{altura}+{x}+{y}")

        self.grab_set()
        self.focus_set()

        # =========================
        # TÍTULO
        # =========================
        ctk.CTkLabel(
            self,
            text="CADASTRO DE CURSO",
            font=("Roboto", 22, "bold")
        ).pack(pady=20)

        # =========================
        # NOME
        # =========================
        ctk.CTkLabel(self, text="Nome do Curso *").pack()

        self.entry_nome = ctk.CTkEntry(self, width=300)
        self.entry_nome.pack(pady=5)

        # =========================
        # CARGA HORÁRIA
        # =========================
        ctk.CTkLabel(self, text="Carga Horária *").pack()

        self.entry_carga = ctk.CTkEntry(self, width=300)
        self.entry_carga.pack(pady=5)

        # =========================
        # BOTÃO SALVAR
        # =========================
        ctk.CTkButton(
            self,
            text="Salvar Curso",
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.salvar
        ).pack(pady=20)

        # =========================
        # BOTÃO CANCELAR
        # =========================
        ctk.CTkButton(
            self,
            text="Cancelar",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.destroy
        ).pack()

    # =========================
    # SALVAR NO BANCO
    # =========================
    def salvar(self):

        nome = self.entry_nome.get().strip()
        carga = self.entry_carga.get().strip()

        if not nome or not carga:
            messagebox.showwarning(
                "Erro",
                "Preencha todos os campos"
            )
            return

        if not carga.isdigit():
            messagebox.showerror(
                "Erro",
                "Carga horária deve ser número"
            )
            return

        try:
            conn = conectar()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO cursos
                (nome, carga_horaria)
                VALUES (?, ?)
            """, (nome, int(carga)))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sucesso",
                f"Curso '{nome}' cadastrado!"
            )

            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "Erro Banco",
                str(e)
            )


# =========================
# TESTE
# =========================
if __name__ == "__main__":

    app = ctk.CTk()
    app.withdraw()

    TelaCursos(app)

    app.mainloop()