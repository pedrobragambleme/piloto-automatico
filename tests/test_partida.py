import random

from src.config import CAMINHO_CENARIOS, DISTANCIA_VITORIA, OBST_ALTURA
from src.dados import carregar_cenarios
from src.obstaculos import criar_obstaculo
from src.partida import (
    alternar_modo_jogador,
    atualizar_partida,
    criar_estado,
    mover_manual,
)

DT = 1 / 60


def _cenario(detecta, condicao="normal"):
    return {
        "id": "teste", "nome": "Obstáculo de teste", "forma": "cone",
        "cor": [255, 140, 0], "condicao": condicao, "ia_detecta": detecta,
        "confianca": 90, "motivo": "teste", "explicacao": "Explicação de teste.",
    }


def _estado_com_obstaculo(detecta, faixa=1):
    """Estado limpo com um único obstáculo na faixa informada (sem novos sorteios)."""
    estado = criar_estado()
    estado["ultimo_obstaculo"] = 10_000.0   # impede o surgimento de novos obstáculos
    obstaculo = criar_obstaculo(_cenario(detecta), faixa)
    obstaculo["ameaca"] = faixa == estado["faixa"]
    estado["obstaculos"].append(obstaculo)
    return estado


def _rodar_ate_obstaculo_sumir(estado, acao=None, limite=1200):
    """Roda quadros até o obstáculo sair de cena; `acao(estado, quadro)` pode agir."""
    for quadro in range(limite):
        if acao is not None:
            acao(estado, quadro)
        atualizar_partida(estado, [], DT)
        if not estado["obstaculos"]:
            return quadro
    raise AssertionError("obstáculo nunca saiu de cena")


# ---------------------------------------------------------------- Controles
def test_mover_manual_so_funciona_no_modo_manual():
    """No modo automático as setas não mudam de faixa."""
    estado = criar_estado()
    mover_manual(estado, -1)
    assert estado["faixa"] == 1
    alternar_modo_jogador(estado)
    mover_manual(estado, -1)
    assert estado["faixa"] == 0


def test_mover_manual_nao_sai_da_pista():
    """O carro nunca passa da primeira nem da última faixa."""
    estado = criar_estado()
    alternar_modo_jogador(estado)
    for _ in range(5):
        mover_manual(estado, 1)
    assert estado["faixa"] == 2
    for _ in range(5):
        mover_manual(estado, -1)
    assert estado["faixa"] == 0


# ---------------------------------------------------------------- Piloto automático
def test_ia_desvia_de_obstaculo_detectado():
    """No automático, a IA desvia de um obstáculo que enxerga."""
    estado = _estado_com_obstaculo(detecta=True)
    _rodar_ate_obstaculo_sumir(estado)
    assert estado["vidas"] == 3
    assert estado["estatisticas"]["desvios_da_ia"] == 1


def test_ia_bate_em_obstaculo_nao_detectado():
    """No automático, a IA não vê o obstáculo e o carro colide (-1 vida, com explicação)."""
    estado = _estado_com_obstaculo(detecta=False)
    _rodar_ate_obstaculo_sumir(estado)
    assert estado["vidas"] == 2
    assert estado["estatisticas"]["colisoes"] == 1
    assert estado["mensagem"]["tipo"] == "erro"
    assert estado["mensagem"]["texto"] == "Explicação de teste."


def test_obstaculo_em_outra_faixa_nao_gera_dano_nem_avaliacao():
    """Obstáculo fora da faixa do carro passa sem efeito."""
    estado = _estado_com_obstaculo(detecta=False, faixa=0)
    _rodar_ate_obstaculo_sumir(estado)
    assert estado["vidas"] == 3
    assert estado["estatisticas"]["intervencoes_corretas"] == 0


# ---------------------------------------------------------------- Intervenção do jogador
def _assumir_e_desviar(estado, quadro):
    if quadro == 5:
        alternar_modo_jogador(estado)
        mover_manual(estado, -1)


def test_intervencao_correta_da_bonus():
    """Assumir o controle e desviar do que a IA não via rende pontos extras."""
    estado = _estado_com_obstaculo(detecta=False)
    _rodar_ate_obstaculo_sumir(estado, _assumir_e_desviar)
    assert estado["vidas"] == 3
    assert estado["estatisticas"]["intervencoes_corretas"] == 1
    assert estado["mensagem"]["tipo"] == "acerto"
    assert estado["pontos"] >= 20


