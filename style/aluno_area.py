import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from database.banco import conectar, PASTA_ENTREGAS
import os
import shutil
import time
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

TAMANHO_MAXIMO = 10 * 1024 * 1024


class TelaAluno(ctk.CTkToplevel):
    def __init__(self, parent=None, nome_aluno="Aluno", usuario_id=None):
        super().__init__(parent)

        self.title("Área do Aluno")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.nome_aluno = nome_aluno
        self.usuario_id = usuario_id

        self.criar_layout()

    def criar_layout(self):
        self.menu = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.menu.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.menu,
            text="Área do Aluno",
            font=("Arial", 24, "bold")
        ).pack(pady=30)

        ctk.CTkButton(
            self.menu,
            text="Minhas Notas",
            command=self.mostrar_notas
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self.menu,
            text="Matérias",
            command=self.mostrar_materias
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self.menu,
            text="Tarefas",
            command=self.mostrar_tarefas
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self.menu,
            text="Estudos",
            command=self.mostrar_estudos
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self.menu,
            text="Sair",
            fg_color="red",
            hover_color="#8B0000",
            command=self.destroy
        ).pack(side="bottom", pady=30, padx=20, fill="x")

        self.area = ctk.CTkFrame(self)
        self.area.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        self.mostrar_inicio()

    def limpar_area(self):
        for widget in self.area.winfo_children():
            widget.destroy()

    def abrir_arquivo(self, caminho):
        if not caminho or not os.path.exists(caminho):
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            return

        try:
            subprocess.call(["open", caminho])
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{e}")

    def buscar_aluno_id(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM alunos
            WHERE usuario_id = ?
        """, (self.usuario_id,))

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return resultado[0]

        return None

    def mostrar_inicio(self):
        self.limpar_area()

        ctk.CTkLabel(
            self.area,
            text=f"Bem-vindo, {self.nome_aluno}",
            font=("Arial", 30, "bold")
        ).pack(pady=40)

        ctk.CTkLabel(
            self.area,
            text="Aqui você pode acessar suas notas, matérias, tarefas e conteúdos de estudo.",
            font=("Arial", 18)
        ).pack(pady=10)

    def mostrar_notas(self):
        self.limpar_area()

        ctk.CTkLabel(
            self.area,
            text="Minhas Notas",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        colunas = ("Matéria", "Nota 1", "Nota 2", "Média", "Situação")

        tabela = ttk.Treeview(
            self.area,
            columns=colunas,
            show="headings",
            height=10
        )

        for coluna in colunas:
            tabela.heading(coluna, text=coluna)
            tabela.column(coluna, width=150, anchor="center")

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                disciplinas.nome,
                notas.nota1,
                notas.nota2,
                notas.media
            FROM notas
            INNER JOIN alunos
                ON alunos.id = notas.aluno_id
            INNER JOIN disciplinas
                ON disciplinas.id = notas.disciplina_id
            WHERE alunos.usuario_id = ?
            ORDER BY disciplinas.nome
        """, (self.usuario_id,))

        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            tabela.insert(
                "",
                "end",
                values=("Nenhuma nota lançada", "-", "-", "-", "-")
            )

        for materia, nota1, nota2, media in resultados:
            situacao = "Aprovado" if media >= 6 else "Reprovado"

            tabela.insert(
                "",
                "end",
                values=(
                    materia,
                    f"{nota1:.1f}",
                    f"{nota2:.1f}",
                    f"{media:.2f}",
                    situacao
                )
            )

        tabela.pack(pady=20)

    def mostrar_materias(self):
        self.limpar_area()

        ctk.CTkLabel(
            self.area,
            text="Minhas Matérias",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT disciplinas.nome
            FROM matriculas
            INNER JOIN alunos
                ON alunos.id = matriculas.aluno_id
            INNER JOIN disciplinas
                ON disciplinas.id = matriculas.disciplina_id
            WHERE alunos.usuario_id = ?
            ORDER BY disciplinas.nome
        """, (self.usuario_id,))

        materias = cursor.fetchall()
        conn.close()

        if not materias:
            ctk.CTkLabel(
                self.area,
                text="Nenhuma matéria encontrada.",
                font=("Arial", 18)
            ).pack(pady=20)
            return

        for (materia,) in materias:
            card = ctk.CTkFrame(self.area)
            card.pack(pady=8, padx=30, fill="x")

            ctk.CTkLabel(
                card,
                text=materia,
                font=("Arial", 18)
            ).pack(pady=12, padx=15, anchor="w")

    def mostrar_tarefas(self):
        self.limpar_area()

        ctk.CTkLabel(
            self.area,
            text="Tarefas Disponíveis",
            font=("Arial", 28, "bold")
        ).pack(pady=15)

        colunas = ("ID", "Disciplina", "Título", "Entrega", "Status", "Arquivo")

        self.tabela_tarefas = ttk.Treeview(
            self.area,
            columns=colunas,
            show="headings",
            height=14
        )

        for coluna in colunas:
            self.tabela_tarefas.heading(coluna, text=coluna)
            self.tabela_tarefas.column(coluna, width=125, anchor="center")

        self.tabela_tarefas.pack(padx=20, pady=10, fill="both")

        botoes = ctk.CTkFrame(self.area, fg_color="transparent")
        botoes.pack(pady=10)

        ctk.CTkButton(
            botoes,
            text="Abrir PDF",
            command=self.abrir_tarefa
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            botoes,
            text="Enviar Resposta",
            fg_color="green",
            command=self.enviar_resposta
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            botoes,
            text="Atualizar",
            command=self.carregar_tarefas
        ).pack(side="left", padx=10)

        self.carregar_tarefas()

    def carregar_tarefas(self):
        self.caminhos_tarefas = {}

        for item in self.tabela_tarefas.get_children():
            self.tabela_tarefas.delete(item)

        aluno_id = self.buscar_aluno_id()

        if not aluno_id:
            self.tabela_tarefas.insert(
                "",
                "end",
                values=("-", "-", "Aluno não encontrado", "-", "-", "-")
            )
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                tarefas_pdf.id,
                disciplinas.nome,
                tarefas_pdf.titulo,
                tarefas_pdf.data_entrega,
                tarefas_pdf.arquivo_pdf,
                entregas_pdf.id
            FROM tarefas_pdf
            INNER JOIN disciplinas
                ON disciplinas.id = tarefas_pdf.disciplina_id
            INNER JOIN matriculas
                ON matriculas.disciplina_id = disciplinas.id
            INNER JOIN alunos
                ON alunos.id = matriculas.aluno_id
            LEFT JOIN entregas_pdf
                ON entregas_pdf.tarefa_id = tarefas_pdf.id
                AND entregas_pdf.aluno_id = alunos.id
            WHERE alunos.id = ?
            ORDER BY tarefas_pdf.id DESC
        """, (aluno_id,))

        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            self.tabela_tarefas.insert(
                "",
                "end",
                values=("-", "-", "Nenhuma tarefa disponível", "-", "-", "-")
            )
            return

        for tarefa_id, disciplina, titulo, data_entrega, arquivo_pdf, entrega_id in resultados:
            status = "Entregue" if entrega_id else "Pendente"

            self.caminhos_tarefas[str(tarefa_id)] = arquivo_pdf

            self.tabela_tarefas.insert(
                "",
                "end",
                values=(
                    tarefa_id,
                    disciplina,
                    titulo,
                    data_entrega if data_entrega else "-",
                    status,
                    os.path.basename(arquivo_pdf)
                )
            )

    def abrir_tarefa(self):
        item = self.tabela_tarefas.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione uma tarefa.")
            return

        valores = self.tabela_tarefas.item(item, "values")

        if not valores or valores[0] == "-":
            messagebox.showwarning("Aviso", "Selecione uma tarefa válida.")
            return

        tarefa_id = str(valores[0])
        caminho = self.caminhos_tarefas.get(tarefa_id)

        self.abrir_arquivo(caminho)

    def enviar_resposta(self):
        item = self.tabela_tarefas.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione uma tarefa.")
            return

        valores = self.tabela_tarefas.item(item, "values")

        if not valores or valores[0] == "-":
            messagebox.showwarning("Aviso", "Selecione uma tarefa válida.")
            return

        tarefa_id = int(valores[0])
        aluno_id = self.buscar_aluno_id()

        if not aluno_id:
            messagebox.showerror("Erro", "Aluno não encontrado.")
            return

        arquivo = filedialog.askopenfilename(
            title="Selecione seu PDF de resposta",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )

        if not arquivo:
            return

        if not arquivo.lower().endswith(".pdf"):
            messagebox.showerror("Erro", "Selecione apenas arquivos PDF.")
            return

        tamanho = os.path.getsize(arquivo)

        if tamanho > TAMANHO_MAXIMO:
            messagebox.showerror("Erro", "O PDF deve ter no máximo 10 MB.")
            return

        nome_original = os.path.basename(arquivo).replace(" ", "_")
        nome_final = f"aluno_{aluno_id}_tarefa_{tarefa_id}_{int(time.time())}_{nome_original}"

        destino = os.path.join(PASTA_ENTREGAS, nome_final)

        try:
            shutil.copy2(arquivo, destino)

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO entregas_pdf
                (tarefa_id, aluno_id, arquivo_pdf)
                VALUES (?, ?, ?)
                ON CONFLICT(tarefa_id, aluno_id)
                DO UPDATE SET
                    arquivo_pdf = excluded.arquivo_pdf,
                    data_envio = CURRENT_TIMESTAMP
            """, (
                tarefa_id,
                aluno_id,
                destino
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Trabalho enviado com sucesso.")
            self.carregar_tarefas()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar trabalho:\n{e}")

    def mostrar_estudos(self):
        self.limpar_area()

        ctk.CTkLabel(
            self.area,
            text="Área de Estudos",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        estudos = [
            ("Algoritmos", "Revisar laços de repetição e funções."),
            ("Banco de Dados", "Estudar SELECT, INSERT, UPDATE e DELETE."),
            ("Estrutura de Dados", "Revisar listas, pilhas e filas."),
        ]

        for materia, descricao in estudos:
            card = ctk.CTkFrame(self.area)
            card.pack(pady=10, padx=30, fill="x")

            ctk.CTkLabel(
                card,
                text=materia,
                font=("Arial", 20, "bold")
            ).pack(anchor="w", padx=15, pady=(10, 0))

            ctk.CTkLabel(
                card,
                text=descricao,
                font=("Arial", 15)
            ).pack(anchor="w", padx=15, pady=(5, 10))


if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()

    tela = TelaAluno(app, nome_aluno="Antônio", usuario_id=2)
    app.mainloop()