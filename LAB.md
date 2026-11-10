# LAB — Build `taskbot` with a coding agent

**Time:** 45-60 min · **Level:** beginner · **Class 1 — homework**

You will build a small task CLI (`taskbot add`, `list`, `done`, `rm`) **with the help of a coding agent**, following the professional workflow:

```
Explore → Plan → Implement → Verify → Commit
```

This project continues in classes 2 to 7 (guardrails, MCP/RAG, CI, open models, fine-tuning, security). **Keep it safe.**

> **Legend**
> 🟠 = Claude Code · 🟣 = OpenCode (use only one)
> 💻 = type in the **terminal** · 💬 = type **inside the agent**
> ✅ = how to tell it went well · 🆘 = if something goes wrong

---

## Before you start

You need: `git`, `python3` (3.10+), `node` (20+), `uv`, and an agent (🟠 Claude Code or 🟣 OpenCode) already connected to a model.

```bash
git --version && python3 --version && node --version && uv --version
```
✅ All four print a version.

Missing something? Follow the class 1 `passo-a-passo.md` (Part 0), or:
- `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh` (then reopen the terminal)
- 🟠 `npm install -g @anthropic-ai/claude-code`
- 🟣 `curl -fsSL https://opencode.ai/install | bash` and inside it `/connect` + `/models`

First time with git? `git config --global user.name "Your Name"` and `git config --global user.email "your@email.com"`.

> ⚠️ **Free model?** It may collect data. Nothing in this lab is confidential, but never use work code.

---

## Step 1 — Set up the project (5 min)

### 1.1 Clone this repo
```bash
git clone https://github.com/professordiogodev/taskbot.git
cd taskbot
git switch -c my-taskbot
```

### 1.2 Initialize the Python project
```bash
uv init --package --name taskbot
uv add typer
uv add --dev pytest ruff
```

✅ Now `pyproject.toml` and `src/taskbot/` exist. Check:
```bash
ls
ls src/taskbot
```

### 1.3 First commit
```bash
git add -A
git commit -m "chore: bootstrap"
git status
```
✅ `git status` says *"nothing to commit, working tree clean"*.

🆘 `uv init` says a project already exists? Are you in the right folder? (`pwd` should end in `taskbot`.)

> 💡 **Course rule:** always start each task with a clean git tree. If the agent makes a mess, `git restore .` puts everything back.

---

## Step 2 — Give the agent context (10 min)

### 2.1 Open the agent in the project folder
🟠 💻 `claude` · 🟣 💻 `opencode`

### 2.2 Generate the draft context file
💬 `/init`

- 🟠 creates `CLAUDE.md` · 🟣 creates `AGENTS.md`
- Accept the permissions it asks for (read what it asks!).

### 2.3 Trim the file to ~25 lines
Open it in your editor. The draft is almost always too long. Keep **only**:

```markdown
# taskbot
Task CLI in Python 3.10+. Package manager: uv. CLI with Typer.

## Commands
- Tests: `uv run pytest -q`
- Lint and format: `uv run ruff check . && uv run ruff format .`
- Run the CLI: `uv run taskbot --help`

## Architecture
- `src/taskbot/models.py` — Task dataclass
- `src/taskbot/store.py` — JSON persistence (TASKBOT_FILE variable)
- `src/taskbot/cli.py` — Typer commands

## Rules
- Public functions with type hints and a test in `tests/`.
- Do not add dependencies without asking.
- Never change existing tests to make them pass.
```

> 🧠 For each line ask: *"If I delete this, will the agent get it wrong?"* If not, delete it.

