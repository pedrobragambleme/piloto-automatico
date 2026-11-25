# Configurações centrais do jogo (tela, cores, pista, regras e caminhos de arquivos).

import os

# ---------------------------------------------------------------- Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "Piloto Automático"

# ---------------------------------------------------------------- Cores (RGB)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212, 212, 212)
CINZA_ESCURO = (90, 94, 104)
ASFALTO = (58, 60, 66)
GRAMA = (46, 110, 64)
FUNDO_PAINEL = (24, 28, 36)
FUNDO_CAIXA = (38, 44, 56)
VERDE = (80, 200, 120)
VERMELHO = (225, 80, 80)
AMARELO = (245, 200, 70)
AZUL = (70, 150, 235)
LARANJA = (240, 140, 50)

# ---------------------------------------------------------------- Arquivos
# Os caminhos partem da pasta do projeto, então o jogo funciona de qualquer pasta.
RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_RECORDE = os.path.join(RAIZ_PROJETO, "data", "recorde.txt")
CAMINHO_CENARIOS = os.path.join(RAIZ_PROJETO, "data", "cenarios.json")
CAMINHO_SPRITES = os.path.join(RAIZ_PROJETO, "assets", "imagens", "spritesheet.bmp")

# ---------------------------------------------------------------- Pista (pixels)
NUM_FAIXAS = 3
LARGURA_FAIXA = 130
PISTA_X = 40
PISTA_LARGURA = NUM_FAIXAS * LARGURA_FAIXA
PAINEL_X = PISTA_X + PISTA_LARGURA + 20

CARRO_LARGURA = 60
CARRO_ALTURA = 100
CARRO_Y = ALTURA_TELA - 170

OBST_LARGURA = 76
OBST_ALTURA = 76

# Distância (em pixels) antes do carro em que a IA "reage" a um obstáculo.
ZONA_REACAO = 170
# Velocidade com que o carro troca de faixa (pixels por segundo).
VELOCIDADE_TROCA_FAIXA = 900

# ---------------------------------------------------------------- Regras do jogo
VIDAS_INICIAIS = 3
DISTANCIA_VITORIA = 1000        # metros para vencer
METROS_POR_NIVEL = 250
NIVEL_MAXIMO = 4
VELOCIDADE_BASE = 15            # metros por segundo no nível 1
ACRESCIMO_VELOCIDADE = 5        # metros por segundo a mais a cada nível
PIXELS_POR_METRO = 8

INTERVALO_OBSTACULOS_BASE = 32  # metros entre obstáculos no nível 1
REDUCAO_INTERVALO_NIVEL = 3     # reduz o intervalo a cada nível
TRECHO_METROS = 100             # a condição da pista pode mudar a cada trecho

PONTOS_POR_METRO_AUTO = 1.0
PONTOS_POR_METRO_MANUAL = 0.5
BONUS_INTERVENCAO_CORRETA = 20
PENALIDADE_INTERVENCAO_DESNECESSARIA = 10

TEMPO_INVULNERAVEL = 1.0        # segundos sem levar dano após uma colisão
TEMPO_MENSAGEM = 5.0            # segundos que a mensagem educativa fica na tela

# ---------------------------------------------------------------- Conjuntos de valores válidos
MODOS = {"auto", "manual"}
CONDICOES = ("normal", "chuva", "neblina", "noite")
FORMAS = ("cone", "carro", "pessoa", "placa", "caixa", "animal")

# Probabilidade (peso) de cada condição de pista por nível.
PESOS_CONDICAO = {
    1: {"normal": 100},
    2: {"normal": 40, "chuva": 20, "neblina": 20, "noite": 20},
    3: {"normal": 25, "chuva": 25, "neblina": 25, "noite": 25},
    4: {"normal": 10, "chuva": 30, "neblina": 30, "noite": 30},
}
