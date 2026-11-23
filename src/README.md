# Código-fonte (`src`)

Esta pasta contém os módulos principais do jogo.

## Arquivos

- `jogo.py`: loop principal, eventos de teclado e controle de telas.
- `partida.py`: estado da partida e regras atualizadas a cada quadro (sem Pygame).
- `funcoes.py`: funções puras de regra e lógica (sem Pygame).
- `obstaculos.py`: criação e consulta de obstáculos (sem Pygame).
- `interface.py`: desenho da pista, do carro, dos obstáculos, do painel e das telas.
- `dados.py`: leitura e gravação de dados (recorde e cenários).
- `config.py`: constantes globais (tela, pista, regras, cores, caminhos).
- `sprites.py`: recorte de spritesheet (herdado do template, não usado nesta versão).

## Dica de evolução

Mantenha a lógica (`partida.py`, `funcoes.py`, `obstaculos.py`) separada do desenho (`interface.py`), pois assim ela pode ser testada sem abrir janela.
