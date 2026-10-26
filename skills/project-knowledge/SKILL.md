---
name: project-knowledge
description: Maintain and retrieve a repository's implemented-feature knowledge base, including behavior, source paths, decisions, verification, and limitations. Use when documenting built features, loading project context, or keeping feature knowledge current after code changes.
---

# Project knowledge

Store durable feature context in the **target project's** `.estack/knowledge/`, committed with that project. Keep private project details out of the estack distribution and other projects. This is a source-grounded feature catalog, separate from a backlog or session transcript.

## Load before working

1. Locate the active project root and read its instructions. If `.estack/knowledge/index.json` exists, search it for the task; load only matching feature documents and the source paths needed for the change. Use the helper below or `rg` for exact symbols. A missing search result means discovery is incomplete, not that a feature does not exist.
2. Treat documents as navigation and historical evidence. Inspect relevant live code before relying on a behavioral claim. The helper flags source changes since the recorded review commit; `unchanged` means only that tracked source paths did not change, not that behavior was tested today. Unknown commits, missing Git history, dirty sources, and incomplete source coverage require inspection.
3. Give delegates only the relevant feature IDs, document paths, source paths, and known constraints. Do not copy the whole knowledge base or transcript into each prompt.

```bash
python3 <this-skill>/scripts/knowledge.py context --project <project-root> --query "search export filters"
```

Defaults: at most three matched features and 6,000 output characters. `--limit` and `--max-chars` adjust this bounded retrieval. Ranking is lexical, not semantic; use source search when names differ.

## Bootstrap when requested

When asked to add project memory or a feature knowledge base, initialize it in the selected project:

```bash
python3 <this-skill>/scripts/knowledge.py init --project <project-root> --wire-agents
```

The initializer preserves existing files and appends an idempotent context pointer to `AGENTS.md`. For a host that does not read `AGENTS.md`, add the same short pointer to its existing project instruction file when setting up that host. Plain skill installation alone does not enable automatic context loading outside `eric-mode`.

Inspect routes, commands, exports, existing docs, and tests to seed the important implemented features. Catalog only what the inspected sources establish; leave uninspected areas explicitly uncovered. Reuse existing docs and verification maps through links instead of copying them. The JSON contract and feature writing guide are in [references/format.md](references/format.md).

## Maintain with the change

After implementing, fixing, renaming, or removing a feature, update just its entry and document before handing the work back. Record observable behavior, design constraints that affect future changes, source entry points, and the checks actually run. Use `partial` for incomplete work and `removed` for removed behavior. Keep planned work out of the implemented inventory.

Record the source review commit and date honestly. For uncommitted implementation, leave `reviewed_commit` null until the implementation is committed; never use a preceding commit as evidence for new code. A source review and an executed behavior check are different claims. Verification text records exact commands/results or explicitly says it was not run. Update knowledge in the same change as its implementation where practical; do not add commits merely to chase a self-referential knowledge-file SHA.

```bash
python3 <this-skill>/scripts/knowledge.py check --project <project-root>
```

This checks structure and file references; it cannot establish that behavior works or that every affected dependency was listed. Missing or outdated knowledge should trigger targeted source inspection and a correction, not a full-repository rediscovery on every task.
