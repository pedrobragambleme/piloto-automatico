"""Desenho das telas do jogo com Pygame (pista, carro, obstáculos, painel e menus)."""

import pygame

from src.config import (
    ALTURA_TELA,
    AMARELO,
    ASFALTO,
    AZUL,
    BRANCO,
    CARRO_ALTURA,
    CARRO_LARGURA,
    CARRO_Y,
    CINZA,
    CINZA_ESCURO,
    DISTANCIA_VITORIA,
    FUNDO_CAIXA,
    FUNDO_PAINEL,
    GRAMA,
    LARANJA,
    LARGURA_FAIXA,
    LARGURA_TELA,
    NUM_FAIXAS,
    OBST_ALTURA,
    OBST_LARGURA,
    PAINEL_X,
    PIXELS_POR_METRO,
    PISTA_LARGURA,
    PISTA_X,
    PRETO,
    VERDE,
    VERMELHO,
    VIDAS_INICIAIS,
)
from src.funcoes import calcular_confianca, x_da_faixa
from src.obstaculos import proximo_obstaculo_na_faixa

LARGURA_PAINEL = LARGURA_TELA - PAINEL_X - 12

CORES_CONDICAO = {
    "normal": VERDE,
    "chuva": AZUL,
    "neblina": CINZA,
    "noite": AMARELO,
}

# Camadas translúcidas por condição da pista (criadas uma vez, quando preciso).
_CAMADAS = {}


# ---------------------------------------------------------------- Utilitários de texto
def carregar_fontes():
    """Cria as fontes usadas no jogo (fonte padrão do Pygame)."""
    return {
        "titulo": pygame.font.Font(None, 54),
        "grande": pygame.font.Font(None, 36),
        "media": pygame.font.Font(None, 27),
        "pequena": pygame.font.Font(None, 22),
    }


def quebrar_texto(texto, fonte, largura_maxima):
    """Divide um texto em linhas que cabem na largura informada."""
    linhas = []
    atual = ""
    for palavra in texto.split():
        teste = (atual + " " + palavra).strip()
        if fonte.size(teste)[0] <= largura_maxima:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def escrever(tela, texto, fonte, cor, x, y, centralizar=False):
    """Escreve um texto na tela e devolve a altura usada."""
    imagem = fonte.render(texto, True, cor)
    if centralizar:
        x = x - imagem.get_width() // 2
    tela.blit(imagem, (int(x), int(y)))
    return imagem.get_height()


def escrever_paragrafo(tela, texto, fonte, cor, x, y, largura, espacamento=3):
    """Escreve um texto com quebra de linha e devolve o Y logo após o parágrafo."""
    for linha in quebrar_texto(texto, fonte, largura):
        altura = escrever(tela, linha, fonte, cor, x, y)
        y += altura + espacamento
    return y


def _retangulo(x, y, largura, altura):
    return (int(x), int(y), int(largura), int(altura))


# ---------------------------------------------------------------- Pista e elementos
def _camada(condicao):
    """Camada translúcida que simula chuva, neblina ou noite sobre a pista."""
    if condicao == "normal":
        return None
    if condicao not in _CAMADAS:
        cores = {
            "chuva": (50, 80, 130, 80),
            "neblina": (215, 220, 228, 130),
            "noite": (5, 8, 30, 150),
        }
        camada = pygame.Surface((PISTA_LARGURA, ALTURA_TELA), pygame.SRCALPHA)
        camada.fill(cores[condicao])
        _CAMADAS[condicao] = camada
    return _CAMADAS[condicao]


def desenhar_pista(tela, estado):
    """Desenha grama, asfalto e as marcações de faixa rolando com a distância."""
    tela.fill(GRAMA)
    pygame.draw.rect(tela, ASFALTO, _retangulo(PISTA_X, 0, PISTA_LARGURA, ALTURA_TELA))
    pygame.draw.rect(tela, BRANCO, _retangulo(PISTA_X - 4, 0, 4, ALTURA_TELA))
    pygame.draw.rect(tela, BRANCO, _retangulo(PISTA_X + PISTA_LARGURA, 0, 4, ALTURA_TELA))

    deslocamento = int(estado["distancia"] * PIXELS_POR_METRO) % 60
    for divisoria in range(1, NUM_FAIXAS):
        x = PISTA_X + divisoria * LARGURA_FAIXA - 2
        for y in range(-60, ALTURA_TELA, 60):
            pygame.draw.rect(tela, BRANCO, _retangulo(x, y + deslocamento, 4, 34))


