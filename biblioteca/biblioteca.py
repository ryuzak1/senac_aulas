class Biblioteca:
    def __init__(self, nome):
        self.nome = nome
        self.livros = []

    def cadastrar_livro(self, livro):
        self.livros.append(livro)
        print(f"Livro '{livro.titulo}' cadastrado com sucesso.")

    def listar_livros(self):
        if not self.livros:
            print("Nenhum livro cadastrado na biblioteca.")
            return
        print(f"--- Livros da {self.nome} ---")
        for livro in self.livros:
            if livro.disponivel:
                status = "Disponivel"
            else:
                status = "Emprestado"
            print(f"- {livro.titulo} ({livro.autor}) | {status}")

    def emprestar_livro(self, livro, aluno):
        if livro not in self.livros:
            print(f"O livro '{livro.titulo}' nao pertence a esta biblioteca.")
            return
        if not livro.disponivel:
            print(f"O livro '{livro.titulo}' ja esta emprestado.")
            return
        livro.disponivel = False
        aluno.pegar_livro(livro)
        print(f"Livro '{livro.titulo}' emprestado para {aluno.nome}.")

    def devolver_livro(self, livro, aluno):
        if livro not in aluno.livros_emprestados:
            print(f"{aluno.nome} nao possui o livro '{livro.titulo}' emprestado.")
            return
        livro.disponivel = True
        aluno.devolver_livro(livro)
        print(f"Livro '{livro.titulo}' devolvido por {aluno.nome}.")
