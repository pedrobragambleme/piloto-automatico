import json

from src.funcoes import cenario_valido


def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuação recorde em arquivo texto."""
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se não existir valor válido."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

            if conteudo == "":
                return 0

            return int(conteudo)

    except (FileNotFoundError, ValueError):
        return 0


def carregar_cenarios(caminho_arquivo):
    """Lê os cenários (obstáculos) do JSON, ignorando entradas inválidas.

    Retorna uma lista vazia se o arquivo não existir ou não for um JSON válido.
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(dados, list):
        return []

    return [item for item in dados if isinstance(item, dict) and cenario_valido(item)]
