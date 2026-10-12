# Research Buddy

A production research assistant: an Apple-style Angular app in front of FastAPI and [Google ADK](https://google.github.io/adk-docs/). It loads the [research-scholar agent skills](https://github.com/Yash-Kavaiya/research-scholar-agent-skills) and runs their scripts. You bring your own LLM key. The server never stores it.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yash-kavaiya/research-buddy)

## What it does

Researchers and students work through the research lifecycle in one workspace: finding a problem, literature search and review, study design, analysis, writing, figures, citations, submission, funding, and dissemination.

The assistant does not guess its way through that. For each task it loads a skill (`SKILL.md`) and follows it. When a skill ships a Python script (paper search, citation checks, statistics, power analysis, tables, PDF checks), the API runs that script in a private working folder and returns the output. References that were not retrieved are marked unverified.

## Bring your own key

Supported providers:

| Provider | Typical models |
|---|---|
| Google Gemini | gemini-2.5-flash, gemini-2.5-pro |
| OpenAI | gpt-4.1, gpt-4o |
| Anthropic | Claude 4.5 family |
| Groq | Llama 3.3 and others |
| OpenRouter | any model they serve |
| NVIDIA NIM | Llama and Nemotron hosted models |

The key lives in this browser (localStorage, or sessionStorage if you turn “remember” off). Each request sends it as `X-LLM-Key`. Optional Semantic Scholar, NCBI, and OpenAlex contact details raise scholarly rate limits; the skills work without them. Connect them on the Connectors page.

Links outside the top menu open in a new tab. After five finished chats, a rating prompt asks for a thumbs up or down. Each answer can be copied, shown as Markdown, shared, or branched into a new chat. Chats can be grouped into projects. Deep research tells the agent to load the orchestrator and keep searching. A short disclaimer sits under the composer. Support holds a GitHub star link and a review form; reviews stay on the device.

## Architecture

```
Angular SPA  --GET /api/skills-->  FastAPI (Vercel Python)
             --POST /api/chat-->   ADK LlmAgent + SkillToolset
                                   LiteLLM (caller's key)
                                   skill scripts in a temp folder
```

Conversations stay in the browser. The API is stateless: each chat turn replays history into a fresh ADK session.

## Local development

Python 3.12 and Node 20+.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# terminal 1 — API
cd api && uvicorn app.main:app --reload --port 8000

# terminal 2 — UI (proxies /api to port 8000)
cd frontend && npm ci && npm start
```

Open http://localhost:4200. Add a key in Settings, then use the workspace.

Optional `.env` keys (see [`.env.example`](.env.example)): `ALLOWED_ORIGINS` if the UI is on another host, `RATE_LIMIT_REQUESTS`.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
cd frontend && npm ci && npm run build
```

## Deploy on Vercel

1. Import this repository on [Vercel](https://vercel.com/new).
2. Framework preset: Other. `vercel.json` already sets the Angular build and the Python function.
3. Root directory: repository root. Vercel installs [`requirements.txt`](requirements.txt) for `api/index.py` and builds the frontend into `frontend/dist/frontend/browser`.
4. No server-side LLM keys. Users paste theirs in Settings.

Python 3.12, function max duration 300s. Chat streams as server-sent events. The skill library is bundled with the function via `includeFiles`.

Hobby plans cap duration lower than 300s; Pro or a Fluid-enabled team is the right fit for long agent turns.

## Limits

- Chat body stays under Vercel’s 4.5 MB request cap. Up to 5 attachments, 3 MB each.
- Skill scripts time out at 90s. `publication-figure-maker` and `experiment-logger` scripts are not installed on the server; the assistant gives you the code to run locally.
- Rate limit is per serverless instance (default 30 chat requests / minute / IP).

## Syncing skills

Skills are vendored at `api/skills/` from commit `856545e` of the upstream repository.

```bash
python scripts/sync_skills.py                  # clone latest
python scripts/sync_skills.py --from /path/to/research-scholar-agent-skills
```

## Credits

Skill library: [Yash-Kavaiya/research-scholar-agent-skills](https://github.com/Yash-Kavaiya/research-scholar-agent-skills). Agent runtime: [Google Agent Development Kit](https://google.github.io/adk-docs/).
