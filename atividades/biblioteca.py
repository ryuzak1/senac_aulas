import tkinter as tk
from tkinter import ttk, messagebox


# ==============================================================================
# 1. ESTRUTURA DE CLASSES DO MODELO
# ==============================================================================

class Livro:
    def __init__(self, id_livro, titulo, autor):
        self.id = id_livro
        self.titulo = titulo
        self.autor = autor
        self.disponivel = True

    def emprestar(self):
        if self.disponivel:
            self.disponivel = False
            return True
        return False

    def devolver(self):
        self.disponivel = True


class Aluno:
    def __init__(self, matricula, nome):
        self.matricula = matricula
        self.nome = nome
        self.livros_emprestados = []

    def pegar_emprestado(self, livro):
        self.livros_emprestados.append(livro)

    def devolver_livro(self, livro):
        if livro in self.livros_emprestados:
            self.livros_emprestados.remove(livro)
            return True
        return False


class Biblioteca:
    def __init__(self):
        self.livros = []
        self.alunos = []
        self._contador_livro = 1

    def cadastrar_livro(self, titulo, autor):
        livro = Livro(self._contador_livro, titulo, autor)
        self.livros.append(livro)
        self._contador_livro += 1
        return livro

    def cadastrar_aluno(self, matricula, nome):
        if self.buscar_aluno(matricula):
            return None  # Já existe aluno com esta matrícula
        aluno = Aluno(matricula, nome)
        self.alunos.append(aluno)
        return aluno

    def buscar_livro(self, id_livro):
        for livro in self.livros:
            if livro.id == id_livro:
                return livro
        return None

    def buscar_aluno(self, matricula):
        for aluno in self.alunos:
            if aluno.matricula == matricula:
                return aluno
        return None

    def emprestar_livro(self, matricula, id_livro):
        aluno = self.buscar_aluno(matricula)
        livro = self.buscar_livro(id_livro)

        if not aluno:
            return False, "Aluno não encontrado!"
        if not livro:
            return False, "Livro não encontrado!"
        if not livro.disponivel:
            return False, f"O livro '{livro.titulo}' já está Indisponível!"

        livro.emprestar()
        aluno.pegar_emprestado(livro)
        return True, f"Livro '{livro.titulo}' emprestado para {aluno.nome} com sucesso!"

    def devolver_livro(self, matricula, id_livro):
        aluno = self.buscar_aluno(matricula)
        livro = self.buscar_livro(id_livro)

        if not aluno:
            return False, "Aluno não encontrado!"
        if not livro:
            return False, "Livro não encontrado!"
        if livro not in aluno.livros_emprestados:
            return False, f"O livro '{livro.titulo}' não está vinculado a este aluno!"

        livro.devolver()
        aluno.devolver_livro(livro)
        return True, f"Livro '{livro.titulo}' devolvido com sucesso!"


# ==============================================================================
# 2. INTERFACE GRÁFICA COM TKINTER
# ==============================================================================

class SistemaBibliotecaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de Biblioteca")
        self.geometry("760x560")
        self.resizable(False, False)

        # Instância da Biblioteca
        self.biblioteca = Biblioteca()
        self._carregar_dados_iniciais()

        # Configuração das Abas (ttk.Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Telas/Abas
        self.aba_acervo = ttk.Frame(self.notebook)
        self.aba_alunos = ttk.Frame(self.notebook)
        self.aba_emprestimos = ttk.Frame(self.notebook)

        self.notebook.add(self.aba_acervo, text="📚 Acervo de Livros")
        self.notebook.add(self.aba_alunos, text="👥 Alunos")
        self.notebook.add(self.aba_emprestimos, text="🔄 Empréstimos & Devoluções")

        # Construção do layout de cada aba
        self._criar_tela_acervo()
        self._criar_tela_alunos()
        self._criar_tela_emprestimos()

        # Atualiza todas as tabelas e opções
        self.atualizar_tudo()

    def _carregar_dados_iniciais(self):
        """Cadastra alguns dados de exemplo para facilitar o teste imediato."""
        self.biblioteca.cadastrar_livro("Dom Casmurro", "Machado de Assis")
        self.biblioteca.cadastrar_livro("1984", "George Orwell")
        self.biblioteca.cadastrar_livro("O Pequeno Príncipe", "Antoine de Saint-Exupéry")
        self.biblioteca.cadastrar_aluno("101", "Lucas Silva")
        self.biblioteca.cadastrar_aluno("102", "Mariana Costa")

    # --------------------------------------------------------------------------
    # ABA 1: ACERVO DE LIVROS
    # --------------------------------------------------------------------------
    def _criar_tela_acervo(self):
        # Formulário de Cadastro de Livro
        form_frame = ttk.LabelFrame(self.aba_acervo, text="Cadastrar Novo Livro")
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_titulo = ttk.Entry(form_frame, width=35)
        self.ent_titulo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Autor:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_autor = ttk.Entry(form_frame, width=25)
        self.ent_autor.grid(row=0, column=3, padx=5, pady=5)

        btn_cad_livro = ttk.Button(form_frame, text="Salvar Livro", command=self.salvar_livro)
        btn_cad_livro.grid(row=0, column=4, padx=10, pady=5)

        # Listagem do Acervo
        lista_frame = ttk.LabelFrame(self.aba_acervo, text="Livros no Acervo")
        lista_frame.pack(fill="both", expand=True, padx=10, pady=5)

        colunas = ("id", "titulo", "autor", "status")
        self.tree_livros = ttk.Treeview(lista_frame, columns=colunas, show="headings", height=14)
        self.tree_livros.heading("id", text="ID")
        self.tree_livros.heading("titulo", text="Título")
        self.tree_livros.heading("autor", text="Autor")
        self.tree_livros.heading("status", text="Status")

        self.tree_livros.column("id", width=50, anchor="center")
        self.tree_livros.column("titulo", width=320)
        self.tree_livros.column("autor", width=200)
        self.tree_livros.column("status", width=120, anchor="center")

        # Scrollbar
        scroll = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree_livros.yview)
        self.tree_livros.configure(yscrollcommand=scroll.set)
        self.tree_livros.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        scroll.pack(side="right", fill="y", pady=5)

    def salvar_livro(self):
        titulo = self.ent_titulo.get().strip()
        autor = self.ent_autor.get().strip()

        if not titulo or not autor:
            messagebox.showwarning("Aviso", "Preencha o título e o autor do livro!")
            return

        self.biblioteca.cadastrar_livro(titulo, autor)
        self.ent_titulo.delete(0, tk.END)
        self.ent_autor.delete(0, tk.END)
        self.atualizar_tudo()
        messagebox.showinfo("Sucesso", f"Livro '{titulo}' cadastrado com sucesso!")

    # --------------------------------------------------------------------------
    # ABA 2: ALUNOS
    # --------------------------------------------------------------------------
    def _criar_tela_alunos(self):
        # Formulário de Cadastro de Aluno
        form_frame = ttk.LabelFrame(self.aba_alunos, text="Cadastrar Novo Aluno")
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Matrícula:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_matricula = ttk.Entry(form_frame, width=20)
        self.ent_matricula.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Nome:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_nome_aluno = ttk.Entry(form_frame, width=35)
        self.ent_nome_aluno.grid(row=0, column=3, padx=5, pady=5)

        btn_cad_aluno = ttk.Button(form_frame, text="Salvar Aluno", command=self.salvar_aluno)
        btn_cad_aluno.grid(row=0, column=4, padx=10, pady=5)

        # Listagem de Alunos
        lista_frame = ttk.LabelFrame(self.aba_alunos, text="Alunos Registrados")
        lista_frame.pack(fill="both", expand=True, padx=10, pady=5)

        colunas = ("matricula", "nome", "livros")
        self.tree_alunos = ttk.Treeview(lista_frame, columns=colunas, show="headings", height=14)
        self.tree_alunos.heading("matricula", text="Matrícula")
        self.tree_alunos.heading("nome", text="Nome")
        self.tree_alunos.heading("livros", text="Livros Emprestados")

        self.tree_alunos.column("matricula", width=100, anchor="center")
        self.tree_alunos.column("nome", width=250)
        self.tree_alunos.column("livros", width=340)

        scroll = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree_alunos.yview)
        self.tree_alunos.configure(yscrollcommand=scroll.set)
        self.tree_alunos.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        scroll.pack(side="right", fill="y", pady=5)

    def salvar_aluno(self):
        matricula = self.ent_matricula.get().strip()
        nome = self.ent_nome_aluno.get().strip()

        if not matricula or not nome:
            messagebox.showwarning("Aviso", "Preencha a matrícula e o nome do aluno!")
            return

        resultado = self.biblioteca.cadastrar_aluno(matricula, nome)
        if resultado is None:
            messagebox.showerror("Erro", f"Já existe um aluno com a matrícula '{matricula}'!")
            return

        self.ent_matricula.delete(0, tk.END)
        self.ent_nome_aluno.delete(0, tk.END)
        self.atualizar_tudo()
        messagebox.showinfo("Sucesso", f"Aluno '{nome}' cadastrado com sucesso!")

    # --------------------------------------------------------------------------
    # ABA 3: FLUXO DE EMPRÉSTIMO, DEVOLUÇÃO & PAINEL DO ALUNO
    # --------------------------------------------------------------------------
    def _criar_tela_emprestimos(self):
        # 1. Seção de Empréstimo
        frame_emp = ttk.LabelFrame(self.aba_emprestimos, text="Realizar Empréstimo")
        frame_emp.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_emp, text="Aluno:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cb_aluno_emp = ttk.Combobox(frame_emp, state="readonly", width=35)
        self.cb_aluno_emp.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_emp, text="Livro (Disponível):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.cb_livro_emp = ttk.Combobox(frame_emp, state="readonly", width=35)
        self.cb_livro_emp.grid(row=0, column=3, padx=5, pady=5)

        btn_emp = ttk.Button(frame_emp, text="Confirmar Empréstimo", command=self.executar_emprestimo)
        btn_emp.grid(row=1, column=1, columnspan=3, pady=8)

        # 2. Seção de Painel do Aluno e Devolução
        frame_dev = ttk.LabelFrame(self.aba_emprestimos, text="Painel do Aluno & Devolução")
        frame_dev.pack(fill="both", expand=True, padx=10, pady=5)

        topo_dev = ttk.Frame(frame_dev)
        topo_dev.pack(fill="x", padx=5, pady=5)

        ttk.Label(topo_dev, text="Selecionar Aluno:").pack(side="left", padx=5)
        self.cb_aluno_dev = ttk.Combobox(topo_dev, state="readonly", width=35)
        self.cb_aluno_dev.pack(side="left", padx=5)
        self.cb_aluno_dev.bind("<<ComboboxSelected>>", lambda e: self.atualizar_painel_aluno_devolucao())

        btn_dev = ttk.Button(topo_dev, text="Devolver Livro Selecionado", command=self.executar_devolucao)
        btn_dev.pack(side="right", padx=10)

        # Lista de Livros com o Aluno selecionado
        colunas_dev = ("id", "titulo", "autor")
        self.tree_livros_aluno = ttk.Treeview(frame_dev, columns=colunas_dev, show="headings", height=8)
        self.tree_livros_aluno.heading("id", text="ID")
        self.tree_livros_aluno.heading("titulo", text="Título do Livro")
        self.tree_livros_aluno.heading("autor", text="Autor")

        self.tree_livros_aluno.column("id", width=50, anchor="center")
        self.tree_livros_aluno.column("titulo", width=380)
        self.tree_livros_aluno.column("autor", width=250)
        self.tree_livros_aluno.pack(fill="both", expand=True, padx=5, pady=5)

    def executar_emprestimo(self):
        sel_aluno = self.cb_aluno_emp.get()
        sel_livro = self.cb_livro_emp.get()

        if not sel_aluno or not sel_livro:
            messagebox.showwarning("Aviso", "Selecione um aluno e um livro para realizar o empréstimo!")
            return

        # Extrai matrícula e ID dos textos selecionados no formato "ID/Matricula - Descrição"
        matricula = sel_aluno.split(" - ")[0]
        id_livro = int(sel_livro.split(" - ")[0])

        sucesso, msg = self.biblioteca.emprestar_livro(matricula, id_livro)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.atualizar_tudo()
        else:
            messagebox.showerror("Atenção", msg)

    def executar_devolucao(self):
        sel_item = self.tree_livros_aluno.selection()
        if not sel_item:
            messagebox.showwarning("Aviso", "Selecione o livro que deseja devolver na tabela abaixo!")
            return

        sel_aluno = self.cb_aluno_dev.get()
        if not sel_aluno:
            messagebox.showwarning("Aviso", "Selecione um aluno!")
            return

        matricula = sel_aluno.split(" - ")[0]
        valores_livro = self.tree_livros_aluno.item(sel_item[0], "values")
        id_livro = int(valores_livro[0])

        sucesso, msg = self.biblioteca.devolver_livro(matricula, id_livro)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.atualizar_tudo()
        else:
            messagebox.showerror("Erro", msg)

    # --------------------------------------------------------------------------
    # MÉTODOS DE ATUALIZAÇÃO DA INTERFACE
    # --------------------------------------------------------------------------
    def atualizar_tudo(self):
        self.atualizar_tabela_acervo()
        self.atualizar_tabela_alunos()
        self.atualizar_comboboxes()
        self.atualizar_painel_aluno_devolucao()

    def atualizar_tabela_acervo(self):
        self.tree_livros.delete(*self.tree_livros.get_children())
        for livro in self.biblioteca.livros:
            status = "Disponível" if livro.disponivel else "Indisponível"
            self.tree_livros.insert("", "end", values=(livro.id, livro.titulo, livro.autor, status))

    def atualizar_tabela_alunos(self):
        self.tree_alunos.delete(*self.tree_alunos.get_children())
        for aluno in self.biblioteca.alunos:
            if aluno.livros_emprestados:
                titulos = ", ".join([livro.titulo for livro in aluno.livros_emprestados])
            else:
                titulos = "(Nenhum livro)"
            self.tree_alunos.insert("", "end", values=(aluno.matricula, aluno.nome, titulos))

    def atualizar_comboboxes(self):
        # Lista formatada de alunos: "101 - Lucas Silva"
        lista_alunos = [f"{a.matricula} - {a.nome}" for a in self.biblioteca.alunos]
        self.cb_aluno_emp["values"] = lista_alunos
        self.cb_aluno_dev["values"] = lista_alunos

        # Lista de livros APENAS disponíveis para novo empréstimo
        livros_disponiveis = [
            f"{l.id} - {l.titulo}" for l in self.biblioteca.livros if l.disponivel
        ]
        self.cb_livro_emp["values"] = livros_disponiveis

        # Mantém seleção válida ou limpa
        if lista_alunos and not self.cb_aluno_emp.get():
            self.cb_aluno_emp.current(0)
        if livros_disponiveis and not self.cb_livro_emp.get():
            self.cb_livro_emp.current(0)
        elif not livros_disponiveis:
            self.cb_livro_emp.set("")

        if lista_alunos and not self.cb_aluno_dev.get():
            self.cb_aluno_dev.current(0)

    def atualizar_painel_aluno_devolucao(self):
        self.tree_livros_aluno.delete(*self.tree_livros_aluno.get_children())
        sel_aluno = self.cb_aluno_dev.get()
        if not sel_aluno:
            return

        matricula = sel_aluno.split(" - ")[0]
        aluno = self.biblioteca.buscar_aluno(matricula)
        if aluno:
            for livro in aluno.livros_emprestados:
                self.tree_livros_aluno.insert("", "end", values=(livro.id, livro.titulo, livro.autor))


# ==============================================================================
# EXECUÇÃO DO PROGRAMA
# ==============================================================================
if __name__ == "__main__":
    app = SistemaBibliotecaApp()
    app.mainloop()
