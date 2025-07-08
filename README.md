# Projeto: Minecraft Stats Tracker via Discord

Este projeto foi criado como uma forma divertida de aplicar e expandir conhecimentos em diversas áreas da programação, integrando um bot do Discord, um servidor de Minecraft, um banco de dados e uma aplicação web para criar um sistema completo de ranking e estatísticas de jogadores.

## Principais Funcionalidades

- **Integração com Discord:** Use comandos simples (`!mine`, `!server`) para iniciar o jogo e o servidor diretamente pelo Discord.

- **Coleta de Estatísticas:** Um plugin customizado para o Minecraft coleta dados em tempo real sobre a performance dos jogadores.

- **Ranking de Jogadores:** Um sistema de pontos, baseado nos itens coletados, define quem é o jogador mais valioso do servidor.

- **Dashboard Web:** Uma página web exibe todas as estatísticas, horas jogadas e o ranking geral dos participantes.

- **Conquistas e Níveis:** Atribui status aos jogadores (Ex: "Exterminador de Monstros", "Minerador Nível 4") com base em suas ações no jogo.

## Fluxo de Funcionamento

1. **Comando no Discord:** O administrador do servidor utiliza o comando `!server` para iniciar o servidor de Minecraft. Cada jogador usa `!mine` para abrir seu próprio jogo.

2. **Execução via Script:** O bot aciona scripts locais que executam o servidor e o cliente do Minecraft.

3. **Coleta de Dados (Plugin):** Dentro do jogo, um plugin em Java monitora as atividades de cada jogador (itens, mortes, monstros abatidos, tempo online) e envia esses dados.

4. **Armazenamento (Banco de Dados):** As informações coletadas alimentam um banco de dados SQLite.

5. **Visualização (Aplicação Web):** Uma aplicação web, hospedada na nuvem, lê os dados do banco e os exibe em uma interface amigável, calculando pontos e atualizando o ranking.

## Tecnologias Utilizadas

- **Bot:** Python (`discord.py`)

- **Backend:** Python (`Flask` ou `Django`)

- **Frontend:** `HTML`, `CSS`, `JavaScript`

- **Plugin Minecraft:** `Java` (Spigot/Bukkit API)

- **Banco de Dados:** `SQLite`

- **Hospedagem:** `Render`

## Conceitos Aplicados

- Automação de tarefas com scripts.

- Desenvolvimento de APIs para comunicação entre serviços.

- Criação e gerenciamento de banco de dados.

- Desenvolvimento Full-Stack (Backend e Frontend).

- Modding de jogos (Minecraft Plugin).

- Integração e deploy de aplicações na nuvem.

---
