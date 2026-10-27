# Standalone estack distribution

Estack is Eric Sheng's renamed personal fork of Lauren Tan's MIT-licensed pstack. GitHub's parent repository is `cursor/plugins`, where pstack lives in a subdirectory. Estack keeps its standalone root layout. The original 58 top-level skills remain, with `project-knowledge` and `delegate-work` bringing the current top-level collection to 60.

The renamed entrypoints are `eric-mode`, `eric-help`, `setup-estack`, and the delegate persona `eric-agent`. `plugin.json` and `.cursor-plugin/plugin.json` identify `ericsheng495/estack` at version `0.2.0`. The README documents installing plain skills with `npx skills add ericsheng495/estack` and the host-specific limitations. The repository is manually maintained; no automatic upstream sync is configured.

The fork migration joins upstream Git history with the original estack history using an `ours` merge. This preserves both ancestries and the existing working tree without claiming a newer upstream code import. The implementation baseline and the upstream history anchor are recorded separately in `UPSTREAM.md`. The previous independent repository is preserved as `ericsheng495/estack-standalone-backup`. Future updates review only upstream `pstack/` changes and apply the rename/path mapping; one-click fork synchronization is unsuitable for the extracted root layout.

## Verification and limits

The common frontmatter schemas and folder/name agreement were checked for all 60 top-level skills, along with plugin version metadata and links in the new documentation and main entrypoints. New knowledge helper tests run through `.github/workflows/knowledge.yml`.

Cursor-first upstream workflows still contain tools requiring adaptation on other hosts. Plain skill installation does not register native plugin agents or supply external Cursor plugins. The original models by role are retained and require host support. The cost-aware policy limits automatic fanout and context overhead, but does not change role models or implement missing host capabilities. The full upstream helper test suites and a fresh external skills-CLI installation were not run for this change.
