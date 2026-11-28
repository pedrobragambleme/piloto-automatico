Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na etapa inicial do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível. Consulte o enunciado publicado no Canvas para conhecer o eixo temático e as orientações vigentes.

1. Nome provisório do jogo

Informe o nome provisório do jogo.

Nome: Piloto Automático

2. Integrantes do grupo
Nome 1: Pedro Braga Morgan Bleme - 935798
Nome 2: Thiago Lorenzo - 878677

3. Tema escolhido

Indique qual tema específico o grupo escolheu dentro do eixo temático definido no enunciado.

Tema: Mobilidade inteligente e confiabilidade de sistemas inteligentes: o uso responsável de carros autônomos e a necessidade de supervisão humana.

Como esse tema se relaciona com o jogo? Explique brevemente (2 a 4 linhas) como ele aparecerá nos objetivos, nas regras ou nos desafios, e não apenas nas imagens ou no cenário.

O carro anda sozinho com um piloto automático que desvia de alguns obstáculos, mas não enxerga outros (neblina, placa apagada, carga na pista). O jogador precisa decidir quando confiar na IA e quando assumir o controle manual. Intervir sem necessidade perde pontos e confiar na hora errada custa vidas. Um painel mostra a confiança da IA, que às vezes está alta mesmo quando ela erra.

4. Tipo de jogo

Indique o estilo do jogo. Exemplos: desviar de obstáculos, coleta de itens, labirinto, perguntas e respostas, memória, Pong, Snake, Breakout, corrida ou sobrevivência simples.

Tipo escolhido: Desvio de obstáculos (corrida simples com visão de cima).

5. Descrição geral do jogo

Explique, em poucas linhas, como o jogo funcionará. O que aparece na tela? O que o jogador controla? O que ele precisa fazer e quais desafios encontrará?

Descrição: Na tela aparece uma pista de três faixas rolando na vertical, com o carro na parte inferior e obstáculos descendo. O carro começa no modo automático e desvia sozinho dos obstáculos que a IA detecta. O jogador acompanha o painel (vidas, distância, pontos e confiança da IA) e pode assumir o controle com ESPAÇO para trocar de faixa com as setas. O desafio é perceber, pelo contexto (chuva, neblina, tipo de obstáculo), quando a IA vai falhar. Quando o jogador erra, o jogo mostra uma explicação curta do que aconteceu.

6. Objetivo do jogador

Descreva o objetivo principal. Por exemplo: coletar itens, sobreviver por determinado tempo, chegar ao final de um percurso ou completar desafios.

Objetivo: Percorrer 1000 metros sem perder todas as vidas, intervindo nos momentos certos e deixando a IA dirigir quando for seguro, para fazer a maior pontuação possível.

7. Regras principais

Liste até cinco regras que expliquem o funcionamento do jogo. Exemplos: o jogador começa com três vidas; acertos somam pontos; colisões retiram vidas.

Regra 1: O jogador começa com 3 vidas e cada colisão retira 1 vida.
Regra 2: No modo automático, a IA desvia dos obstáculos que detecta, mas colide com os que não detecta.
Regra 3: No modo manual (tecla ESPAÇO), o jogador troca de faixa com as setas e pode desviar de qualquer obstáculo, porém ganha menos pontos por metro.
Regra 4: Desviar manualmente de um obstáculo que a IA não veria dá bônus de pontos; assumir o controle sem necessidade tira pontos.
Regra 5: A cada 250 metros o nível sobe, aumentando a velocidade e as condições difíceis (chuva, neblina, noite).
8. Condição de vitória

Explique como o jogador vence ou conclui a partida. Exemplos: alcançar uma pontuação, finalizar uma fase ou completar todas as tarefas.

Condição de vitória: Completar 1000 metros com pelo menos 1 vida restante.

9. Condição de derrota ou encerramento

Explique quando a partida termina ou como o jogador perde. Exemplos: esgotar as vidas, acabar o tempo ou atingir o limite de erros.

Condição de derrota ou encerramento: A partida termina em derrota quando as 3 vidas acabam. Ao final (vitória ou derrota), uma tela mostra distância, pontuação, intervenções corretas e desnecessárias e o recorde salvo, com opção de jogar de novo (R) ou sair (ESC).

10. Elementos previstos no jogo

