import json

from src.config import CAMINHO_CENARIOS, CONDICOES
from src.dados import carregar_cenarios, carregar_recorde, salvar_recorde


def test_carregar_recorde_arquivo_inexistente_retorna_zero(tmp_path):
    """Sem arquivo de recorde, o recorde começa em 0."""
    assert carregar_recorde(str(tmp_path / "nao_existe.txt")) == 0


def test_salvar_e_carregar_recorde(tmp_path):
    """O recorde salvo deve ser lido de volta."""
    caminho = str(tmp_path / "recorde.txt")
    salvar_recorde(caminho, 850)
    assert carregar_recorde(caminho) == 850


def test_carregar_recorde_com_conteudo_invalido_retorna_zero(tmp_path):
    """Conteúdo que não é número vira recorde 0."""
    arquivo = tmp_path / "recorde.txt"
    arquivo.write_text("abc", encoding="utf-8")
    assert carregar_recorde(str(arquivo)) == 0


def test_carregar_recorde_arquivo_vazio_retorna_zero(tmp_path):
    """Arquivo vazio vira recorde 0."""
    arquivo = tmp_path / "recorde.txt"
    arquivo.write_text("", encoding="utf-8")
    assert carregar_recorde(str(arquivo)) == 0


def test_cenarios_do_jogo_sao_validos_e_suficientes():
    """O JSON do jogo tem pelo menos 8 cenários, todos válidos e com ids únicos."""
    cenarios = carregar_cenarios(CAMINHO_CENARIOS)
    assert len(cenarios) >= 8
    ids = [c["id"] for c in cenarios]
    assert len(ids) == len(set(ids))


def test_cenarios_cobrem_todas_as_condicoes_e_os_dois_tipos_de_deteccao():
    """Cada condição tem cenários, e existem obstáculos detectados e não detectados."""
    cenarios = carregar_cenarios(CAMINHO_CENARIOS)
    for condicao in CONDICOES:
        assert any(c["condicao"] == condicao for c in cenarios)
    assert any(c["ia_detecta"] for c in cenarios)
    assert any(not c["ia_detecta"] for c in cenarios)


def test_carregar_cenarios_arquivo_inexistente_retorna_lista_vazia(tmp_path):
    """Sem arquivo, não há cenários (e o jogo avisa o erro)."""
    assert carregar_cenarios(str(tmp_path / "nada.json")) == []


def test_carregar_cenarios_json_invalido_retorna_lista_vazia(tmp_path):
    """JSON quebrado não derruba o programa."""
    arquivo = tmp_path / "cenarios.json"
    arquivo.write_text("{ isto nao e json", encoding="utf-8")
    assert carregar_cenarios(str(arquivo)) == []


def test_carregar_cenarios_ignora_entradas_invalidas(tmp_path):
    """Entradas incompletas são descartadas e as válidas permanecem."""
    valido = {
        "id": "a", "nome": "Cone", "forma": "cone", "cor": [255, 0, 0],
        "condicao": "normal", "ia_detecta": True, "confianca": 90,
        "motivo": "ok", "explicacao": "ok",
    }
    arquivo = tmp_path / "cenarios.json"
    arquivo.write_text(json.dumps([valido, {"id": "b"}, "texto"]), encoding="utf-8")
    assert carregar_cenarios(str(arquivo)) == [valido]
