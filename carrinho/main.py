from produto import Produto
from carrinho import Carrinho


if __name__ == "__main__":
    p1 = Produto("Arroz", 25.50)
    p2 = Produto("Feijão", 8.90)
    p3 = Produto("Macarrão", 4.20)

    c = Carrinho()
    carrinho = Carrinho()
    c.adicionar(p1)
    c.adicionar(p2)
    c.adicionar(p3)

    print("--- Itens no Carrinho ---")
    carrinho.listar_produtos()
    print(f"Total: R$ {carrinho.calcular_total():.2f}\n")

    print(f"Removendo {p2.nome}...")
    carrinho.remover(p2)

    print("\n--- Itens Atualizados ---")
    carrinho.listar_produtos()
    print(f"Total: R$ {carrinho.calcular_total():.2f}")
