"""Estado e atualização de uma partida (regras do jogo, sem dependência do Pygame).

O estado da partida é um dicionário. A cada quadro, `atualizar_partida` avança
a distância, gera e move obstáculos, faz o piloto automático reagir, trata
colisões e avalia se o jogador interveio corretamente.
"""

import random

from src.config import (
    CARRO_LARGURA,
    DISTANCIA_VITORIA,
    NUM_FAIXAS,
    PIXELS_POR_METRO,
    TEMPO_INVULNERAVEL,
    TEMPO_MENSAGEM,
    TRECHO_METROS,
    VELOCIDADE_TROCA_FAIXA,
    VIDAS_INICIAIS,
)
from src.funcoes import (
    alternar_modo,
    avaliar_passagem,
    calcular_nivel,
    faixa_livre_mais_proxima,
    houve_colisao,
    ia_desvia,
    intervalo_entre_obstaculos,
    limitar_valor,
    pontos_por_distancia,
    pontos_por_evento,
    sortear_cenario,
    sortear_condicao,
    tomar_dano,
    velocidade_do_nivel,
    verificar_fim,
    x_da_faixa,
)
from src.obstaculos import (
    criar_obstaculo,
    entrou_na_zona,
    faixas_ocupadas_pela_ia,
    passou_do_carro,
    retangulo_carro,
    retangulo_obstaculo,
)


def criar_estado():
    """Cria o estado inicial de uma partida nova."""
    return {
        "modo": "auto",
        "faixa": 1,
        "x": float(x_da_faixa(1, CARRO_LARGURA)),
        "vidas": VIDAS_INICIAIS,
        "distancia": 0.0,
        "pontos": 0.0,
        "nivel": 1,
        "condicao": "normal",
        "proximo_trecho": TRECHO_METROS,
        "ultimo_obstaculo": -20.0,   # o primeiro obstáculo surge após ~12 m
        "obstaculos": [],
        "invulneravel": 0.0,
        "mensagem": None,
        "fim": None,                 # None, 'vitoria' ou 'derrota'
        "novo_recorde": False,
        "estatisticas": {
            "intervencoes_corretas": 0,
            "intervencoes_desnecessarias": 0,
            "desvios_da_ia": 0,
            "colisoes": 0,
        },
    }


# ---------------------------------------------------------------- Ações do jogador
def alternar_modo_jogador(estado):
    """Alterna entre o modo automático e o manual (tecla ESPAÇO)."""
    if estado["fim"] is None:
        estado["modo"] = alternar_modo(estado["modo"])


def mover_manual(estado, direcao):
    """Troca de faixa (-1 esquerda, +1 direita). Só funciona no modo manual."""
    if estado["fim"] is not None or estado["modo"] != "manual":
        return
    estado["faixa"] = limitar_valor(estado["faixa"] + direcao, 0, NUM_FAIXAS - 1)


# ---------------------------------------------------------------- Atualização por quadro
def atualizar_partida(estado, cenarios, dt, aleatorio=random):
    """Avança a partida em `dt` segundos."""
    if estado["fim"] is not None:
        return estado

    estado["nivel"] = calcular_nivel(estado["distancia"])
    velocidade = velocidade_do_nivel(estado["nivel"])

    _avancar_distancia(estado, velocidade * dt)
    _atualizar_condicao(estado, aleatorio)
    _gerar_obstaculos(estado, cenarios, aleatorio)
    _mover_obstaculos(estado, velocidade * PIXELS_POR_METRO * dt)
    _acompanhar_ameacas(estado)
    _ia_reagir(estado)
    _animar_carro(estado, dt)
    _tratar_colisoes(estado)
    _tratar_passagens(estado)
    _atualizar_temporizadores(estado, dt)

    resultado = verificar_fim(estado["vidas"], estado["distancia"])
    if resultado != "em_andamento":
        estado["fim"] = resultado
    return estado


def _avancar_distancia(estado, metros):
    metros = min(metros, DISTANCIA_VITORIA - estado["distancia"])
    estado["distancia"] += metros
    estado["pontos"] += pontos_por_distancia(estado["modo"], metros)


def _atualizar_condicao(estado, aleatorio):
    """A cada trecho a condição da pista pode mudar (chuva, neblina, noite)."""
    if estado["distancia"] >= estado["proximo_trecho"]:
        estado["condicao"] = sortear_condicao(estado["nivel"], aleatorio)
        estado["proximo_trecho"] += TRECHO_METROS


def _gerar_obstaculos(estado, cenarios, aleatorio):
    intervalo = intervalo_entre_obstaculos(estado["nivel"])
    if estado["distancia"] - estado["ultimo_obstaculo"] < intervalo:
        return
    cenario = sortear_cenario(cenarios, estado["condicao"], aleatorio)
    faixa = aleatorio.randrange(NUM_FAIXAS)
    obstaculo = criar_obstaculo(cenario, faixa)
    obstaculo["ameaca"] = faixa == estado["faixa"]
    estado["obstaculos"].append(obstaculo)
    estado["ultimo_obstaculo"] = estado["distancia"]


