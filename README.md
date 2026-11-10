# taskbot

Starting point of the running project of the course **Coding Agents, Open Models and Security**.

This repository starts **almost empty on purpose**: you will build `taskbot` (a task CLI in Python) with the help of a coding agent.

## Getting started

1. Clone the repo:
   ```bash
   git clone https://github.com/professordiogodev/taskbot.git
   cd taskbot
   git switch -c my-taskbot
   ```
2. Open **[LAB.md](LAB.md)** and follow the steps in order.

## What you will build

```bash
taskbot add "study agents"
taskbot list
taskbot done 1
taskbot rm 1
```

With JSON persistence, tests, a context file for the agent, and priorities.

## Requirements

`git`, `python3` (3.10+), `node` (20+), [`uv`](https://docs.astral.sh/uv/), and a coding agent: **Claude Code** or **OpenCode**.

> This repo does not contain the solution. The goal is for you to learn the workflow: *Explore → Plan → Implement → Verify → Commit*.
