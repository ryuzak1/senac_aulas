import tkinter as tk

# --- SEGUNDA TELA (NORMAL COM tk.Tk) ---
class SegundaTela(tk.Tk):
    def __init__(self, informacao):
        super().__init__()
        self.title("Segunda Tela")
        self.geometry("300x200")
        
        # Recebe e exibe a informação passada da primeira tela
        texto_exibicao = f"Informação recebida:\n{informacao}"
        self.label = tk.Label(self, text=texto_exibicao, font=("Arial", 12))
        self.label.pack(pady=30, fill='x')
        
        # Botão para voltar para a tela principal
        self.btn_voltar = tk.Button(self, text="Voltar", command=self.voltar)
        self.btn_voltar.pack(pady=10)

    def voltar(self):
        self.destroy()
        app = TelaPrincipal()
        app.mainloop()


# --- PRIMEIRA TELA (PRINCIPAL COM tk.Tk) ---
class TelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tela Principal")
        self.geometry("300x200")
        
        # Campo de entrada de texto
        self.label_instrucao = tk.Label(self, text="Digite algo para enviar:")
        self.label_instrucao.pack(pady=10)
        
        self.entrada_dados = tk.Entry(self, width=25)
        self.entrada_dados.pack(pady=5)
        
        # Botão para acionar o envio
        self.btn_enviar = tk.Button(self, text="Enviar para próxima tela", command=self.abrir_proxima_tela)
        self.btn_enviar.pack(pady=20)
        
    def abrir_proxima_tela(self):
        # 1. Pega o texto atual do campo de entrada
        dado_para_passar = self.entrada_dados.get()
        
        # 2. Fecha a primeira tela
        self.destroy()
        
        # 3. Abre a segunda tela como janela normal
        app2 = SegundaTela(informacao=dado_para_passar)
        app2.mainloop()


# --- EXECUÇÃO DO APP ---
if __name__ == "__main__":
    app = TelaPrincipal()
    app.mainloop()
