# taskbot

Ponto de partida do projeto-fio-condutor do curso **Agentes de Código, Modelos Abertos e Segurança**.

Este repositório começa **quase vazio de propósito**: vais construir o `taskbot` (uma CLI de tarefas em Python) com a ajuda de um agente de código.

## Como começar

1. Clona o repo:
   ```bash
   git clone https://github.com/professordiogodev/taskbot.git
   cd taskbot
   git switch -c meu-taskbot
   ```
2. Abre **[LAB.md](LAB.md)** (Aula 1) ou **[LAB3.md](LAB3.md)** (Aula 3 — MCP + RAG + CI) e segue os passos pela ordem.
3. Instala as dependências: `uv sync`

## O que vais construir

```bash
taskbot add "estudar agentes"
taskbot list
taskbot done 1
taskbot rm 1
```

Com persistência em JSON, testes, ficheiro de contexto para o agente e prioridades.

## Requisitos

`git`, `python3` (3.10+), `node` (20+), [`uv`](https://docs.astral.sh/uv/), e um agente de código: **Claude Code** ou **OpenCode**.

> Este repo não tem a solução. O objetivo é aprenderes o fluxo: *Explorar → Planear → Implementar → Verificar → Commit*.
