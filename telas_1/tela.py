import tkinter as tk
from tkinter import ttk, messagebox
from banco import salvar_nome, listar_nomes

def cadastrar():
    nome = entry_nome.get().strip()

    if not nome:
        messagebox.showwarning("Aviso", "Por favor, digite um nome!")
        return

    try:
        salvar_nome(nome)
        messagebox.showinfo("Sucesso", "Nome salvo com sucesso!")
        entry_nome.delete(0, tk.END)
        atualizar_tabela()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}")

def pesquisar():
    termo = entry_pesquisa.get().strip()
    atualizar_tabela(termo)

def limpar_pesquisa():
    entry_pesquisa.delete(0, tk.END)
    atualizar_tabela()

def atualizar_tabela(pesquisa=""):
    for item in tree.get_children():
        tree.delete(item)
    registros = listar_nomes(pesquisa)
    for reg in registros:
        tree.insert("", tk.END, values=(reg.id, reg.nome))

# Janela principal
janela = tk.Tk()
janela.title("Cadastro Simples")
janela.geometry("400x460")

# Texto de instrução
label_instrucao = tk.Label(janela, text="Digite o Nome:")
label_instrucao.pack(pady=(15, 5))

# Campo de entrada
entry_nome = tk.Entry(janela, width=28)
entry_nome.pack(pady=5)

# Botão para salvar
btn_salvar = tk.Button(janela, text="Salvar", width=12, command=cadastrar)
btn_salvar.pack(pady=10)

# --- PARTE DA LISTAGEM E PESQUISA (ADICIONADA AO FINAL) ---

# Campo e botões de pesquisa
frame_pesquisa = tk.Frame(janela)
frame_pesquisa.pack(pady=10)

entry_pesquisa = tk.Entry(frame_pesquisa, width=18)
entry_pesquisa.pack(side="left", padx=5)

btn_pesquisar = tk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar)
btn_pesquisar.pack(side="left", padx=2)

btn_todos = tk.Button(frame_pesquisa, text="Ver Todos", command=limpar_pesquisa)
btn_todos.pack(side="left", padx=2)

# Tabela para listar os alunos
colunas = ("id", "nome")
tree = ttk.Treeview(janela, columns=colunas, show="headings", height=8)
tree.heading("id", text="ID")
tree.heading("nome", text="Nome")
tree.column("id", width=50, anchor="center")
tree.column("nome", width=260)
tree.pack(padx=20, pady=5, fill="both", expand=True)

# Carrega os dados na inicialização
try:
    atualizar_tabela()
except Exception as e:
    print(f"Erro ao carregar dados: {e}")

janela.mainloop()