Descreva brevemente os elementos mais importantes, sem precisar detalhar a implementação.

Personagem ou elemento principal: carro autônomo, que alterna entre modo automático e manual.
Obstáculos ou desafios: cones, carro parado, carga caída, pedestre e placa apagada, em condições de pista normal, chuva, neblina ou noite. Alguns a IA detecta e outros não.
Itens ou objetos de interação (se houver): painel de confiança da IA com o motivo (ex.: "visibilidade baixa") e mensagens explicativas após os erros.
Pontuação, vidas, tempo ou progresso: vidas, distância percorrida (até 1000 m), pontuação, nível e recorde.
11. Controles previstos

Informe como o jogador vai interagir com o jogo (por exemplo, setas para movimentar, espaço para agir ou mouse para selecionar).

Controles: Setas esquerda e direita para trocar de faixa (no modo manual), ESPAÇO para alternar entre automático e manual, P para pausar, ENTER para iniciar, R para reiniciar e ESC para sair.

12. Principais dificuldades esperadas

Cite até três dificuldades que o grupo espera enfrentar. Exemplos: movimentação, colisões, controle de tempo, testes ou uso do GitHub.

Dificuldade 1: Fazer as colisões e a troca de faixa funcionarem de forma estável.
Dificuldade 2: Equilibrar a dificuldade, dando tempo ao jogador para perceber o risco e intervir.
Dificuldade 3: Separar a lógica do jogo do código de desenho para conseguir testar, e trabalhar em grupo no GitHub sem conflitos.
13. Escopo mínimo para a entrega final

Descreva a versão mais simples que já seria jogável, com as interações e regras essenciais. Evite planejar funcionalidades demais.

Escopo mínimo: Janela Pygame com menu inicial e pista de três faixas, carro e obstáculos descendo. Alternância entre modo automático e manual, com obstáculos que a IA detecta e que não detecta. Pontuação, 3 vidas, níveis, vitória aos 1000 m e derrota sem vidas. Pelo menos 8 tipos de obstáculo lidos de um arquivo JSON, explicação após os erros e recorde salvo em arquivo. Testes das funções de lógica, README e proposta atualizados.

14. Possíveis melhorias, caso haja tempo

Liste até três funcionalidades extras para implementar somente depois que a versão mínima estiver funcionando. Exemplos: sons, fases, ranking, animações ou menu inicial.

Melhoria 1: Efeitos sonoros e alerta sonoro quando a confiança da IA estiver baixa.
Melhoria 2: Efeitos visuais de chuva e neblina e fases com cenários diferentes (cidade, estrada, túnel).
Melhoria 3: Ranking com os cinco melhores resultados e resumo dos tipos de situação em que o jogador mais errou.
15. Informações complementares (exigidas pelo Ponto de controle 01)
Organização inicial do código

O projeto foi desenvolvido sobre o template da disciplina, mantendo sua estrutura de pastas. Módulos (atualizados na Entrega 2; os nomes foram adaptados ao template):

main.py: ponto de entrada do jogo.
src/jogo.py: loop principal, entrada do teclado e controle de telas (menu, jogo, pausa, fim).
src/partida.py: estado da partida e regras por quadro (obstáculos, piloto automático, colisões, pontuação).
src/funcoes.py: funções puras de lógica (colisão, pontos, nível, vitória/derrota, escolha de faixa, confiança da IA).
src/obstaculos.py: criação e consulta de obstáculos.
src/interface.py: desenho de pista, carro, obstáculos, painel e telas.
src/dados.py: leitura e escrita de recorde e leitura dos cenários (JSON).
src/config.py: constantes do jogo (tela, pista, regras, pesos de condição).
data/cenarios.json e data/recorde.txt: arquivos auxiliares.
tests/test_logica.py, tests/test_dados.py e tests/test_partida.py: testes das funções de lógica, dos arquivos e de partidas simuladas.

Estruturas de dados
Dicionários: cada obstáculo (tipo, condicao, ia_detecta, explicacao) e o estado do jogo (vidas, distância, pontos, modo, nível).
Listas: obstáculos ativos na pista e tipos de obstáculo disponíveis.
Tuplas: cores RGB, posições e tamanhos.
Conjuntos: modos válidos ({"auto", "manual"}).
Uso de arquivos
Leitura de data/cenarios.json com os tipos de obstáculos, condições e explicações.
Leitura e escrita de data/recorde.txt para salvar a melhor pontuação. Se o arquivo não existir, o recorde começa em 0.
Funções principais previstas

