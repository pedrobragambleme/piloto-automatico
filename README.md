# Piloto Automático

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Jogo sobre **IA no cotidiano e uso responsável**, com foco em mobilidade inteligente: você acompanha um carro autônomo e precisa decidir quando confiar no piloto automático e quando assumir o controle.

> Status: versão final (Entrega 3). Proposta em `docs/proposta.MD`.

## Integrantes do grupo

* Pedro Braga Morgan Bleme - 935798
* Thiago Lorenzo - 878677

## Estrutura do projeto

* `main.py`: ponto de entrada da aplicação.
* `src/`: código-fonte principal do jogo:
  * `jogo.py`: loop principal, teclado e telas (menu, jogo, pausa, fim);
  * `partida.py`: estado da partida e regras a cada quadro;
  * `funcoes.py`: funções puras de lógica (colisão, pontos, nível, fim de jogo, piloto automático);
  * `obstaculos.py`: criação e consulta de obstáculos;
  * `interface.py`: desenho da pista, do painel e das telas;
  * `dados.py`: leitura/escrita do recorde e leitura dos cenários;
  * `config.py`: constantes do jogo.
* `assets/`: imagens, fontes e sons.
* `data/`: arquivos persistentes (`recorde.txt` e `cenarios.json`, com os obstáculos e suas explicações).
* `tests/`: testes unitários com `pytest`.
* `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

O carro anda sozinho por uma pista de três faixas, com obstáculos descendo. O piloto automático desvia de alguns obstáculos, mas não enxerga outros (neblina, placa apagada, carga na pista). Na pista, um **quadro verde** marca os obstáculos que a IA detectou; os que ficam **sem quadro** são os que ela não viu. O painel mostra a visibilidade da IA, a confiança e o motivo, mas a confiança nem sempre é confiável. O jogador precisa observar o contexto e decidir quando deixar a IA dirigir e quando assumir o controle manual. Quando erra, o jogo mostra uma explicação curta do que aconteceu.

## Objetivo do jogador

Percorrer 1000 metros sem perder todas as vidas, intervindo nos momentos certos e deixando a IA dirigir quando for seguro, para fazer a maior pontuação possível.

## Regras do jogo

* O jogador começa com 3 vidas e cada colisão retira 1 vida.
* No modo automático, a IA desvia dos obstáculos que detecta, mas colide com os que não detecta.
* No modo manual, o jogador troca de faixa com as setas e pode desviar de qualquer obstáculo, mas ganha menos pontos por metro.
* Desviar manualmente de um obstáculo que a IA não veria dá bônus de pontos; assumir o controle sem necessidade tira pontos.
* A cada 250 metros o nível sobe, aumentando a velocidade e as condições difíceis (chuva, neblina, noite).
* Vitória: completar 1000 metros com pelo menos 1 vida. Derrota: perder as 3 vidas.

## Controles

* Seta para esquerda: mudar para a faixa da esquerda (modo manual)
* Seta para direita: mudar para a faixa da direita (modo manual)
* Espaço: alternar entre modo automático e manual
* P: pausar
* Enter: iniciar
* R: reiniciar
* ESC: sair do jogo

## Como o jogo funciona

* O carro anda sozinho. Um **quadro verde** com o texto "IA detectou" aparece sobre cada obstáculo que a IA enxerga e vai desviar. **Sem quadro, a IA não viu o obstáculo**: é o momento de assumir o controle.
* O painel mostra a **visibilidade da IA** (boa, reduzida ou baixa, conforme a pista) e a **leitura da IA** na faixa do carro (o que ela acha que está à frente e a confiança em %). A confiança nem sempre é confiável: em alguns casos a IA está muito confiante e não viu o obstáculo.
* A **condição da pista** (normal, chuva, neblina ou noite) muda a cada 100 m e define quais obstáculos aparecem. Quanto pior a visibilidade, mais a IA falha.
* No **modo automático** vale 1 ponto por metro; no **manual**, 0,5. Intervir quando a IA falharia dá **+20**; intervir quando ela já detectava o obstáculo custa **-10**.
* Depois de cada batida, o jogo explica por que a IA errou. O nível sobe a cada 250 m (mais velocidade e mais condições difíceis).
* O recorde é salvo em `data/recorde.txt`.

## Como executar o projeto

Requisitos: Python 3.13 (ou outro Python 3 recente) e as bibliotecas de `requirements.txt` (`pygame` e `pytest`).

```
git clone https://github.com/pedrobragambleme/piloto-automatico.git
cd piloto-automatico
pip install -r requirements.txt
python main.py
```

No Windows, se o comando `python` não for reconhecido, use o lançador `py`, por exemplo `py -3.13 -m pip install -r requirements.txt` e `py -3.13 main.py`. O jogo pode ser executado de qualquer pasta, pois os arquivos de `data/` são localizados a partir da pasta do projeto.

## Como executar os testes

```
python -m pytest
```

São 63 testes de lógica (colisão, pontos, nível, fim de jogo, piloto automático, leitura de arquivos e partidas simuladas). Eles não abrem janela e não dependem do Pygame para rodar.

## Conceitos da disciplina utilizados

* Variáveis, entrada e saída: teclado, título da janela e painel na tela.
* Condicionais e laços: loop principal do jogo e regras avaliadas a cada quadro.
* Listas: obstáculos ativos na pista e cenários carregados do arquivo.
* Dicionários: estado da partida, obstáculos e cenários.
* Tuplas e conjuntos: cores RGB, retângulos de colisão e modos válidos.
* Funções e modularização: lógica pura em `funcoes.py`, `obstaculos.py` e `partida.py`, separada do desenho em `interface.py`.
* Arquivos: leitura de `data/cenarios.json` e leitura/escrita de `data/recorde.txt`.
* Documentação e testes: docstrings, este README, `docs/proposta.MD` e testes com `pytest`.

## Recursos externos utilizados

* **Template da disciplina**: [IntroAlgs_pygame_template](https://github.com/ICEI-PUC-Minas-PPL-CDIA/IntroAlgs_pygame_template) (ICEI PUC Minas), usado como base da estrutura de pastas e arquivos.
* **Pygame** (https://www.pygame.org), biblioteca de jogos em Python, licença LGPL.
* **pytest** (https://pytest.org), biblioteca de testes, licença MIT.
* **Python** (https://www.python.org), licença PSF.
* **Claude (Anthropic)**, assistente de IA usado como apoio de programação durante o desenvolvimento: sugestões de organização do código, escrita e revisão de funções e testes, e redação da documentação. O código foi testado e revisado pelo grupo, e os integrantes sabem explicar o seu funcionamento.
* **Imagens, sons e fontes**: nenhum recurso externo. Os desenhos (carro, obstáculos, pista, quadros da IA) são formas geométricas feitas com o próprio Pygame, e a fonte é a padrão do Pygame. Os textos e os 15 cenários de `data/cenarios.json` foram escritos pelo grupo para este jogo.

O arquivo `assets/imagens/spritesheet.bmp` e o módulo `src/sprites.py` vêm do template e não são usados no jogo.

## Checklist mínimo para entrega

* [x] Preencher este README com nome final, descrição real, regras e controles do jogo.
* [x] Atualizar `docs/proposta.md` com a proposta do grupo.
* [x] Garantir que o jogo executa com `python main.py`.
* [x] Garantir que os testes passam com `pytest`.