def _mover_obstaculos(estado, deslocamento):
    for obstaculo in estado["obstaculos"]:
        obstaculo["y"] += deslocamento


def _acompanhar_ameacas(estado):
    """Marca ameaças e registra se o jogador estava no controle manual."""
    for obstaculo in estado["obstaculos"]:
        if not obstaculo["na_zona"] and entrou_na_zona(obstaculo):
            obstaculo["na_zona"] = True
            if obstaculo["faixa"] == estado["faixa"]:
                obstaculo["ameaca"] = True
        if (obstaculo["ameaca"] and estado["modo"] == "manual"
                and not passou_do_carro(obstaculo)):
            obstaculo["interveio"] = True


def _ia_reagir(estado):
    """No modo automático, a IA desvia apenas dos obstáculos que detecta."""
    if estado["modo"] != "auto":
        return
    for obstaculo in estado["obstaculos"]:
        if (obstaculo["na_zona"] and not passou_do_carro(obstaculo)
                and obstaculo["faixa"] == estado["faixa"] and ia_desvia(obstaculo)):
            ocupadas = faixas_ocupadas_pela_ia(estado["obstaculos"])
            nova_faixa = faixa_livre_mais_proxima(estado["faixa"], ocupadas)
            if nova_faixa is not None:
                estado["faixa"] = nova_faixa
            return


def _animar_carro(estado, dt):
    """Move o carro suavemente até a faixa de destino."""
    alvo = x_da_faixa(estado["faixa"], CARRO_LARGURA)
    passo = VELOCIDADE_TROCA_FAIXA * dt
    diferenca = alvo - estado["x"]
    if abs(diferenca) <= passo:
        estado["x"] = float(alvo)
    elif diferenca > 0:
        estado["x"] += passo
    else:
        estado["x"] -= passo


def _tratar_colisoes(estado):
    if estado["invulneravel"] > 0:
        return
    carro = retangulo_carro(estado["x"])
    for obstaculo in estado["obstaculos"]:
        if houve_colisao(carro, retangulo_obstaculo(obstaculo)):
            estado["vidas"] = tomar_dano(estado["vidas"], 1)
            estado["invulneravel"] = TEMPO_INVULNERAVEL
            estado["estatisticas"]["colisoes"] += 1
            estado["mensagem"] = _mensagem_colisao(estado, obstaculo)
            estado["obstaculos"].remove(obstaculo)
            return


def _mensagem_colisao(estado, obstaculo):
    """Explicação educativa que aparece depois de uma batida."""
    if estado["modo"] == "manual":
        texto = (f"Você estava no controle e bateu em: {obstaculo['nome']}. "
                 "No modo manual a atenção é sua: olhe a pista antes de trocar de faixa.")
    elif not ia_desvia(obstaculo):
        texto = obstaculo["explicacao"]
    else:
        texto = (f"A IA não conseguiu desviar de: {obstaculo['nome']}. "
                 "Sistemas automáticos também têm limites.")
    return {"titulo": "Colisão! -1 vida", "texto": texto,
            "tipo": "erro", "tempo": TEMPO_MENSAGEM}


def _tratar_passagens(estado):
    """Avalia cada obstáculo que o carro acabou de ultrapassar sem bater."""
    for obstaculo in list(estado["obstaculos"]):
        if not passou_do_carro(obstaculo):
            continue
        resultado = avaliar_passagem(obstaculo)
        estado["pontos"] = max(0.0, estado["pontos"] + pontos_por_evento(resultado))
        _registrar_resultado(estado, obstaculo, resultado)
        estado["obstaculos"].remove(obstaculo)


def _registrar_resultado(estado, obstaculo, resultado):
    stats = estado["estatisticas"]
    if resultado == "intervencao_correta":
        stats["intervencoes_corretas"] += 1
        estado["mensagem"] = {
            "titulo": "Boa intervenção! +20",
            "texto": f"Você percebeu o risco que a IA não via: {obstaculo['nome']}.",
            "tipo": "acerto", "tempo": TEMPO_MENSAGEM,
        }
    elif resultado == "intervencao_desnecessaria":
        stats["intervencoes_desnecessarias"] += 1
        estado["mensagem"] = {
            "titulo": "Intervenção desnecessária -10",
            "texto": (f"A IA já detectava: {obstaculo['nome']}. Quando o sistema "
                      "é confiável, deixe-o dirigir e volte ao modo automático."),
            "tipo": "aviso", "tempo": TEMPO_MENSAGEM,
        }
    elif resultado == "ia_acertou":
        stats["desvios_da_ia"] += 1


def _atualizar_temporizadores(estado, dt):
    estado["invulneravel"] = max(0.0, estado["invulneravel"] - dt)
    if estado["mensagem"] is not None:
        estado["mensagem"]["tempo"] -= dt
        if estado["mensagem"]["tempo"] <= 0:
            estado["mensagem"] = None
