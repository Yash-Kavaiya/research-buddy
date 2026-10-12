---
name: experiment-logger
description: "Keeps an append-only lab notebook of experiment runs, configs, metrics, git commits, and decisions, and renders a Markdown notebook. Use when recording or comparing runs. Not for planning experiments."
version: 1.0.0
compatibility: "Requires Python 3.10 or later. Runs locally with no network access."
allowed-tools: "Bash(python:*) Read Write"
permissions: [shell, file_write]
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [experiment-tracking, lab-notebook, reproducibility]
---

# Experiment Logger

Record what was run, with which settings, what came out, and why the next step was chosen. The log is the evidence behind every number in the paper.

## Purpose

Record what was run, with which settings, what came out, and why the next step was chosen, so that every number in a paper can be traced to a run. The log is a plain JSON-lines file kept with the code.

## When to use

- At the start of experimental work, to set up the log.
- After every run, sweep, or analysis that produces a result.
- When a decision is made: an idea dropped, a setting fixed, a bug found.
- When writing up and looking for the run behind a number.

Hand off instead for planning what to run (`experiment-planner`) or reading what the results mean (`results-interpreter`).

## Prerequisites

- Python 3.10 or later; the script uses only the standard library.
- Optional: git, so each entry records the commit and whether the working tree was clean.
- Write access to the project folder (default log: *log.jsonl* in the *experiments* folder).

## Inputs

- Run name and purpose.
- Configuration: hyperparameters, dataset, seed. A JSON config file is best.
- Metrics, with the split they were measured on.
- Paths to artifacts: checkpoints, plots, output files.
- For decisions: what was decided and the evidence.

## Instructions

1. **Set up once.** The log lives in the project at *log.jsonl* in the *experiments* folder. Commit it to version control. If the team already uses a tracker (Weights & Biases, MLflow, TensorBoard), keep using it for curves and use this log for the run index and the decisions, with the tracker's run URL as an artifact.
2. **Record each run** as soon as it finishes, including failed ones:

   ```bash
   python scripts/log_run.py add --name baseline-resnet50 \
     --config lr=0.1 --config epochs=90 --config seed=0 \
     --metric val_top1=76.1 --metric test_top1=75.8 \
     --tags baseline --note "Reference run with the paper's schedule" \
     --artifact baseline-ckpt.pt
   python scripts/log_run.py add --name sweep-03 --config-file sweep03.json \
     --metric val_top1=77.4 --status completed
   python scripts/log_run.py add --name sweep-04 --config-file sweep04.json \
     --status failed --note "NaN loss at step 1200 with lr=1.0"
   ```

   The script assigns an id, adds a timestamp, and records the git commit, branch, and whether the working tree had uncommitted changes. Use `--log PATH` before the subcommand for a different log file. Nested config files are flattened to dotted keys.
3. **Record decisions** when they are made:

   ```bash
   python scripts/log_run.py decision "Dropping label smoothing: no gain over 3 seeds (runs 4-6, mean diff 0.1, sd 0.3)"
   ```

   A good decision entry names the evidence (run ids) and the alternative that was rejected.
4. **Query the log:**

   ```bash
   python scripts/log_run.py best --metric val_top1 --mode max
   python scripts/log_run.py compare 3 7        # config and metric differences between two runs
   ```

5. **Render the notebook** for reading and for supervisor meetings:

   ```bash
   python scripts/log_run.py render             # writes NOTEBOOK.md next to the log
   ```

6. **Correct by appending.** Entries are never edited or deleted. If a run was logged with a wrong metric, add a decision entry saying so and log the corrected run again.
7. **Before writing the paper**, map every number in every table to a run id, and store that mapping with the paper.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/log_run.py add` | Appends a run entry with config, metrics, tags, note, artifacts, and git state | `--name` (required), `--config KEY=VALUE`, `--config-file JSON`, `--metric KEY=VALUE`, `--status`, `--tags`, `--note`, `--artifact PATH` |
| `scripts/log_run.py decision` | Appends a dated decision with its reason | `TEXT` (required) |
| `scripts/log_run.py best` | Shows the best run for a metric | `--metric NAME` (required), `--mode max|min` |
| `scripts/log_run.py compare` | Shows config and metric differences between two runs | `ID_A ID_B` |
| `scripts/log_run.py render` | Writes the Markdown notebook | `--out FILE`; global `--log PATH` goes before the subcommand |

Run a script with the agent's script tool, for example `run_script("scripts/log_run.py add", args=[...])`, or from a shell in the skill folder with `python scripts/log_run.py add ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

