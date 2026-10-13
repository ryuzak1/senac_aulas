class Produto:
    def __init__(self, nome: str, preco: float):
        self.nome = nome
        self.preco = preco


class Carrinho:
    def __init__(self):
        self.produtos = []

    def adicionar(self, produto: Produto):
        self.produtos.append(produto)

    def remover(self, produto: Produto):
        if produto in self.produtos:
            self.produtos.remove(produto)

    def listar_produtos(self):
        if not self.produtos:
            print("O carrinho está vazio.")
            return
        for p in self.produtos:
            print(f"Produto: {p.nome} | Preço: R$ {p.preco:.2f}")

    def calcular_total(self) -> float:
        return sum(p.preco for p in self.produtos)


if __name__ == "__main__":
    # Exemplo de teste das classes
    p1 = Produto("Arroz", 25.50)
    p2 = Produto("Feijão", 8.90)
    p3 = Produto("Macarrão", 4.20)

    carrinho = Carrinho()
    carrinho.adicionar(p1)
    carrinho.adicionar(p2)
    carrinho.adicionar(p3)

    print("--- Itens no Carrinho ---")
    carrinho.listar_produtos()
    print(f"Total: R$ {carrinho.calcular_total():.2f}\n")

    print(f"Removendo {p2.nome}...")
    carrinho.remover(p2)

    print("\n--- Itens Atualizados ---")
    carrinho.listar_produtos()
    print(f"Total: R$ {carrinho.calcular_total():.2f}")
