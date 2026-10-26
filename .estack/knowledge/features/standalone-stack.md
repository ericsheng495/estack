# Standalone estack distribution

Estack is Eric Sheng's renamed personal variation of Lauren Tan's MIT-licensed pstack, copied from `cursor/plugins` at the snapshot recorded in `UPSTREAM.md`. The original 58 top-level skills remain, with `project-knowledge` and `delegate-work` bringing the current top-level collection to 60.

The renamed entrypoints are `eric-mode`, `eric-help`, `setup-estack`, and the delegate persona `eric-agent`. `plugin.json` and `.cursor-plugin/plugin.json` identify `ericsheng495/estack` at version `0.2.0`. The README documents installing plain skills with `npx skills add ericsheng495/estack` and the host-specific limitations. The repository is manually maintained; no automatic upstream sync is configured.

## Verification and limits

The common frontmatter schemas and folder/name agreement were checked for all 60 top-level skills, along with plugin version metadata and links in the new documentation and main entrypoints. New knowledge helper tests run through `.github/workflows/knowledge.yml`.

Cursor-first upstream workflows still contain tool and model examples requiring adaptation on other hosts. Plain skill installation does not register native plugin agents or supply external Cursor plugins. The cost-aware policy overrides inherited fanout/model instructions, but does not implement missing host capabilities. The full upstream helper test suites and a fresh external skills-CLI installation were not run for this change.
