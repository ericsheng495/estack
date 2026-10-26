# Project feature knowledge

Estack's existing `recall` skill reconstructs recent context from transcripts and shared records. Its verification skills maintain maps of user journeys. Neither provides a general implemented-feature catalog that is read and updated across engineering tasks. The `project-knowledge` skill adds that layer while linking existing maps and decision records.

## Use in a project

With the skill installed, ask:

> Use project-knowledge to build a knowledge base of the implemented features in this repository. Link the relevant source files and tests, record limitations, and enable the project context pointer.

It creates `.estack/knowledge/index.json`, feature documents, and a short pointer in the project's `AGENTS.md`. The files live in the project they describe, so each project keeps its own history. The skill has automatic discovery enabled. `eric-mode` explicitly consults an existing catalog; other hosts must read the project pointer or invoke the skill. Installing estack does not automatically inspect all your repositories or backfill your past work.

At the start of a task the agent retrieves matching context, inspects the relevant code, and passes only useful paths and constraints to delegates. After changing behavior it updates the affected entry and records what was actually checked. No background service, embeddings, external account, or paid memory API is required.

For deterministic initialization, retrieval, and structural validation:

```bash
python3 <installed-project-knowledge>/scripts/knowledge.py init --project /path/to/project --wire-agents
python3 <installed-project-knowledge>/scripts/knowledge.py context --project /path/to/project --query "csv export"
python3 <installed-project-knowledge>/scripts/knowledge.py check --project /path/to/project
```

Initialization is idempotent and preserves existing instructions and entries. It creates an empty catalog; the agent fills it from inspected sources. Retrieval uses lexical matching across metadata and feature documents, returns at most three features by default, and caps serialized JSON at 6,000 characters. Increase `--limit` or `--max-chars` when needed. The bound controls returned context; this local search still scans feature documents on disk. It does not provide semantic or guaranteed exhaustive retrieval.

Each entry records a source review commit, date, and verification account. The helper compares listed sources with that commit, including local modifications and untracked files, to return `stale`, `unchanged`, or `unknown`. It cannot infer unlisted dependencies, external state, or correctness. `implemented` describes inventory status; it does not claim a test passed. Uncommitted implementations use a null review commit until an actual implementation snapshot can be recorded.

See the [format contract](../skills/project-knowledge/references/format.md) and [skill instructions](../skills/project-knowledge/SKILL.md). Estack's own catalog demonstrates the format and deliberately covers only its documented local variations.

## Research and design choices

[Anthropic's context engineering guidance](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) describes finite context budgets, just-in-time retrieval, and persistent structured notes. We apply those ideas with a small manifest and selectively retrieved feature pages. This implementation choice does not establish a measured cost saving.

[Anthropic's long-running agent harness study](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) uses persistent feature state, progress artifacts, Git history, and actual behavior checks to help fresh sessions continue work. Our catalog records implemented behavior and evidence, while source freshness and honest verification prevent a remembered claim from silently becoming proof.

[AGENTS.md](https://agents.md/) provides a predictable project instruction file used by multiple coding agents. We add a short pointer there rather than placing the whole knowledge base in always-loaded instructions. Hosts that do not consume that file need an equivalent pointer in their own project instructions.
