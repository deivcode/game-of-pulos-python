# Documentação dos Arquivos CSV do Jogo

Este documento explica o propósito de cada arquivo `.csv` encontrado na pasta raiz do projeto, que são utilizados para construir os diferentes elementos do mapa do jogo.

## Como Funcionam os Arquivos CSV

Cada arquivo `.csv` representa uma "camada" do nosso mapa. Os números dentro desses arquivos correspondem a IDs de tiles (pequenas imagens) que são carregados pelo jogo. O valor `-1` geralmente significa que não há nenhum tile naquela posição, deixando-a vazia.

Esses arquivos são lidos pela função `build()` no `platformer.py`, que os transforma em objetos `Actor` no jogo, posicionando-os corretamente na tela.

## Arquivos CSV e Seus Propósitos

### `plataformer_arvore .csv`
Este arquivo define a estrutura principal das árvores no cenário. Ele contém os IDs dos tiles que formam os troncos e as partes maiores das árvores.

### `plataformer_final.csv`
Este CSV marca a posição do objetivo final do jogo. Quando o jogador alcança os tiles definidos neste arquivo, ele completa o nível.

### `plataformer_galhos.csv`
Este arquivo define a posição dos galhos das árvores. Recentemente, a lógica do jogo foi atualizada para que esses galhos sejam sólidos, permitindo que o jogador suba neles.

### `plataformer_ground.csv`
Contém os tiles que formam o chão principal do jogo, onde o jogador começa e se move na maior parte do tempo.

### `plataformer_jumps.csv`
Este CSV especifica a localização de tiles especiais que dão ao jogador um "super pulo" quando ele colide com eles.

### `plataformer_mushroms.csv`
Define a posição dos cogumelos no mapa. Eles podem ser apenas decorativos ou ter alguma interação específica no jogo.

### `plataformer_Plano-de-Fundo.csv`
Este arquivo é usado para definir elementos de fundo que não interagem com o jogador, como montanhas distantes ou nuvens, criando profundidade no cenário.

### `plataformer_plataforma-lado.csv`
Contém os tiles que formam as plataformas que se movem horizontalmente no jogo, adicionando um desafio extra ao jogador.

### `plataformer_Plataformas.csv`
Define a localização das plataformas fixas no jogo, que o jogador usa para pular e alcançar diferentes áreas.

### `plataformer_recompensas.csv`
Este CSV indica onde as recompensas (como moedas ou joias) estão localizadas no mapa, para o jogador coletar.