import tkinter as tk
from tkinter import ttk, messagebox
from banco import salvar_nome, listar_nomes, excluir_nome

def cadastrar():
    nome = entry_nome.get().strip()
    telefone = entry_telefone.get().strip()

    if not nome or not telefone:
        messagebox.showwarning("Aviso", "Por favor, preencha o nome e o telefone!")
        return

    if not telefone.isdigit():
        messagebox.showwarning("Aviso", "O telefone deve conter apenas números!")
        return

    try:
        salvar_nome(nome, telefone)
        messagebox.showinfo("Sucesso", "Salvo com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        atualizar_tabela()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}")

def pesquisar():
    termo = entry_pesquisa.get().strip()
    atualizar_tabela(termo)

def limpar_pesquisa():
    entry_pesquisa.delete(0, tk.END)
    atualizar_tabela()

def excluir():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um registro na tabela para excluir!")
        return

    item = tree.item(selecionado)
    registro_id = item["values"][0]
    registro_nome = item["values"][1]

    if messagebox.askyesno("Confirmar", f"Deseja realmente excluir '{registro_nome}' (ID: {registro_id})?"):
        try:
            excluir_nome(registro_id)
            messagebox.showinfo("Sucesso", "Registro excluído com sucesso!")
            atualizar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")

def atualizar_tabela(pesquisa=""):
    for item in tree.get_children():
        tree.delete(item)
    registros = listar_nomes(pesquisa)
    for reg in registros:
        tree.insert("", tk.END, values=(reg.id, reg.nome, reg.telefone))

# Janela principal
janela = tk.Tk()
janela.title("Cadastro Simples")
janela.geometry("450x570")

# Campo Nome
label_nome = tk.Label(janela, text="Digite o Nome:")
label_nome.pack(pady=(10, 2))

entry_nome = tk.Entry(janela, width=30)
entry_nome.pack(pady=2)

# Campo Telefone
label_telefone = tk.Label(janela, text="Digite o Telefone:")
label_telefone.pack(pady=(5, 2))

entry_telefone = tk.Entry(janela, width=30)
entry_telefone.pack(pady=2)

# Botão para salvar
btn_salvar = tk.Button(janela, text="Salvar", width=12, command=cadastrar)
btn_salvar.pack(pady=10)

# --- PARTE DA LISTAGEM E PESQUISA ---

# Campo e botões de pesquisa
frame_pesquisa = tk.Frame(janela)
frame_pesquisa.pack(pady=10)

entry_pesquisa = tk.Entry(frame_pesquisa, width=20)
entry_pesquisa.pack(side="left", padx=5)

btn_pesquisar = tk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar)
btn_pesquisar.pack(side="left", padx=2)

btn_todos = tk.Button(frame_pesquisa, text="Ver Todos", command=limpar_pesquisa)
btn_todos.pack(side="left", padx=2)

# Tabela para listar os registros
colunas = ("id", "nome", "telefone")
tree = ttk.Treeview(janela, columns=colunas, show="headings", height=8)
tree.heading("id", text="ID")
tree.heading("nome", text="Nome")
tree.heading("telefone", text="Telefone")

tree.column("id", width=40, anchor="center")
tree.column("nome", width=200)
tree.column("telefone", width=120, anchor="center")
tree.pack(padx=20, pady=5, fill="both", expand=True)

# Botão para excluir registro selecionado
btn_excluir = tk.Button(janela, text="Excluir Selecionado", bg="#ffcccc", command=excluir)
btn_excluir.pack(pady=10)

# Carrega os dados na inicialização
try:
    atualizar_tabela()
except Exception as e:
    print(f"Erro ao carregar dados: {e}")

janela.mainloop()
