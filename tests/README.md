# Testes

Esta pasta contem testes automatizados do projeto.

## Arquivos

- `test_logica.py`: funcoes puras de logica em `src/funcoes.py` (colisao, pontos, nivel, fim de jogo, piloto automatico, visibilidade da IA).
- `test_dados.py`: recorde e leitura dos cenarios (`data/cenarios.json`).
- `test_obstaculos.py`: alcance da câmera da IA sobre os obstaculos (`no_alcance_da_ia`).
- `test_partida.py`: partidas simuladas em `src/partida.py` (IA desviando, IA batendo, intervencoes do jogador, vitoria e derrota).

## Como executar

```bash
python -m pytest
```

## Boas praticas

- Crie testes para toda regra de pontuacao, vidas e condicoes de fim de jogo.
- Prefira funcoes pequenas e testaveis, sem depender do Pygame.