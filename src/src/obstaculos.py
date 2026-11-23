"""Criação e consulta de obstáculos (sem dependência do Pygame)."""

from src.config import (
    CARRO_ALTURA,
    CARRO_LARGURA,
    CARRO_Y,
    OBST_ALTURA,
    OBST_LARGURA,
    ZONA_REACAO,
)
from src.funcoes import ia_desvia, x_da_faixa


def criar_obstaculo(cenario, faixa):
    """Cria um obstáculo (dicionário) a partir de um cenário do JSON.

    Além dos dados do cenário, guarda o estado de jogo do obstáculo:
    - na_zona: já chegou perto o bastante para a IA reagir;
    - ameaca: está na faixa do carro (precisa ser desviado);
    - interveio: o jogador estava no modo manual enquanto ele era uma ameaça.
    """
    obstaculo = dict(cenario)
    obstaculo.update({
        "faixa": faixa,
        "y": float(-OBST_ALTURA),
        "na_zona": False,
        "ameaca": False,
        "interveio": False,
    })
    return obstaculo


def retangulo_obstaculo(obstaculo):
    """Área de colisão (x, y, largura, altura) do obstáculo, um pouco menor que o desenho."""
    x = x_da_faixa(obstaculo["faixa"], OBST_LARGURA)
    return (x + 8, obstaculo["y"] + 8, OBST_LARGURA - 16, OBST_ALTURA - 16)


def retangulo_carro(x):
    """Área de colisão (x, y, largura, altura) do carro, um pouco menor que o desenho."""
    return (x + 6, CARRO_Y + 8, CARRO_LARGURA - 12, CARRO_ALTURA - 16)


def entrou_na_zona(obstaculo):
    """Verdadeiro quando o obstáculo chegou à zona em que a IA reage."""
    return obstaculo["y"] + OBST_ALTURA >= CARRO_Y - ZONA_REACAO


def passou_do_carro(obstaculo):
    """Verdadeiro quando o obstáculo já passou inteiro pelo carro."""
    return obstaculo["y"] >= CARRO_Y + CARRO_ALTURA


def faixas_ocupadas_pela_ia(obstaculos):
    """Faixas com obstáculos que a IA enxerga e que estão perto do carro."""
    return {
        o["faixa"]
        for o in obstaculos
        if ia_desvia(o) and entrou_na_zona(o) and not passou_do_carro(o)
    }


def proximo_obstaculo_na_faixa(obstaculos, faixa):
    """Obstáculo visível mais próximo do carro na faixa informada (ou None)."""
    candidatos = [
        o for o in obstaculos
        if o["faixa"] == faixa
        and o["y"] + OBST_ALTURA > 0
        and not passou_do_carro(o)
    ]
    if not candidatos:
        return None
    return max(candidatos, key=lambda o: o["y"])
