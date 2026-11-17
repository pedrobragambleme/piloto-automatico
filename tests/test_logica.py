from src.funcoes import (
    alternar_modo,
    avaliar_passagem,
    calcular_confianca,
    calcular_nivel,
    calcular_pontos,
    cenario_valido,
    faixa_livre_mais_proxima,
    houve_colisao,
    ia_desvia,
    jogador_perdeu,
    limitar_valor,
    pontos_por_distancia,
    pontos_por_evento,
    sortear_condicao,
    velocidade_do_nivel,
    verificar_fim,
)


# ---------------------------------------------------------------- Testes do template
def test_calcular_pontos():
    """Deve somar corretamente os pontos atuais com os pontos ganhos."""
    assert calcular_pontos(10, 5) == 15


def test_jogador_perdeu_com_zero_vidas():
    """Deve indicar derrota quando o total de vidas chega a zero."""
    assert jogador_perdeu(0) is True


def test_jogador_nao_perdeu_com_vidas():
    """Nao deve indicar derrota quando o jogador ainda tem vidas."""
    assert jogador_perdeu(3) is False


def test_limitar_valor_abaixo_do_minimo():
    """Deve retornar o limite minimo quando o valor informado for menor."""
    assert limitar_valor(-5, 0, 100) == 0


def test_limitar_valor_acima_do_maximo():
    """Deve retornar o limite maximo quando o valor informado for maior."""
    assert limitar_valor(150, 0, 100) == 100


def test_limitar_valor_dentro_do_intervalo():
    """Deve manter o valor original quando ele ja estiver no intervalo."""
    assert limitar_valor(50, 0, 100) == 50


# ---------------------------------------------------------------- Piloto automático
def test_ia_desvia_obstaculo_detectavel():
    """A IA desvia quando o obstáculo é detectável."""
    assert ia_desvia({"ia_detecta": True}) is True


def test_ia_nao_desvia_obstaculo_nao_detectavel():
    """A IA não desvia quando não detecta o obstáculo."""
    assert ia_desvia({"ia_detecta": False}) is False


def test_calcular_confianca_retorna_valor_e_motivo():
    """O painel recebe a confiança e o motivo do cenário."""
    obstaculo = {"confianca": 91, "motivo": "Pista livre"}
    assert calcular_confianca(obstaculo) == (91, "Pista livre")


def test_calcular_confianca_limita_entre_0_e_100():
    """Valores fora do intervalo são limitados."""
    assert calcular_confianca({"confianca": 150, "motivo": "x"})[0] == 100
    assert calcular_confianca({"confianca": -4, "motivo": "x"})[0] == 0


def test_alternar_modo():
    """ESPAÇO alterna entre automático e manual."""
    assert alternar_modo("auto") == "manual"
    assert alternar_modo("manual") == "auto"


def test_faixa_livre_mantem_faixa_se_ja_estiver_livre():
    """Se a faixa atual está livre, a IA fica onde está."""
    assert faixa_livre_mais_proxima(1, {0}) == 1


def test_faixa_livre_escolhe_a_mais_proxima():
    """Com a faixa do meio ocupada, escolhe a vizinha livre (esquerda em empate)."""
    assert faixa_livre_mais_proxima(1, {1}) == 0
    assert faixa_livre_mais_proxima(1, {0, 1}) == 2
    assert faixa_livre_mais_proxima(0, {0}) == 1


def test_faixa_livre_nao_atravessa_faixa_ocupada():
    """O carro não pode atravessar uma faixa ocupada para chegar a uma livre."""
    assert faixa_livre_mais_proxima(0, {0, 1}) is None
    assert faixa_livre_mais_proxima(2, {1, 2}) is None
    assert faixa_livre_mais_proxima(2, {2}) == 1


def test_faixa_livre_sem_saida():
    """Se todas as faixas estão ocupadas, não há faixa livre."""
    assert faixa_livre_mais_proxima(1, {0, 1, 2}) is None


# ---------------------------------------------------------------- Colisão
def test_houve_colisao_com_sobreposicao():
    """Retângulos que se sobrepõem colidem."""
    assert houve_colisao((0, 0, 10, 10), (5, 5, 10, 10)) is True


def test_houve_colisao_sem_sobreposicao():
    """Retângulos afastados não colidem."""
    assert houve_colisao((0, 0, 10, 10), (20, 20, 10, 10)) is False


