import pygame

from src.config import (
    ALTURA_TELA,
    CAMINHO_CENARIOS,
    CAMINHO_RECORDE,
    FPS,
    LARGURA_TELA,
    TITULO_JOGO,
)
from src.dados import carregar_cenarios, carregar_recorde, salvar_recorde
from src.interface import (
    carregar_fontes,
    desenhar_fim,
    desenhar_jogo,
    desenhar_menu,
    desenhar_pausa,
)
from src.partida import (
    alternar_modo_jogador,
    atualizar_partida,
    criar_estado,
    mover_manual,
)


def tratar_tecla(tecla, tela_atual, estado):
    """Reage a uma tecla pressionada.

    Retorna (nova_tela, novo_estado, deve_sair). As telas possíveis são
    'menu', 'jogando', 'pausado' e 'fim'.
    """
    if tecla == pygame.K_ESCAPE:
        return tela_atual, estado, True

    if tela_atual == "menu":
        if tecla == pygame.K_RETURN:
            return "jogando", criar_estado(), False

    elif tela_atual == "jogando":
        if tecla == pygame.K_SPACE:
            alternar_modo_jogador(estado)
        elif tecla == pygame.K_LEFT:
            mover_manual(estado, -1)
        elif tecla == pygame.K_RIGHT:
            mover_manual(estado, 1)
        elif tecla == pygame.K_p:
            return "pausado", estado, False
        elif tecla == pygame.K_r:
            return "jogando", criar_estado(), False

    elif tela_atual == "pausado":
        if tecla == pygame.K_p:
            return "jogando", estado, False
        if tecla == pygame.K_r:
            return "jogando", criar_estado(), False

    elif tela_atual == "fim":
        if tecla in (pygame.K_r, pygame.K_RETURN):
            return "jogando", criar_estado(), False

    return tela_atual, estado, False


def finalizar_partida(estado, recorde):
    """Atualiza e salva o recorde ao fim da partida; devolve o recorde vigente."""
    pontos = int(estado["pontos"])
    if pontos > recorde:
        recorde = pontos
        estado["novo_recorde"] = True
        salvar_recorde(CAMINHO_RECORDE, recorde)
    return recorde


def executar_jogo():
    """Executa o loop principal do jogo: entrada, atualização e desenho."""
    pygame.init()

    cenarios = carregar_cenarios(CAMINHO_CENARIOS)
    if not cenarios:
        print(f"Erro: não foi possível carregar os cenários de '{CAMINHO_CENARIOS}'.")
        pygame.quit()
        return

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    fontes = carregar_fontes()
    recorde = carregar_recorde(CAMINHO_RECORDE)

    tela_atual = "menu"
    estado = criar_estado()
    rodando = True

    # Loop principal: processa entrada, atualiza estado e renderiza a cena.
    while rodando:
        # dt em segundos; o limite evita saltos grandes se a janela travar.
        dt = min(relogio.tick(FPS) / 1000.0, 0.05)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                tela_atual, estado, sair = tratar_tecla(evento.key, tela_atual, estado)
                if sair:
                    rodando = False

        if tela_atual == "jogando":
            atualizar_partida(estado, cenarios, dt)
            if estado["fim"] is not None:
                recorde = finalizar_partida(estado, recorde)
                tela_atual = "fim"
            pygame.display.set_caption(
                f"{TITULO_JOGO} | Pontos: {int(estado['pontos'])} | "
                f"Vidas: {estado['vidas']} | Modo: {estado['modo']}"
            )

        if tela_atual == "menu":
            desenhar_menu(tela, fontes, recorde)
        elif tela_atual == "jogando":
            desenhar_jogo(tela, estado, fontes, recorde)
        elif tela_atual == "pausado":
            desenhar_pausa(tela, estado, fontes, recorde)
        elif tela_atual == "fim":
            desenhar_fim(tela, estado, fontes, recorde)

        pygame.display.flip()

    pygame.quit()