def test_intervencao_desnecessaria_tira_pontos():
    """Assumir o controle quando a IA já detectava o obstáculo gera penalidade."""
    estado = _estado_com_obstaculo(detecta=True)
    estado["pontos"] = 100.0
    _rodar_ate_obstaculo_sumir(estado, _assumir_e_desviar)
    assert estado["vidas"] == 3
    assert estado["estatisticas"]["intervencoes_desnecessarias"] == 1
    assert estado["mensagem"]["tipo"] == "aviso"


def test_bater_no_modo_manual_tem_mensagem_propria():
    """Se o jogador bate no modo manual, a mensagem fala da responsabilidade dele."""
    estado = _estado_com_obstaculo(detecta=True)

    def so_assumir(estado, quadro):
        if quadro == 5:
            alternar_modo_jogador(estado)

    _rodar_ate_obstaculo_sumir(estado, so_assumir)
    assert estado["vidas"] == 2
    assert "controle" in estado["mensagem"]["texto"]


def test_invulnerabilidade_evita_perder_duas_vidas_na_mesma_batida():
    """Depois de uma colisão há 1 s de proteção."""
    estado = _estado_com_obstaculo(detecta=False)
    _rodar_ate_obstaculo_sumir(estado)
    assert estado["invulneravel"] > 0


# ---------------------------------------------------------------- Partida completa
def _simular_partida(cenarios, semente, limite_quadros=20_000):
    estado = criar_estado()
    aleatorio = random.Random(semente)
    for _ in range(limite_quadros):
        atualizar_partida(estado, cenarios, DT, aleatorio)
        if estado["fim"] is not None:
            break
    return estado


def test_partida_so_com_obstaculos_detectados_termina_em_vitoria():
    """Se a IA enxerga tudo, ela completa os 1000 m sem perder vidas."""
    detectaveis = [_cenario(True, c) for c in ("normal", "chuva", "neblina", "noite")]
    for semente in range(5):
        estado = _simular_partida(detectaveis, semente)
        assert estado["fim"] == "vitoria"
        assert estado["vidas"] == 3
        assert estado["distancia"] == DISTANCIA_VITORIA


def test_partida_so_com_obstaculos_nao_detectados_termina_em_derrota():
    """Se a IA não enxerga nada e o jogador não interfere, as vidas acabam."""
    invisiveis = [_cenario(False, c) for c in ("normal", "chuva", "neblina", "noite")]
    estado = _simular_partida(invisiveis, semente=1)
    assert estado["fim"] == "derrota"
    assert estado["vidas"] == 0
    assert estado["distancia"] < DISTANCIA_VITORIA


def test_partida_com_cenarios_reais_sempre_termina():
    """Com os cenários do JSON a partida chega a um fim (vitória ou derrota)."""
    cenarios = carregar_cenarios(CAMINHO_CENARIOS)
    for semente in range(5):
        estado = _simular_partida(cenarios, semente)
        assert estado["fim"] in ("vitoria", "derrota")


def test_nivel_e_condicao_evoluem_durante_a_partida():
    """O nível chega ao máximo e a pista deixa de ser sempre 'normal'."""
    cenarios = carregar_cenarios(CAMINHO_CENARIOS)
    detectaveis = [c for c in cenarios if c["ia_detecta"]]
    estado = criar_estado()
    aleatorio = random.Random(3)
    condicoes_vistas = set()
    for _ in range(20_000):
        atualizar_partida(estado, detectaveis, DT, aleatorio)
        condicoes_vistas.add(estado["condicao"])
        if estado["fim"] is not None:
            break
    assert estado["nivel"] == 4
    assert len(condicoes_vistas) > 1


def test_partida_encerrada_nao_atualiza_mais():
    """Depois do fim, atualizar a partida não muda mais o estado."""
    estado = criar_estado()
    estado["fim"] = "derrota"
    distancia = estado["distancia"]
    atualizar_partida(estado, [], DT)
    assert estado["distancia"] == distancia


def test_obstaculo_nasce_acima_da_tela():
    """Obstáculos surgem fora da tela, no topo."""
    obstaculo = criar_obstaculo(_cenario(True), 0)
    assert obstaculo["y"] == -OBST_ALTURA
