from livro import Livro
from aluno import Aluno
from biblioteca import Biblioteca


if __name__ == "__main__":
    biblioteca = Biblioteca("Biblioteca SENAC")

    livro1 = Livro("Dom Casmurro", "Machado de Assis")
    livro2 = Livro("O Cortico", "Aluisio Azevedo")
    livro3 = Livro("Capitaes da Areia", "Jorge Amado")

    biblioteca.cadastrar_livro(livro1)
    biblioteca.cadastrar_livro(livro2)
    biblioteca.cadastrar_livro(livro3)

    print()
    biblioteca.listar_livros()

    aluno1 = Aluno("Maria")
    aluno2 = Aluno("Joao")

    print()
    biblioteca.emprestar_livro(livro1, aluno1)
    biblioteca.emprestar_livro(livro2, aluno2)
    biblioteca.emprestar_livro(livro1, aluno2)

    print()
    biblioteca.listar_livros()

    print()
    aluno1.listar_livros()
    aluno2.listar_livros()

    print()
    biblioteca.devolver_livro(livro1, aluno1)

    print()
    biblioteca.listar_livros()

    print()
    aluno1.listar_livros()