### 2.4 Confirm the commands are true
```bash
uv run ruff check .
uv run pytest -q
```
(`pytest` may say "no tests ran": that's normal for now.)

### 2.5 Save
```bash
git add -A
git commit -m "docs: add context file"
```

✅ **Checkpoint 2:** context file with ≤ 40 lines and commit done.

---

## Step 3 — Plan before coding (10 min)

### 3.1 Enter plan mode
The agent only **reads and proposes**, it does not edit.
- 🟠 `Shift + Tab` until **plan mode** appears
- 🟣 `Tab` until the active agent is **Plan**

### 3.2 Ask for the plan
💬
```
I want a task CLI called taskbot with the commands:
  add "text"   → creates a task
  list         → lists tasks (id and status)
  done <id>    → marks as completed
  rm <id>      → removes
Persistence in a JSON file (path via the TASKBOT_FILE environment variable,
default ~/.taskbot.json). Use Typer.
Ask me whatever questions you need and then propose a plan:
files, functions, tests, risks. Do not write code.
```

### 3.3 Answer the questions and read the whole plan
### 3.4 Add **one correction of your own**
For example:
💬
```
Add to the plan: ids are incremental and are never reused, even after an rm.
The store must be testable without touching the user's real file.
```

✅ **Checkpoint 3:** the plan mentions `TASKBOT_FILE`, tests, and your correction.

> 💡 Fixing a plan takes 20 seconds. Fixing 200 wrong lines takes 20 minutes.

---

## Step 4 — Implement and verify, step by step (20 min)

Leave plan mode (🟠 `Shift+Tab` · 🟣 `Tab` → **Build**). Do **one step at a time** and one commit per step.

### 4.1 Model and store
💬
```
Implement models.py and store.py (with store tests in tests/test_store.py). Run the tests.
```
Check **yourself**:
```bash
git diff
uv run pytest -q
uv run ruff check .
```
Questions to ask while reading the `git diff`:
- Do the tests really test what matters (ids never reused, missing file)?
- Does any test touch the real `~/.taskbot.json` file? (It shouldn't.)

```bash
git add -A
git commit -m "feat: task store"
```

### 4.2 CLI
💬
```
Implement the CLI in cli.py with the commands add, list, done and rm, and tests using typer.testing.CliRunner. Run the tests and ruff.
```
Check:
```bash
git diff
uv run pytest -q
uv run ruff check .
git add -A
git commit -m "feat: cli"
```

### 4.3 Try it by hand
```bash
export TASKBOT_FILE=/tmp/taskbot-test.json
uv run taskbot add "study agents"
uv run taskbot add "read AGENTS.md"
uv run taskbot list
uv run taskbot done 1
uv run taskbot list
uv run taskbot rm 2
uv run taskbot list
```
✅ **Checkpoint 4:** tasks show up, get completed, and are removed; tests green; ≥ 2 new commits.

🆘 The `taskbot` command doesn't exist? 💬 `The taskbot entry point doesn't work. Fix pyproject.toml and show me what you changed.`
🆘 The agent "fixed" things by changing tests? `git restore .` and repeat, adding *"do not change existing tests"*.

---

## Step 5 — A feature with the full workflow: priorities (10 min)

### 5.1 New conversation
🟠 `/clear` · 🟣 `/new`  (you changed task → new conversation). Confirm `git status` is clean.

### 5.2 Plan mode and request
💬
```
Add a priority field (low/med/high, default med) to tasks.
`add` gets an --priority/-p option. `list` sorts by priority (high first) and shows it.
Old JSON files without priority must keep working (assume med).
Write the failing tests first, then implement.
Verify with pytest and ruff.
```

### 5.3 Approve the plan, implement, read the diff
```bash
git diff
uv run pytest -q
uv run ruff check .
```

### 5.4 The point a vague request would forget
Is there **a test for old JSON files** (without `priority`)? If not, 💬:
```
Add a test for an old JSON file without the priority field.
```

```bash
git add -A
git commit -m "feat: task priorities"
```

✅ **Checkpoint 5:** a backward-compatibility test exists and passes.

---

## Step 6 — Fine-tune the context (5 min)

Was there a mistake the agent repeated (wrong command, ignored convention)?
1. Add **one concrete rule** to the context file.
2. Remove **one useless line**.
3. Commit:
```bash
git add -A
git commit -m "docs: refine context file"
```

---

## Step 7 — Publish to YOUR GitHub (5 min)

You will need this in **class 3** (CI on GitHub).

```bash
gh auth login          # only if you haven't yet
gh repo create taskbot --private --source . --remote mine --push
```
✅ The command prints your repo's URL.

(No `gh`? Create an empty repo on the GitHub website and run `git remote add mine <url>` and `git push -u mine my-taskbot`.)

---

## ✅ Deliverable

- [ ] Context file (`CLAUDE.md`/`AGENTS.md`) with ≤ 40 lines
- [ ] ≥ 5 commits in `git log --oneline`
- [ ] `uv run pytest -q` and `uv run ruff check .` passing
- [ ] Backward-compatibility test (priorities)
- [ ] Repo published on your GitHub

---

## 🧗 Extra challenges

1. **Comparison:** repeat Step 5 **without plan mode** and with a vague request ("add priorities") on a separate branch (`git switch -c vague`). Compare the two diffs: what was left out?
2. **Permissions:** pre-approve `pytest` and `git diff` so you stop being interrupted (🟠 `/permissions` · 🟣 `opencode.json`).
3. **Context:** measure the tokens before and after asking *"read the whole project"*.
4. **Another agent:** open the same repo with the other agent. Does it use the context file?
5. **New command:** `taskbot clear-done` (removes all completed tasks), with the full workflow.

---

## 🆘 Common problems

| Symptom | What to do |
|---|---|
| `command not found: uv/claude/opencode` | Close and reopen the terminal; repeat the installation |
| `git commit` asks for name and email | `git config --global user.name ...` and `user.email ...` |
| `uv run pytest` can't find the package | `uv sync`; check `pyproject.toml` |
| The agent ignores the context file | Open the agent at the project root; trim the file |
| Agent looping on the same error | New conversation with the exact error |
| Huge, confusing diff | `git restore .` and split the request into steps |
| Free model ran out of quota | Another model (🟣 `/models`) or wait |
| The agent made a mess | `git restore .` (and `git clean -fd` for new files) · 🟣 `/undo` |

---

## Final reflection (2 min)

- Which part of the workflow saved you the most time?
- Where did the agent "invent" something you didn't ask for?
- What will you change in your context file?
