from src.config import ALCANCE_IA, CARRO_ALTURA, CARRO_Y, OBST_ALTURA
from src.obstaculos import criar_obstaculo, no_alcance_da_ia


def _obstaculo(y):
    cenario = {
        "id": "t", "nome": "Cone", "forma": "cone", "cor": [255, 0, 0],
        "condicao": "normal", "ia_detecta": True, "confianca": 90,
        "motivo": "ok", "explicacao": "ok",
    }
    obstaculo = criar_obstaculo(cenario, 1)
    obstaculo["y"] = y
    return obstaculo


def test_obstaculo_recem_criado_esta_fora_do_alcance_da_ia():
    """Logo que nasce, acima da tela, o obstáculo ainda não é visto pela IA."""
    assert no_alcance_da_ia(_obstaculo(-OBST_ALTURA)) is False


def test_obstaculo_dentro_do_alcance_da_ia():
    """Perto o bastante do carro, a câmera da IA o alcança."""
    assert no_alcance_da_ia(_obstaculo(CARRO_Y - ALCANCE_IA + 10)) is True


def test_obstaculo_que_ja_passou_do_carro_sai_do_alcance():
    """Depois que passa pelo carro, o obstáculo deixa de ser acompanhado."""
    assert no_alcance_da_ia(_obstaculo(CARRO_Y + CARRO_ALTURA)) is False
