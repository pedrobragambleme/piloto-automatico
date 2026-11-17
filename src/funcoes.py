"""Funções puras de regra e lógica do jogo (não dependem do Pygame)."""

import random

from src.config import (
    ACRESCIMO_VELOCIDADE,
    BONUS_INTERVENCAO_CORRETA,
    CONDICOES,
    DISTANCIA_VITORIA,
    FORMAS,
    INTERVALO_OBSTACULOS_BASE,
    LARGURA_FAIXA,
    METROS_POR_NIVEL,
    NIVEL_MAXIMO,
    NUM_FAIXAS,
    PENALIDADE_INTERVENCAO_DESNECESSARIA,
    PESOS_CONDICAO,
    PISTA_X,
    PONTOS_POR_METRO_AUTO,
    PONTOS_POR_METRO_MANUAL,
    REDUCAO_INTERVALO_NIVEL,
    VELOCIDADE_BASE,
)

# Campos obrigatórios de cada cenário (obstáculo) em data/cenarios.json.
CAMPOS_CENARIO = (
    "id", "nome", "forma", "cor", "condicao",
    "ia_detecta", "confianca", "motivo", "explicacao",
)


# ---------------------------------------------------------------- Pontuação e vidas
def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposição entre dois retângulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)


def houve_colisao(ret_a, ret_b):
    """Verifica sobreposição entre dois retângulos no formato (x, y, largura, altura)."""
    xa, ya, la, aa = ret_a
    xb, yb, lb, ab = ret_b
    return xa < xb + lb and xb < xa + la and ya < yb + ab and yb < ya + aa


def pontos_por_distancia(modo, metros):
    """Pontos ganhos por andar: o modo automático rende mais que o manual."""
    if modo == "auto":
        return metros * PONTOS_POR_METRO_AUTO
    return metros * PONTOS_POR_METRO_MANUAL


def pontos_por_evento(evento):
    """Pontos (ou penalidade) de uma avaliação de intervenção do jogador."""
    if evento == "intervencao_correta":
        return BONUS_INTERVENCAO_CORRETA
    if evento == "intervencao_desnecessaria":
        return -PENALIDADE_INTERVENCAO_DESNECESSARIA
    return 0


# ---------------------------------------------------------------- Progresso e fim de jogo
def calcular_nivel(distancia):
    """Calcula o nível (1 a NIVEL_MAXIMO) conforme a distância percorrida."""
    nivel = int(distancia // METROS_POR_NIVEL) + 1
    return limitar_valor(nivel, 1, NIVEL_MAXIMO)


def velocidade_do_nivel(nivel):
    """Velocidade do carro (metros por segundo) em cada nível."""
    return VELOCIDADE_BASE + (nivel - 1) * ACRESCIMO_VELOCIDADE


def intervalo_entre_obstaculos(nivel):
    """Distância (metros) entre obstáculos; diminui conforme o nível sobe."""
    return INTERVALO_OBSTACULOS_BASE - (nivel - 1) * REDUCAO_INTERVALO_NIVEL


def verificar_fim(vidas, distancia):
    """Retorna 'derrota', 'vitoria' ou 'em_andamento'."""
    if jogador_perdeu(vidas):
        return "derrota"
    if distancia >= DISTANCIA_VITORIA:
        return "vitoria"
    return "em_andamento"


# ---------------------------------------------------------------- Piloto automático (simulado)
def alternar_modo(modo):
    """Troca entre o modo 'auto' e o modo 'manual'."""
    if modo == "auto":
        return "manual"
    return "auto"


def ia_desvia(obstaculo):
    """Indica se o piloto automático detecta (e portanto desvia de) o obstáculo."""
    return bool(obstaculo.get("ia_detecta", False))


def calcular_confianca(obstaculo):
    """Retorna (confiança em %, motivo) que o painel mostra para o obstáculo.

    A confiança exibida nem sempre reflete a realidade: a IA pode estar muito
    confiante e mesmo assim não ter visto o obstáculo.
    """
    confianca = limitar_valor(int(obstaculo.get("confianca", 0)), 0, 100)
    motivo = obstaculo.get("motivo", "Sem informação")
    return confianca, motivo


def faixa_livre_mais_proxima(faixa_atual, faixas_ocupadas, total_faixas=NUM_FAIXAS):
    """Escolhe a faixa livre mais próxima da atual (ou None se não houver saída).

    O carro só pode ir para uma faixa se todas as faixas do caminho também
    estiverem livres (ele não atravessa uma faixa ocupada). Em empate, vai
    para a esquerda.
    """
    if faixa_atual not in faixas_ocupadas:
        return faixa_atual
    for distancia in range(1, total_faixas):
        for sentido in (-1, 1):
            caminho = [faixa_atual + sentido * passo for passo in range(1, distancia + 1)]
            if all(0 <= f < total_faixas and f not in faixas_ocupadas for f in caminho):
                return caminho[-1]
    return None


def avaliar_passagem(obstaculo):
    """Avalia como o jogador/IA lidou com um obstáculo que acabou de passar.

    Retorna 'intervencao_correta', 'intervencao_desnecessaria', 'ia_acertou'
    ou None (o obstáculo nunca foi uma ameaça).
    """
    if not obstaculo["ameaca"]:
        return None
    if obstaculo["interveio"]:
        if ia_desvia(obstaculo):
            return "intervencao_desnecessaria"
        return "intervencao_correta"
    if ia_desvia(obstaculo):
        return "ia_acertou"
    return None


# ---------------------------------------------------------------- Pista e sorteios
def x_da_faixa(faixa, largura):
    """Posição X (pixels) para centralizar um objeto de certa largura na faixa."""
    return PISTA_X + faixa * LARGURA_FAIXA + (LARGURA_FAIXA - largura) // 2


def sortear_condicao(nivel, aleatorio=random):
    """Sorteia a condição da pista (normal, chuva, neblina, noite) para o nível."""
    pesos = PESOS_CONDICAO[nivel]
    return aleatorio.choices(list(pesos.keys()), weights=list(pesos.values()))[0]


def sortear_cenario(cenarios, condicao, aleatorio=random):
    """Sorteia um cenário compatível com a condição atual da pista."""
    candidatos = [c for c in cenarios if c["condicao"] == condicao]
    if not candidatos:
        candidatos = cenarios
    return aleatorio.choice(candidatos)


def cenario_valido(cenario):
    """Confere se um cenário lido do JSON tem todos os campos e valores válidos."""
    for campo in CAMPOS_CENARIO:
        if campo not in cenario:
            return False
    cor = cenario["cor"]
    if not (isinstance(cor, (list, tuple)) and len(cor) == 3):
        return False
    for componente in cor:
        if not isinstance(componente, int) or not 0 <= componente <= 255:
            return False
    if cenario["condicao"] not in CONDICOES or cenario["forma"] not in FORMAS:
        return False
    if not isinstance(cenario["ia_detecta"], bool):
        return False
    confianca = cenario["confianca"]
    if isinstance(confianca, bool) or not isinstance(confianca, int):
        return False
    return 0 <= confianca <= 100
