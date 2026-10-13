import tkinter as tk

# Funções da calculadora
def clicar(valor):
    # Adiciona o número ou operador no visor
    visor.insert(tk.END, valor)

def limpar():
    # Limpa o visor
    visor.delete(0, tk.END)

def calcular():
    try:
        # Avalia a expressão matemática digitada no visor
        resultado = eval(visor.get())
        limpar()
        visor.insert(tk.END, str(resultado))
    except Exception:
        limpar()
        visor.insert(tk.END, "Erro")

# 1. Cria a janela principal
janela = tk.Tk()
janela.title("Calculadora")
janela.resizable(False, False)

# 2. Campo de texto (Visor) para mostrar o que foi digitado
visor = tk.Entry(janela, font=("Arial", 20), justify="right", bd=10)
visor.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# 3. Lista de botões com suas posições (texto, linha, coluna)
botoes = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3)
]

# 4. Criação dos botões na janela
for texto, linha, coluna in botoes:
    if texto == "=":
        comando = calcular
    elif texto == "C":
        comando = limpar
    else:
        comando = lambda t=texto: clicar(t)

    botao = tk.Button(janela, text=texto, width=5, height=2, font=("Arial", 14), command=comando)
    botao.grid(row=linha, column=coluna, padx=5, pady=5)

# 5. Inicia o loop da aplicação
janela.mainloop()