def test_houve_colisao_apenas_encostando_nao_colide():
    """Retângulos apenas encostados não contam como colisão."""
    assert houve_colisao((0, 0, 10, 10), (10, 0, 10, 10)) is False


# ---------------------------------------------------------------- Pontuação, nível e fim
def test_pontos_por_distancia_modo_automatico_vale_mais():
    """No automático ganha-se 1 ponto por metro; no manual, 0,5."""
    assert pontos_por_distancia("auto", 10) == 10
    assert pontos_por_distancia("manual", 10) == 5


def test_pontos_por_evento():
    """Intervenção correta dá bônus; desnecessária, penalidade."""
    assert pontos_por_evento("intervencao_correta") == 20
    assert pontos_por_evento("intervencao_desnecessaria") == -10
    assert pontos_por_evento("ia_acertou") == 0
    assert pontos_por_evento(None) == 0


def test_calcular_nivel_sobe_a_cada_250_metros():
    """O nível sobe a cada 250 m e para no máximo (4)."""
    assert calcular_nivel(0) == 1
    assert calcular_nivel(249) == 1
    assert calcular_nivel(250) == 2
    assert calcular_nivel(500) == 3
    assert calcular_nivel(750) == 4
    assert calcular_nivel(5000) == 4


def test_velocidade_aumenta_com_o_nivel():
    """Níveis mais altos são mais rápidos."""
    assert velocidade_do_nivel(2) > velocidade_do_nivel(1)


def test_verificar_fim_vitoria():
    """Chegar a 1000 m com vidas é vitória."""
    assert verificar_fim(2, 1000) == "vitoria"


def test_verificar_fim_derrota():
    """Ficar sem vidas é derrota."""
    assert verificar_fim(0, 300) == "derrota"


def test_verificar_fim_em_andamento():
    """Com vidas e antes de 1000 m a partida continua."""
    assert verificar_fim(3, 999) == "em_andamento"


# ---------------------------------------------------------------- Avaliação de intervenção
def _obstaculo(ameaca, interveio, detecta):
    return {"ameaca": ameaca, "interveio": interveio, "ia_detecta": detecta}


def test_intervencao_correta_quando_ia_nao_detecta():
    """Jogador interveio e a IA não veria o obstáculo: acerto."""
    assert avaliar_passagem(_obstaculo(True, True, False)) == "intervencao_correta"


def test_intervencao_desnecessaria_quando_ia_detecta():
    """Jogador interveio mas a IA já detectava: intervenção desnecessária."""
    assert avaliar_passagem(_obstaculo(True, True, True)) == "intervencao_desnecessaria"


def test_ia_acertou_quando_jogador_nao_interveio():
    """Sem intervenção, a IA detectou e desviou."""
    assert avaliar_passagem(_obstaculo(True, False, True)) == "ia_acertou"


def test_obstaculo_que_nao_era_ameaca_nao_e_avaliado():
    """Obstáculo fora da faixa do carro não gera avaliação."""
    assert avaliar_passagem(_obstaculo(False, False, True)) is None


# ---------------------------------------------------------------- Sorteios e validação
def test_nivel_1_sempre_sorteia_condicao_normal():
    """No nível 1 só existe pista normal."""
    assert all(sortear_condicao(1) == "normal" for _ in range(20))


def _cenario_base():
    return {
        "id": "x", "nome": "Cone", "forma": "cone", "cor": [255, 0, 0],
        "condicao": "normal", "ia_detecta": True, "confianca": 90,
        "motivo": "ok", "explicacao": "ok",
    }


def test_cenario_valido():
    """Um cenário completo é aceito."""
    assert cenario_valido(_cenario_base()) is True


def test_cenario_invalido_sem_campo():
    """Falta de campo obrigatório invalida o cenário."""
    cenario = _cenario_base()
    del cenario["motivo"]
    assert cenario_valido(cenario) is False


def test_cenario_invalido_com_condicao_desconhecida():
    """Condição fora da lista invalida o cenário."""
    cenario = _cenario_base()
    cenario["condicao"] = "granizo"
    assert cenario_valido(cenario) is False


def test_cenario_invalido_com_cor_errada():
    """Cor precisa ter 3 valores entre 0 e 255."""
    cenario = _cenario_base()
    cenario["cor"] = [300, 0, 0]
    assert cenario_valido(cenario) is False
