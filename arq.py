from pathlib import Path
import tkinter as tk

def mostrar_conteudo():
    caminho = Path(__file__).with_name("text.txt")
    try:
        print(caminho.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("Arquivo text.txt não encontrado.")

# 1. Cria a janela principal
app = tk.Tk()
app.title("Aplicação Tkinter")
app.geometry("300x150")

# 2. Cria o rótulo de texto
label = tk.Label(app, text="Olá, Mundo!", font=("Arial", 12))
label.pack(pady=10)

# 3. Cria o botão
botao = tk.Button(app, text="Clique Aqui", command=mostrar_conteudo)
botao.pack(pady=5)

# 4. Inicia o loop da aplicação
app.mainloop()
