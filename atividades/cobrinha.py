import tkinter as tk
import random

# Configurações do jogo
LARGURA = 400
ALTURA = 400
TAMANHO_BLOCO = 20
VELOCIDADE = 120  # Milissegundos entre cada movimento da cobra

# Variáveis globais do jogo
cobra = [(100, 100), (80, 100), (60, 100)]
direcao = "Right"
comida = (0, 0)
pontos = 0
jogo_ativo = True

def gerar_comida():
    global comida
    # Gera coordenadas alinhadas à grade de 20 em 20 pixels
    x = random.randint(0, (LARGURA // TAMANHO_BLOCO) - 1) * TAMANHO_BLOCO
    y = random.randint(0, (ALTURA // TAMANHO_BLOCO) - 1) * TAMANHO_BLOCO
    comida = (x, y)

def mudar_direcao(event):
    global direcao
    tecla = event.keysym

    # Impede que a cobra dê ré nela mesma
    if tecla == "Up" and direcao != "Down":
        direcao = "Up"
    elif tecla == "Down" and direcao != "Up":
        direcao = "Down"
    elif tecla == "Left" and direcao != "Right":
        direcao = "Left"
    elif tecla == "Right" and direcao != "Left":
        direcao = "Right"

def mover():
    global cobra, pontos, jogo_ativo

    if not jogo_ativo:
        return

    # Pega a posição atual da cabeça
    cabeca_x, cabeca_y = cobra[0]

    # Atualiza a posição com base na direção atual
    if direcao == "Up":
        cabeca_y -= TAMANHO_BLOCO
    elif direcao == "Down":
        cabeca_y += TAMANHO_BLOCO
    elif direcao == "Left":
        cabeca_x -= TAMANHO_BLOCO
    elif direcao == "Right":
        cabeca_x += TAMANHO_BLOCO

    nova_cabeca = (cabeca_x, cabeca_y)

    # 1. Colisão com as bordas da tela
    if cabeca_x < 0 or cabeca_x >= LARGURA or cabeca_y < 0 or cabeca_y >= ALTURA:
        fim_de_jogo()
        return

    # 2. Colisão com o próprio corpo
    if nova_cabeca in cobra:
        fim_de_jogo()
        return

    # Adiciona a nova cabeça na frente
    cobra.insert(0, nova_cabeca)

    # 3. Verifica se pegou a comida
    if nova_cabeca == comida:
        pontos += 1
        gerar_comida()
    else:
        # Remove o último pedaço do rabo se não comeu
        cobra.pop()

    # Redesenha os elementos na tela
    desenhar()

    # Agenda a próxima movimentação
    janela.after(VELOCIDADE, mover)

def desenhar():
    # Limpa a tela antes de desenhar o novo quadro
    canvas.delete("all")

    # Desenha a comida (quadrado vermelho)
    cx, cy = comida
    canvas.create_rectangle(
        cx, cy, cx + TAMANHO_BLOCO, cy + TAMANHO_BLOCO,
        fill="red"
    )

    # Desenha os pedaços da cobra (quadrados verdes)
    for x, y in cobra:
        canvas.create_rectangle(
            x, y, x + TAMANHO_BLOCO, y + TAMANHO_BLOCO,
            fill="green"
        )

    # Desenha a pontuação no topo esquerdo
    canvas.create_text(
        50, 15,
        text=f"Pontos: {pontos}",
        fill="white",
        font=("Arial", 12)
    )

def fim_de_jogo():
    global jogo_ativo
    jogo_ativo = False
    canvas.create_text(
        LARGURA // 2, ALTURA // 2,
        text="FIM DE JOGO!",
        fill="white",
        font=("Arial", 22, "bold")
    )

# 1. Criação da janela principal
janela = tk.Tk()
janela.title("Jogo da Cobrinha")
janela.resizable(False, False)

# 2. Criação do Canvas onde o jogo é desenhado
canvas = tk.Canvas(janela, width=LARGURA, height=ALTURA, bg="black")
canvas.pack()

# 3. Configuração dos controles do teclado (setas direcionais)
janela.bind("<Up>", mudar_direcao)
janela.bind("<Down>", mudar_direcao)
janela.bind("<Left>", mudar_direcao)
janela.bind("<Right>", mudar_direcao)

# 4. Inicia o jogo
gerar_comida()
desenhar()
janela.after(VELOCIDADE, mover)

# 5. Inicia o loop da aplicação
janela.mainloop()
