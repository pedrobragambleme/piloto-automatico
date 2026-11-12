# Piloto Automático

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Jogo sobre **IA no cotidiano e uso responsável**, com foco em mobilidade inteligente: você acompanha um carro autônomo e precisa decidir quando confiar no piloto automático e quando assumir o controle.

> Status: em desenvolvimento (Ponto de controle 01 – proposta definida em `docs/proposta.md`).

## Integrantes do grupo

* [Pedro Braga Morgan Bleme - 935798]
* [Matheus Fernandes de Oliveira - 932354]

## Estrutura do projeto

* `main.py`: ponto de entrada da aplicação.
* `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
* `assets/`: imagens, fontes e sons.
* `data/`: arquivos persistentes (recorde/ranking e cenários).
* `tests/`: testes unitários com `pytest`.
* `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

O carro anda sozinho por uma pista de três faixas, com obstáculos descendo. O piloto automático desvia de alguns obstáculos, mas não enxerga outros (neblina, placa apagada, carga na pista). Um painel mostra a confiança da IA e o motivo, mas a confiança nem sempre é confiável. O jogador precisa observar o contexto e decidir quando deixar a IA dirigir e quando assumir o controle manual. Quando erra, o jogo mostra uma explicação curta do que aconteceu.

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

## Como executar o projeto

1. Clonar o repositório

```
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```
python -m pytest
```

## Recursos externos utilizados

Nenhum até o momento. Qualquer imagem, som, fonte, trecho de código ou tutorial usado será listado aqui com origem e, quando possível, licença.

## Checklist mínimo para entrega

* [ ] Preencher este README com nome final, descrição real, regras e controles do jogo.
* [x] Atualizar `docs/proposta.md` com a proposta do grupo.
* [ ] Garantir que o jogo executa com `python main.py`.
* [ ] Garantir que os testes passam com `pytest`.

## Observações para os alunos

* Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
* Comentem partes importantes da lógica, principalmente regras do jogo.
* Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
