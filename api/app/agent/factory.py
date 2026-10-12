"""Builds the research agent for one request from the caller's own provider, model, and key."""

from __future__ import annotations

import datetime
import functools
import warnings
from pathlib import Path
from typing import AsyncGenerator, Callable

from google.adk.agents import LlmAgent
from google.adk.models.base_llm import BaseLlm
from google.adk.models.lite_llm import LiteLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.skills import load_skills_from_dir
from google.adk.tools.skill_toolset import SkillToolset

from .. import config
from ..catalog import load_catalog
from ..errors import ProviderError, describe
from .tools import make_script_tools

warnings.filterwarnings("ignore", category=UserWarning, module=r"google\.adk")

AGENT_NAME = "research_buddy"

INSTRUCTION = """\
You are Research Buddy, an assistant for researchers and students. You work through a \
library of research skills that covers the research lifecycle: finding a problem, \
literature search and review, study design, analysis, writing, figures and tables, \
citations and integrity, submission and peer review, funding, and dissemination.

How to work:
1. For any research task, find the skill that fits. Call `list_skills` when you are unsure \
which one applies, then `load_skill` to read its instructions before you do the work, and \
follow those instructions, including the skill's output format.
2. When a request spans stages or names a goal instead of a task, load \
`research-scholar-orchestrator` and follow its routing table, loading each skill in turn.
3. Some skills ship Python scripts for work that must be computed or retrieved, not \
recalled: literature search, citation checks, statistics, power analysis, tables. Run them \
with `run_script(skill_name, script, args)`. This replaces any instruction to use bash, a \
shell, `run_skill_script`, or another script tool: `run_script` is the only way to run a \
script here, and it does work. Scripts read and write files in a private working folder; \
put pasted text there with `write_file`, and read output files with `read_file`.
4. Use `load_skill_resource` to open a skill's `references/` and `assets/` files when its \
instructions call for them.
5. Answer simple conversational questions directly, without loading a skill.

Rules that always hold:
- Never invent references, quotations, data, results, statistics, or facts about venues, \
funders, or people. Retrieve them with a script, or say they are unknown.
- Only cite papers that a script returned in this conversation or that the user supplied. A \
reference that was not retrieved is unverified; say so.
- State limitations, failed checks, sources that could not be searched, and anything you \
could not verify.
- Research decisions and responsibility for what is submitted stay with the user. Stop at \
decisions that are theirs: topic, research question, design, venue.
- You cannot browse the web or read URLs. The scripts of `publication-figure-maker` and \
`experiment-logger` are not available here; for those skills, give the user the code or \
commands to run themselves.

Write in Markdown. Use tables where the skill's output format calls for them, fenced code \
blocks for code, LaTeX, and BibTeX, and `$...$` or `$$...$$` for mathematics.

Today's date is {today}.
"""


@functools.lru_cache(maxsize=1)
def _adk_skills():
    return load_skills_from_dir(config.SKILLS_DIR)


def build_model(provider_id: str, model: str, api_key: str) -> BaseLlm:
    """A LiteLLM-backed model that carries the caller's key. Nothing is cached or put in the environment."""
    provider = config.PROVIDERS[provider_id]
    return LiteLlm(model=provider.litellm_model(model), api_key=api_key, drop_params=True)


class GuardedLlm(BaseLlm):
    """Wraps a model so a failed call raises a ProviderError with the caller's secrets removed.

    ADK logs model exceptions before the app sees them, and a provider may echo the key
    it was sent, so the original exception must not travel past this point.
    """

    inner: BaseLlm
    secrets: tuple[str, ...] = ()

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        try:
            async for response in self.inner.generate_content_async(llm_request, stream=stream):
                yield response
        except Exception as exc:
            raise ProviderError(*describe(exc, *self.secrets)) from None


def build_agent(
    model: BaseLlm,
    workdir: Path,
    *,
    secrets: tuple[str, ...] = (),
    pinned_skill: str | None = None,
    attachments: list[str] | None = None,
    script_env: dict[str, str] | None = None,
    today: datetime.date | None = None,
) -> LlmAgent:
    catalog = load_catalog()
    instruction = INSTRUCTION.format(today=(today or datetime.date.today()).isoformat())
    if pinned_skill and pinned_skill in catalog:
        instruction += (
            f"\nThe user chose the `{pinned_skill}` skill for this conversation. Load it with "
            "`load_skill` before your first answer and work through it unless they ask for something else.\n"
        )
    if attachments:
        instruction += (
            "\nFiles the user attached, already in the working folder and ready to pass to "
            "`run_script` or open with `read_file`: " + ", ".join(attachments) + "\n"
        )

    tools: list[Callable | SkillToolset] = [
        SkillToolset(
            skills=_adk_skills(),
            tool_filter=["list_skills", "load_skill", "load_skill_resource"],
        ),
        *make_script_tools(workdir, script_env),
    ]
    guarded = GuardedLlm(model=model.model, inner=model, secrets=tuple(s for s in secrets if s))
    return LlmAgent(
        name=AGENT_NAME,
        model=guarded,
        instruction=instruction,
        tools=tools,
        description="Routes research requests to the research-scholar skills and carries them out.",
    )