def desenhar_obstaculo(tela, obstaculo):
    """Desenha o obstáculo de acordo com a sua forma (cone, carro, pessoa...)."""
    x = x_da_faixa(obstaculo["faixa"], OBST_LARGURA)
    y = int(obstaculo["y"])
    largura, altura = OBST_LARGURA, OBST_ALTURA
    cor = tuple(obstaculo["cor"])
    centro_x = x + largura // 2
    forma = obstaculo["forma"]

    if forma == "cone":
        pygame.draw.polygon(tela, cor, [(centro_x, y + 4), (x + 14, y + altura - 12),
                                        (x + largura - 14, y + altura - 12)])
        pygame.draw.rect(tela, PRETO, _retangulo(x + 8, y + altura - 14, largura - 16, 8))
        pygame.draw.rect(tela, BRANCO, _retangulo(centro_x - 9, y + 34, 18, 6))
    elif forma == "carro":
        pygame.draw.rect(tela, cor, _retangulo(x + 14, y + 2, largura - 28, altura - 4),
                         border_radius=8)
        pygame.draw.rect(tela, PRETO, _retangulo(x + 20, y + 12, largura - 40, 16),
                         border_radius=4)
        pygame.draw.rect(tela, PRETO, _retangulo(x + 20, y + altura - 26, largura - 40, 12),
                         border_radius=4)
    elif forma == "pessoa":
        pygame.draw.circle(tela, (235, 200, 160), (centro_x, y + 14), 10)
        pygame.draw.rect(tela, cor, _retangulo(centro_x - 12, y + 26, 24, 34), border_radius=5)
        pygame.draw.rect(tela, cor, _retangulo(centro_x - 10, y + 58, 8, 14))
        pygame.draw.rect(tela, cor, _retangulo(centro_x + 2, y + 58, 8, 14))
    elif forma == "placa":
        pygame.draw.rect(tela, CINZA_ESCURO, _retangulo(centro_x - 3, y + 30, 6, 42))
        pygame.draw.rect(tela, cor, _retangulo(x + 12, y + 4, largura - 24, 30), border_radius=3)
        pygame.draw.rect(tela, CINZA_ESCURO, _retangulo(x + 12, y + 4, largura - 24, 30), 2,
                         border_radius=3)
    elif forma == "caixa":
        pygame.draw.rect(tela, cor, _retangulo(x + 10, y + 14, largura - 20, altura - 26))
        pygame.draw.rect(tela, PRETO, _retangulo(x + 10, y + 14, largura - 20, altura - 26), 2)
        pygame.draw.line(tela, PRETO, (x + 10, y + 32), (x + largura - 10, y + 32), 2)
    elif forma == "animal":
        pygame.draw.ellipse(tela, cor, _retangulo(x + 8, y + 24, largura - 22, 32))
        pygame.draw.circle(tela, cor, (x + largura - 12, y + 28), 11)
        for pata in (18, 30, 44, 54):
            pygame.draw.line(tela, cor, (x + pata, y + 50), (x + pata, y + 68), 4)


def desenhar_carro(tela, estado):
    """Desenha o carro; a cor mostra o modo atual e ele pisca após uma colisão."""
    if estado["invulneravel"] > 0 and int(estado["invulneravel"] * 10) % 2 == 0:
        return
    cor = AZUL if estado["modo"] == "auto" else LARANJA
    x = int(estado["x"])
    pygame.draw.rect(tela, cor, _retangulo(x, CARRO_Y, CARRO_LARGURA, CARRO_ALTURA),
                     border_radius=12)
    pygame.draw.rect(tela, PRETO, _retangulo(x + 8, CARRO_Y + 22, CARRO_LARGURA - 16, 22),
                     border_radius=5)
    pygame.draw.rect(tela, PRETO, _retangulo(x + 8, CARRO_Y + 66, CARRO_LARGURA - 16, 14),
                     border_radius=5)
    pygame.draw.circle(tela, AMARELO, (x + 12, CARRO_Y + 7), 4)
    pygame.draw.circle(tela, AMARELO, (x + CARRO_LARGURA - 12, CARRO_Y + 7), 4)


def desenhar_efeito_chuva(tela, estado):
    """Riscos de chuva caindo (posição derivada da distância, sem aleatoriedade)."""
    deslocamento = int(estado["distancia"] * PIXELS_POR_METRO * 2)
    for i in range(45):
        x = PISTA_X + (i * 37) % PISTA_LARGURA
        y = (i * 53 + deslocamento) % ALTURA_TELA
        pygame.draw.line(tela, (170, 195, 235), (x, y), (x - 4, y + 14), 1)


# ---------------------------------------------------------------- Tela de jogo (versão inicial, sem painel)
def desenhar_jogo(tela, estado, fontes=None, recorde=0):
    """Desenha a pista, os obstáculos, os efeitos da condição e o carro."""
    desenhar_pista(tela, estado)
    for obstaculo in estado["obstaculos"]:
        desenhar_obstaculo(tela, obstaculo)

    camada = _camada(estado["condicao"])
    if camada is not None:
        tela.blit(camada, (PISTA_X, 0))
    if estado["condicao"] == "chuva":
        desenhar_efeito_chuva(tela, estado)

    desenhar_carro(tela, estado)
