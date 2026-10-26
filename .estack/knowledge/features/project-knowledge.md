# Implemented-feature knowledge

Agents can keep durable project context in `.estack/knowledge/index.json` and linked feature documents. Invoke `project-knowledge` to bootstrap a selected project; `eric-mode` reads an existing catalog before feature work, and `recall` checks it before mining historical context. After behavior changes the instructions require updating the affected feature record.

The CLI in `skills/project-knowledge/scripts/knowledge.py` supports `init`, `check`, and `context`. Initialization preserves existing entries and can append an idempotent pointer to `AGENTS.md`. Retrieval uses lexical search, defaults to three features, and bounds serialized output to 6,000 characters. `check` validates the versioned manifest and project-relative source/document paths. Git comparison flags changed listed sources, unavailable snapshots, and local changes; it does not establish behavioral correctness.

The manifest format lives in `skills/project-knowledge/references/format.md`. Each feature has a status, summary, document, source paths, source review commit/date, and verification account. Features may be implemented while their runtime behavior remains unverified. Keep verification maps and decision records in their existing locations and link them.

## Verification and limits

`python3 -m unittest discover -s skills/project-knowledge/scripts -p 'test_*.py' -v` passed 13 checks covering initialization preservation/idempotency, retrieval, output/count bounds, invalid references, traversal/symlinks, removed features, and freshness with committed, dirty, untracked, or unavailable sources. An independent temporary-project smoke exercise also confirmed the bootstrap and retrieval flow. Skill schemas and referenced documentation were validated.

This catalog intentionally covers estack's local variations rather than all upstream skills. Existing user projects need a separate bootstrap from their actual sources. The helper scans document text on disk; it does not use embeddings. Retrieval can miss synonyms. Staleness covers only listed source paths, not implicit dependencies, external state, or unrecorded work. Hosts must load project instructions or invoke the skill for context to be consumed.