carregar_cenarios, criar_obstaculo, ia_desvia, calcular_confianca, houve_colisao, faixa_livre_mais_proxima, avaliar_passagem, pontos_por_distancia, pontos_por_evento, calcular_nivel, verificar_fim, carregar_recorde, salvar_recorde, desenhar_painel e desenhar_pista.

Testes planejados

Testes simples em tests/ para:

ia_desvia: verdadeiro para obstáculo detectável e falso para não detectável.
houve_colisao: detecta sobreposição e ausência dela.
pontos_por_evento: bônus por intervenção correta e penalidade por intervenção desnecessária.
calcular_nivel: sobe de nível nas distâncias esperadas.
verificar_fim: detecta vitória (1000 m) e derrota (0 vidas).
carregar_recorde: retorna 0 quando o arquivo não existe.
Recursos necessários

Python 3 e Pygame, formas geométricas e fontes padrão do Pygame. Os textos dos cenários serão escritos pelo grupo. Qualquer imagem, som, fonte ou código externo será listado no README com origem e licença.

Declaração de originalidade

Declaramos que a ideia, as regras, os textos dos cenários e o código deste jogo serão desenvolvidos pelo grupo especificamente para esta disciplina e não reaproveitam jogos de semestres anteriores. Qualquer recurso externo será identificado no README.md com sua origem e, quando possível, licença. Todos os integrantes saberão explicar as partes em que trabalharam.

Atualização da Entrega 2
Mudanças em relação à proposta inicial: (1) os módulos seguem os nomes do template (funcoes.py, dados.py e jogo.py) e foram acrescentados partida.py, obstaculos.py e interface.py; (2) a condição da pista (normal, chuva, neblina, noite) muda a cada 100 m e define quais obstáculos surgem, com 15 cenários no data/cenarios.json; (3) uma intervenção é avaliada como correta quando o jogador estava no modo manual diante de um obstáculo que a IA não detectava (+20), e como desnecessária quando a IA já detectava (-10); (4) a IA só muda para uma faixa se o caminho até ela estiver livre. O escopo e as regras principais continuam os mesmos.

Atualização da Entrega 3
Versão final do jogo. O grupo final é formado por Pedro Braga Morgan Bleme e Thiago Lorenzo. Mudanças e resultados em relação à proposta e à Entrega 2: (1) a IA passou a mostrar o que enxerga: um quadro verde com o texto "IA detectou" aparece sobre cada obstáculo detectado, e obstáculo sem quadro é um obstáculo que a IA não viu; uma linha pontilhada marca o alcance da câmera da IA e o painel mostra a visibilidade da IA (boa, reduzida ou baixa) conforme a condição da pista; (2) o painel ganhou legenda fixa e o menu inicial explica o quadro verde; (3) a dificuldade foi ajustada após testes de jogo (velocidade, intervalo entre obstáculos e efeitos de chuva, neblina e noite); (4) os caminhos dos arquivos passaram a partir da pasta do projeto, e o jogo funciona de qualquer pasta; (5) a suíte de testes chegou a 63 testes de lógica, incluindo partidas simuladas, leitura de arquivos, alcance e visibilidade da IA.

Escopo entregue: tela principal, controle do carro, mecânica central de supervisionar o piloto automático, vidas, pontos, distância, nível e recorde, vitória aos 1000 m e derrota sem vidas, 15 cenários em arquivo JSON, mensagens educativas após colisões e intervenções, menu, pausa e tela final. A integração com o tema é verificável na jogabilidade: a IA só desvia do que detecta, a condição da pista muda o que ela enxerga, a confiança mostrada pode estar alta mesmo quando ela erra, e o jogador ganha ou perde pontos conforme intervém no momento certo ou não.

Melhorias possíveis: sons e imagens autorais, mais cenários e condições de pista, ranking com várias pontuações e dificuldade selecionável no menu.

Recursos externos: Pygame, pytest e o template da disciplina, além do assistente de IA Claude (Anthropic), usado como apoio de programação. Todos estão identificados no README.md, com origem e licença. O grupo testou o jogo e revisou o código, e todos os integrantes devem saber explicar as partes do projeto.
