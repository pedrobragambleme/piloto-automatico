# Piloto Automático

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Jogo sobre **IA no cotidiano e uso responsável**, com foco em mobilidade inteligente: você acompanha um carro autônomo e precisa decidir quando confiar no piloto automático e quando assumir o controle.

> Status: versão parcial jogável (Entrega 2). Proposta em `docs/proposta.MD`.

## Integrantes do grupo

* Pedro Braga Morgan Bleme - 935798
* Matheus Fernandes de Oliveira - 932354
* Thiago Lorenzo - 

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

## Como o jogo funciona

* O carro anda sozinho. O painel mostra a **leitura da IA** (o que ela acha que está à frente e a confiança em %), mas a confiança nem sempre é confiável: em alguns casos a IA está muito confiante e não viu o obstáculo.
* A **condição da pista** (normal, chuva, neblina ou noite) muda a cada 100 m e define quais obstáculos aparecem. Quanto pior a visibilidade, mais a IA falha.
* No **modo automático** vale 1 ponto por metro; no **manual**, 0,5. Intervir quando a IA falharia dá **+20**; intervir quando ela já detectava o obstáculo custa **-10**.
* Depois de cada batida, o jogo explica por que a IA errou. O nível sobe a cada 250 m (mais velocidade e mais condições difíceis).
* O recorde é salvo em `data/recorde.txt`.

## Como executar o projeto

1. Clonar o repositório

```
git clone https://github.com/pedrobragambleme/piloto-automatico.git
cd piloto-automatico
pip install -r requirements.txt
python main.py
```

Execute sempre a partir da pasta raiz do projeto, pois os arquivos de `data/` são lidos por caminho relativo.

## Como executar os testes

```
python -m pytest
```

## Recursos externos utilizados

Nenhum até o momento. Os desenhos (carro, obstáculos, pista) são formas geométricas feitas com o próprio Pygame, e a fonte é a padrão do Pygame. Qualquer imagem, som, fonte, trecho de código ou tutorial usado no futuro será listado aqui com origem e, quando possível, licença.

O arquivo `assets/imagens/spritesheet.bmp` e o módulo `src/sprites.py` vêm do template e não são usados nesta versão.

## Checklist mínimo para entrega

* [x] Preencher este README com nome final, descrição real, regras e controles do jogo.
* [x] Atualizar `docs/proposta.md` com a proposta do grupo.
* [ ] Garantir que o jogo executa com `python main.py`.
* [ ] Garantir que os testes passam com `pytest`.

## Observações para os alunos

* Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
* Comentem partes importantes da lógica, principalmente regras do jogo.
* Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
