# Research Buddy

A web app that puts the 59 [research-scholar agent skills](https://github.com/Yash-Kavaiya/research-scholar-agent-skills) behind a chat workspace. Describe a research task; an agent picks the skill that fits, follows its method, runs its scripts for the parts that should be computed or retrieved, and shows its work.

- **Frontend:** Angular 20 (standalone components, signals, zoneless), styled after Apple's design language.
- **Backend:** FastAPI with [Google ADK](https://google.github.io/adk-docs/). The skills load through ADK's `SkillToolset`; models are reached through LiteLLM.
- **Bring your own key:** Google Gemini, OpenAI, Anthropic, Groq, OpenRouter, or NVIDIA NIM. The key stays in your browser and is sent as a header with each request. The server stores nothing.
- **Deployment:** one Vercel project serves the static site and the Python function.

## How it works

```
browser ──/api/chat (SSE)──▶ FastAPI ──▶ ADK LlmAgent ──LiteLLM──▶ your model provider
   │ key, provider, model                  │
   │ in request headers                    ├─ list_skills / load_skill / load_skill_resource   (59 vendored skills)
   │                                       └─ write_file / read_file / run_script              (allowlisted scripts)
   └─ conversations and keys in localStorage
```

The server is stateless. Each request carries the conversation so far, builds a fresh agent with the caller's key, and streams back text, the skills the agent loaded, and each script it ran with its output.

Scripts run with the server's Python, without a shell, from an allowlist, in a scratch folder that exists for one request. Literature scripts call arXiv, Semantic Scholar, OpenAlex, PubMed, and Crossref. Two upstream scripts are not offered: `pubstyle.py` (needs matplotlib) and `log_run.py` (needs a persistent notebook and git).

## Run it locally

Requires Python 3.12+, Node 20+, and [uv](https://docs.astral.sh/uv/) (or plain `pip`).

```bash
# API
uv venv .venv
uv pip install --python .venv -r requirements.txt pytest uvicorn
.venv/bin/python -m uvicorn app.main:app --app-dir api --port 8010 --reload   # Windows: .venv\Scripts\python

# Site (in another terminal); /api is proxied to port 8010
cd frontend
npm install
npm start
```

Open http://localhost:4200, go to **Settings**, choose a provider, paste your key, and pick a model. The model list is read from your provider, and the model must support tool calling.

## Test

```bash
.venv/bin/python -m pytest api/tests          # API, agent wiring, script sandbox; no network or key needed
cd frontend && npx ng test --watch=false --browsers=ChromeHeadless
```

## Deploy to Vercel

The repository deploys as is: import it in Vercel, or run `npx vercel --prod` from the root. `vercel.json` builds `frontend/`, serves `api/index.py` as the function, and sets security headers. No environment variables are required. Optional ones are in `.env.example`.

## API

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | Liveness and skill count |
| `GET /api/skills`, `GET /api/skills/{name}` | The catalog, and one skill's full instructions |
| `GET /api/providers` | Supported model providers |
| `GET /api/models` | Models the supplied key can use, read from the provider |
| `POST /api/keys/validate` | One small call to check the key and model |
| `POST /api/chat` | Run a turn; responds with Server-Sent Events |

Credentials travel in `X-LLM-Provider`, `X-LLM-Model`, and `X-LLM-Key` headers. `X-S2-Key` and `X-NCBI-Key` are optional and raise scholarly API rate limits. Interactive docs are at `/api/docs`.

## Updating the skills

The skills are vendored in `api/skills/` at a pinned upstream commit, recorded in `api/skills/UPSTREAM`.

```bash
python scripts/sync_skills.py --ref main   # then set PINNED_REF in the script to the new commit
```

## Limits worth knowing

- The agent cannot browse the web or open URLs. It reaches the literature only through the skill scripts.
- Attached files (`.bib`, `.csv`, `.tex`, `.txt`, `.md`, `.json`, `.pdf`, up to 3 MB each) are held in browser memory and resent with each turn. They are gone after a reload.
- A turn must finish within the function's time limit (300 seconds). Long multi-skill pipelines may need to be split across messages.
- Rate limiting is per serverless instance and best effort. Put a real limiter in front if the site gets heavy public use.
- The skills help plan, analyse, draft, and check. Decisions, data, and what you submit remain yours.