Each line of *log.jsonl* in the *experiments* folder is one entry:

```json
{"id": 7, "time": "2026-03-04T15:12:09+05:30", "type": "run", "name": "sweep-03", "status": "completed",
 "config": {"lr": 0.01, "epochs": 90, "seed": 0}, "metrics": {"val_top1": 77.4},
 "tags": ["sweep"], "note": "", "artifacts": [], "git": {"commit": "a1b2c3d", "dirty": false, "branch": "main"}}
{"id": 8, "time": "...", "type": "decision", "text": "Fix lr=0.01 for all later runs (runs 5-7)"}
```

*NOTEBOOK.md* contains a runs table (id, date, name, status, one column per metric, commit, tags) followed by a chronological log of runs and decisions.

## Examples

Requests that should trigger this skill:

- "Log this run: lr 0.01, 90 epochs, top-1 77.4."
- "Set up a lab notebook for my experiments."
- "Which config gave the best validation accuracy?"
- "What changed between run 3 and run 7?"
- "Record that we dropped label smoothing and why."

Requests that belong to another skill:

- "Plan which experiments to run." → use `experiment-planner`
- "Interpret these results." → use `results-interpreter`
- "Track my thesis milestones." → use `research-progress-tracker`

### Worked example

**Request:** "Log my finished run: name sweep-03, lr=0.01, epochs=90, seed=0, val_top1=77.4. Then tell me how it differs from run 1."

**What the agent does:**

1. Runs `run_script("scripts/log_run.py", args="add --name sweep-03 --config lr=0.01 --config epochs=90 --config seed=0 --metric val_top1=77.4")`.
2. Notes from the output that the working tree was dirty and advises committing before reportable runs.
3. Runs `compare 1 3` and reads the differences.
4. Renders the notebook.

**Result (excerpt):**

```markdown
{"id": 3, "type": "run", "name": "sweep-03", "config": {"lr": 0.01, "epochs": 90, "seed": 0}, "metrics": {"val_top1": 77.4}, "git": {"commit": "a1b2c3d", "dirty": true, "branch": "main"}}

compare 1 3:
{"config": {"lr": [0.1, 0.01]}, "metrics": {"val_top1": [76.1, 77.4]}}
```

## Quality bar and pitfalls

- Log only what happened. Metrics are copied from the run's output, never typed from memory or rounded up.
- Log failed and negative runs. The record of what did not work prevents repeating it and belongs in the paper's honest account.
- A run logged with a dirty working tree (`*` after the commit) cannot be reproduced exactly from the commit. Commit before running anything that may be reported.
- Always record the seed and the dataset version or split.
- Name the split in the metric (`val_`, `test_`). Selecting on test metrics is a methodological error the log should make visible.
- Do not put secrets, API keys, or personal data in configs or notes; the log is committed.
- One entry per run. Averages over seeds are computed from the entries, not logged in place of them.

## Limitations

- The log records what is entered. It does not capture metrics automatically from training code or verify that they are correct.
- It is an index of runs and decisions, not a replacement for curve-level trackers such as Weights & Biases or MLflow.
- A run logged with uncommitted changes cannot be reproduced exactly from its commit.
- Concurrent writes from several processes at once are not coordinated.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `error: expected key=value, got 'lr'` | A `--config` or `--metric` argument has no equals sign | Write each as `KEY=VALUE`, for example `--config lr=0.01` |
| `error: no run has a numeric metric named 'x'` | The metric name is misspelled or was logged as text | Check metric names in the rendered notebook and log metrics as numbers |
| The `git` field is empty | The project is not a git repository, or git is not installed | Initialise git; the entry is still valid without it |
| A logged value is wrong | A typing mistake | Do not edit the file; add a decision entry noting the error and log the corrected run again |

## Related skills

- `experiment-planner` defines the runs this log records.
- `ablation-study-designer` runs are logged with a shared tag.
- `paper-to-code-reproducer` logs reproduction runs and assumptions here.
- `results-interpreter` reads the log to produce findings.
- `reproducibility-checklist` draws on the recorded configs, seeds, and commits.
- `research-progress-tracker` summarises the log for supervisor meetings.
- `latex-table-generator` typesets results exported from the log.
