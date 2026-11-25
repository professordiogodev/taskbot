# taskbot

Ponto de partida do projeto-fio-condutor do curso **Agentes de Código, Modelos Abertos e Segurança**.

O `taskbot` é uma CLI de tarefas em Python (Typer), construída com a ajuda de um agente de código, com persistência em JSON, prioridades e testes.

## Como começar

1. Clona o repo:
   ```bash
   git clone https://github.com/professordiogodev/taskbot.git
   cd taskbot
   git switch -c meu-taskbot
   ```
2. Segue o guião do lab fornecido pelo professor.
3. Instala as dependências: `uv sync`

## Como usar

```bash
uv sync                      # instala as dependências e o comando `taskbot` na .venv
source .venv/bin/activate    # ou usa `uv run taskbot ...` sem ativar

taskbot add "estudar agentes" -p high   # prioridade: low/med/high (por defeito: med)
taskbot list                            # lista as tarefas, high primeiro
taskbot done 1                          # marca a tarefa 1 como concluída
taskbot rm 1                            # remove a tarefa 1
taskbot --help
```

As tarefas são guardadas em `~/.taskbot.json`. Para usar outro ficheiro, define `TASKBOT_FILE`:

```bash
TASKBOT_FILE=./tarefas.json taskbot list
```

Testes: `.venv/bin/python -m pytest -q`

## Requisitos

`git`, `python3` (3.10+), `node` (20+), [`uv`](https://docs.astral.sh/uv/), e um agente de código: **Claude Code** ou **OpenCode**.

> O objetivo é aprenderes o fluxo: *Explorar → Planear → Implementar → Verificar → Commit*.
