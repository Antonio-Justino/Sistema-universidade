import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from database.banco import conectar, PASTA_TAREFAS
import os
import shutil
import time
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

TAMANHO_MAXIMO = 10 * 1024 * 1024


class TelaProfessor(ctk.CTkToplevel):
    def __init__(self, parent=None, nome_professor="Professor"):
        super().__init__(parent)

        self.title("Área do Professor")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.nome_professor = nome_professor
        self.pdf_selecionado = None

        self.criar_layout()

    def criar_layout(self):
        self.menu = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.menu.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.menu,
            text="Área do Professor",
            font=("Arial", 22, "bold")
        ).pack(pady=30)

        ctk.CTkButton(
            self.menu,
            text="Alunos",
            command=self.mostrar_alunos
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self.menu,
            text="Lançar Notas",
            command=self.mostrar_notas
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self.menu,
            text="Tarefas PDF",
            command=self.mostrar_tarefas_pdf
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

    def mostrar_inicio(self):
        self.limpar_area()

        ctk.CTkLabel(
            self.area,
            text=f"Bem-vindo, {self.nome_professor}",
            font=("Arial", 30, "bold")
        ).pack(pady=40)

        ctk.CTkLabel(
            self.area,
            text="Aqui você pode lançar notas e tarefas para os alunos.",
            font=("Arial", 18)
        ).pack(pady=10)

    def abrir_arquivo(self, caminho):
        if not caminho or not os.path.exists(caminho):
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            return

        try:
            subprocess.call(["open", caminho])
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{e}")

    def buscar_alunos(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nome
            FROM alunos
            ORDER BY nome
        """)

        dados = cursor.fetchall()
        conn.close()

        return dados

    def buscar_disciplinas(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nome
            FROM disciplinas
            ORDER BY nome
        """)

        dados = cursor.fetchall()
        conn.close()

        return dados

    def mostrar_alunos(self):
        self.limpar_area()

        ctk.CTkLabel(
            self.area,
            text="Lista de Alunos",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        colunas = ("ID", "Nome", "Curso")

        tabela = ttk.Treeview(
            self.area,
            columns=colunas,
            show="headings",
            height=14
        )

        for coluna in colunas:
            tabela.heading(coluna, text=coluna)
            tabela.column(coluna, width=180, anchor="center")

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                alunos.id,
                alunos.nome,
                IFNULL(cursos.nome, 'Sem curso')
            FROM alunos
            LEFT JOIN cursos ON cursos.id = alunos.curso_id
            ORDER BY alunos.nome
        """)

        for linha in cursor.fetchall():
            tabela.insert("", "end", values=linha)

        conn.close()

        tabela.pack(pady=20, padx=20, fill="both")

    def mostrar_notas(self):
        self.limpar_area()

        ctk.CTkLabel(
            self.area,
            text="Lançar Notas",
            font=("Arial", 28, "bold")
        ).pack(pady=15)

        form = ctk.CTkFrame(self.area)
        form.pack(pady=10, padx=30, fill="x")

        self.alunos = self.buscar_alunos()
        self.disciplinas = self.buscar_disciplinas()

        self.dict_alunos = {
            f"{id} - {nome}": id
            for id, nome in self.alunos
        }

        self.dict_disciplinas = {
            f"{id} - {nome}": id
            for id, nome in self.disciplinas
        }

        ctk.CTkLabel(form, text="Aluno").pack(anchor="w", padx=20, pady=(15, 0))

        self.combo_aluno = ctk.CTkComboBox(
            form,
            values=list(self.dict_alunos.keys()) if self.dict_alunos else ["Nenhum aluno cadastrado"]
        )
        self.combo_aluno.pack(pady=8, padx=20, fill="x")

        ctk.CTkLabel(form, text="Disciplina").pack(anchor="w", padx=20, pady=(10, 0))

        self.combo_disciplina = ctk.CTkComboBox(
            form,
            values=list(self.dict_disciplinas.keys()) if self.dict_disciplinas else ["Nenhuma disciplina cadastrada"]
        )
        self.combo_disciplina.pack(pady=8, padx=20, fill="x")

        self.entry_nota1 = ctk.CTkEntry(form, placeholder_text="Nota 1")
        self.entry_nota1.pack(pady=8, padx=20, fill="x")

        self.entry_nota2 = ctk.CTkEntry(form, placeholder_text="Nota 2")
        self.entry_nota2.pack(pady=8, padx=20, fill="x")

        ctk.CTkButton(
            form,
            text="Salvar Nota",
            command=self.salvar_nota
        ).pack(pady=15)

        self.label_resultado = ctk.CTkLabel(
            self.area,
            text="",
            font=("Arial", 15)
        )
        self.label_resultado.pack(pady=5)

        self.criar_tabela_notas()

    def criar_tabela_notas(self):
        colunas = ("Aluno", "Disciplina", "Nota 1", "Nota 2", "Média", "Situação")

        self.tabela_notas = ttk.Treeview(
            self.area,
            columns=colunas,
            show="headings",
            height=8
        )

        for coluna in colunas:
            self.tabela_notas.heading(coluna, text=coluna)
            self.tabela_notas.column(coluna, width=120, anchor="center")

        self.tabela_notas.pack(padx=20, pady=10, fill="both")

        self.carregar_notas()

    def salvar_nota(self):
        aluno_texto = self.combo_aluno.get()
        disciplina_texto = self.combo_disciplina.get()

        if aluno_texto not in self.dict_alunos:
            messagebox.showwarning("Aviso", "Selecione um aluno válido.")
            return

        if disciplina_texto not in self.dict_disciplinas:
            messagebox.showwarning("Aviso", "Selecione uma disciplina válida.")
            return

        try:
            nota1 = float(self.entry_nota1.get().replace(",", "."))
            nota2 = float(self.entry_nota2.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Digite notas válidas.")
            return

        if nota1 < 0 or nota1 > 10 or nota2 < 0 or nota2 > 10:
            messagebox.showwarning("Aviso", "As notas devem ser entre 0 e 10.")
            return

        media = (nota1 + nota2) / 2

        aluno_id = self.dict_alunos[aluno_texto]
        disciplina_id = self.dict_disciplinas[disciplina_texto]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO notas(aluno_id, disciplina_id, nota1, nota2, media)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(aluno_id, disciplina_id)
            DO UPDATE SET
                nota1 = excluded.nota1,
                nota2 = excluded.nota2,
                media = excluded.media
        """, (aluno_id, disciplina_id, nota1, nota2, media))

        conn.commit()
        conn.close()

        situacao = "Aprovado" if media >= 6 else "Reprovado"

        self.label_resultado.configure(
            text=f"Nota salva com sucesso | Média: {media:.2f} | {situacao}"
        )

        self.entry_nota1.delete(0, "end")
        self.entry_nota2.delete(0, "end")

        self.carregar_notas()

    def carregar_notas(self):
        for item in self.tabela_notas.get_children():
            self.tabela_notas.delete(item)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                alunos.nome,
                disciplinas.nome,
                notas.nota1,
                notas.nota2,
                notas.media
            FROM notas
            INNER JOIN alunos ON alunos.id = notas.aluno_id
            INNER JOIN disciplinas ON disciplinas.id = notas.disciplina_id
            ORDER BY alunos.nome
        """)

        for aluno, disciplina, nota1, nota2, media in cursor.fetchall():
            situacao = "Aprovado" if media >= 6 else "Reprovado"

            self.tabela_notas.insert(
                "",
                "end",
                values=(
                    aluno,
                    disciplina,
                    f"{nota1:.2f}",
                    f"{nota2:.2f}",
                    f"{media:.2f}",
                    situacao
                )
            )

        conn.close()

    # ==========================
    # TAREFAS PDF
    # ==========================

    def mostrar_tarefas_pdf(self):
        self.limpar_area()
        self.pdf_selecionado = None

        ctk.CTkLabel(
            self.area,
            text="Tarefas PDF",
            font=("Arial", 28, "bold")
        ).pack(pady=15)

        form = ctk.CTkFrame(self.area)
        form.pack(padx=20, pady=10, fill="x")

        self.disciplinas = self.buscar_disciplinas()

        self.dict_disciplinas_tarefa = {
            f"{id} - {nome}": id
            for id, nome in self.disciplinas
        }

        ctk.CTkLabel(form, text="Disciplina").pack(anchor="w", padx=20, pady=(10, 0))

        self.combo_disciplina_tarefa = ctk.CTkComboBox(
            form,
            values=list(self.dict_disciplinas_tarefa.keys()) if self.dict_disciplinas_tarefa else ["Nenhuma disciplina cadastrada"]
        )
        self.combo_disciplina_tarefa.pack(padx=20, pady=5, fill="x")

        self.entry_titulo_tarefa = ctk.CTkEntry(
            form,
            placeholder_text="Título da tarefa"
        )
        self.entry_titulo_tarefa.pack(padx=20, pady=8, fill="x")

        self.entry_descricao_tarefa = ctk.CTkEntry(
            form,
            placeholder_text="Descrição da tarefa"
        )
        self.entry_descricao_tarefa.pack(padx=20, pady=8, fill="x")

        self.entry_data_entrega = ctk.CTkEntry(
            form,
            placeholder_text="Data de entrega. Ex: 30/05/2026"
        )
        self.entry_data_entrega.pack(padx=20, pady=8, fill="x")

        self.label_pdf = ctk.CTkLabel(
            form,
            text="Nenhum PDF selecionado",
            font=("Arial", 13)
        )
        self.label_pdf.pack(padx=20, pady=5)

        ctk.CTkButton(
            form,
            text="Selecionar PDF",
            command=self.selecionar_pdf_tarefa
        ).pack(padx=20, pady=5)

        ctk.CTkButton(
            form,
            text="Salvar Tarefa PDF",
            command=self.salvar_tarefa_pdf,
            fg_color="green"
        ).pack(padx=20, pady=10)

        self.criar_tabela_tarefas_pdf()
        self.criar_tabela_entregas_pdf()

    def selecionar_pdf_tarefa(self):
        arquivo = filedialog.askopenfilename(
            title="Selecionar PDF",
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

        self.pdf_selecionado = arquivo
        self.label_pdf.configure(text=os.path.basename(arquivo))

    def salvar_tarefa_pdf(self):
        disciplina_texto = self.combo_disciplina_tarefa.get()
        titulo = self.entry_titulo_tarefa.get().strip()
        descricao = self.entry_descricao_tarefa.get().strip()
        data_entrega = self.entry_data_entrega.get().strip()

        if disciplina_texto not in self.dict_disciplinas_tarefa:
            messagebox.showwarning("Aviso", "Selecione uma disciplina válida.")
            return

        if not titulo:
            messagebox.showwarning("Aviso", "Digite o título da tarefa.")
            return

        if not self.pdf_selecionado:
            messagebox.showwarning("Aviso", "Selecione um PDF.")
            return

        disciplina_id = self.dict_disciplinas_tarefa[disciplina_texto]

        nome_original = os.path.basename(self.pdf_selecionado)
        nome_seguro = nome_original.replace(" ", "_")
        nome_final = f"{int(time.time())}_{nome_seguro}"

        destino = os.path.join(PASTA_TAREFAS, nome_final)

        try:
            shutil.copy2(self.pdf_selecionado, destino)

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO tarefas_pdf
                (disciplina_id, titulo, descricao, data_entrega, arquivo_pdf)
                VALUES (?, ?, ?, ?, ?)
            """, (
                disciplina_id,
                titulo,
                descricao,
                data_entrega,
                destino
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Tarefa PDF cadastrada com sucesso.")

            self.entry_titulo_tarefa.delete(0, "end")
            self.entry_descricao_tarefa.delete(0, "end")
            self.entry_data_entrega.delete(0, "end")
            self.pdf_selecionado = None
            self.label_pdf.configure(text="Nenhum PDF selecionado")

            self.carregar_tarefas_pdf()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar tarefa:\n{e}")

    def criar_tabela_tarefas_pdf(self):
        ctk.CTkLabel(
            self.area,
            text="Tarefas cadastradas",
            font=("Arial", 18, "bold")
        ).pack(pady=(10, 5))

        colunas = ("ID", "Disciplina", "Título", "Entrega", "Arquivo")

        self.tabela_tarefas = ttk.Treeview(
            self.area,
            columns=colunas,
            show="headings",
            height=5
        )

        for coluna in colunas:
            self.tabela_tarefas.heading(coluna, text=coluna)
            self.tabela_tarefas.column(coluna, width=130, anchor="center")

        self.tabela_tarefas.pack(padx=20, pady=5, fill="x")

        frame_botoes = ctk.CTkFrame(self.area, fg_color="transparent")
        frame_botoes.pack(pady=5)

        ctk.CTkButton(
            frame_botoes,
            text="Abrir PDF da tarefa",
            command=self.abrir_pdf_tarefa_selecionada
        ).pack(side="left", padx=5)

        self.carregar_tarefas_pdf()

    def carregar_tarefas_pdf(self):
        if not hasattr(self, "tabela_tarefas"):
            return

        for item in self.tabela_tarefas.get_children():
            self.tabela_tarefas.delete(item)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                tarefas_pdf.id,
                disciplinas.nome,
                tarefas_pdf.titulo,
                tarefas_pdf.data_entrega,
                tarefas_pdf.arquivo_pdf
            FROM tarefas_pdf
            INNER JOIN disciplinas
                ON disciplinas.id = tarefas_pdf.disciplina_id
            ORDER BY tarefas_pdf.id DESC
        """)

        self.caminhos_tarefas = {}

        for tarefa_id, disciplina, titulo, data_entrega, arquivo_pdf in cursor.fetchall():
            self.caminhos_tarefas[str(tarefa_id)] = arquivo_pdf

            self.tabela_tarefas.insert(
                "",
                "end",
                values=(
                    tarefa_id,
                    disciplina,
                    titulo,
                    data_entrega if data_entrega else "-",
                    os.path.basename(arquivo_pdf)
                )
            )

        conn.close()

    def abrir_pdf_tarefa_selecionada(self):
        item = self.tabela_tarefas.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione uma tarefa.")
            return

        valores = self.tabela_tarefas.item(item, "values")
        tarefa_id = str(valores[0])

        caminho = self.caminhos_tarefas.get(tarefa_id)
        self.abrir_arquivo(caminho)

    def criar_tabela_entregas_pdf(self):
        ctk.CTkLabel(
            self.area,
            text="Entregas dos alunos",
            font=("Arial", 18, "bold")
        ).pack(pady=(10, 5))

        colunas = ("Aluno", "Tarefa", "Disciplina", "Data envio", "Arquivo")

        self.tabela_entregas = ttk.Treeview(
            self.area,
            columns=colunas,
            show="headings",
            height=5
        )

        for coluna in colunas:
            self.tabela_entregas.heading(coluna, text=coluna)
            self.tabela_entregas.column(coluna, width=130, anchor="center")

        self.tabela_entregas.pack(padx=20, pady=5, fill="x")

        ctk.CTkButton(
            self.area,
            text="Abrir entrega selecionada",
            command=self.abrir_entrega_selecionada
        ).pack(pady=5)

        self.carregar_entregas_pdf()

    def carregar_entregas_pdf(self):
        if not hasattr(self, "tabela_entregas"):
            return

        for item in self.tabela_entregas.get_children():
            self.tabela_entregas.delete(item)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                alunos.nome,
                tarefas_pdf.titulo,
                disciplinas.nome,
                entregas_pdf.data_envio,
                entregas_pdf.arquivo_pdf
            FROM entregas_pdf
            INNER JOIN alunos
                ON alunos.id = entregas_pdf.aluno_id
            INNER JOIN tarefas_pdf
                ON tarefas_pdf.id = entregas_pdf.tarefa_id
            INNER JOIN disciplinas
                ON disciplinas.id = tarefas_pdf.disciplina_id
            ORDER BY entregas_pdf.data_envio DESC
        """)

        self.caminhos_entregas = {}

        for i, (aluno, tarefa, disciplina, data_envio, arquivo_pdf) in enumerate(cursor.fetchall()):
            self.caminhos_entregas[str(i)] = arquivo_pdf

            self.tabela_entregas.insert(
                "",
                "end",
                iid=str(i),
                values=(
                    aluno,
                    tarefa,
                    disciplina,
                    data_envio,
                    os.path.basename(arquivo_pdf)
                )
            )

        conn.close()

    def abrir_entrega_selecionada(self):
        item = self.tabela_entregas.focus()

        if not item:
            messagebox.showwarning("Aviso", "Selecione uma entrega.")
            return

        caminho = self.caminhos_entregas.get(str(item))
        self.abrir_arquivo(caminho)


if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()

    tela = TelaProfessor(app, nome_professor="Carlos")
    app.mainloop()