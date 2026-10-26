# Upstream provenance

- Original project: pstack, by Lauren Tan (poteto).
- Repository: https://github.com/cursor/plugins
- Source directory: `pstack/`
- Source commit: `e73df471cd4bd918367e99f3dd9c51bd53ddf5f0`
- Source URL: https://github.com/cursor/plugins/tree/e73df471cd4bd918367e99f3dd9c51bd53ddf5f0/pstack
- Upstream plugin version: `0.15.32`.
- License: MIT; the original copyright notice is preserved in LICENSE.

## Variation

Renamed pstack to estack, poteto-mode to eric-mode, poteto-help to eric-help, poteto-agent to eric-agent, and setup-pstack to setup-estack. Updated internal references, public file links, plugin metadata, and installation instructions. Replaced the upstream first-person introduction with attribution to its author.

Estack adds `project-knowledge`, a repository-local feature catalog with bounded retrieval and source freshness checks, and `delegate-work`, a cost-aware policy overriding inherited mandatory fanout and hardcoded model defaults. Routed workflows load the policy before delegating. Recall checks feature knowledge first. These are local additions, documented with research in `docs/project-knowledge.md` and `docs/delegation.md`; the source snapshot above still identifies the upstream baseline.

## Updating

Compare the source directory at the recorded commit with a newer upstream commit. Review and merge changes into this repository, applying the same name mapping and preserving local edits. Update this record after verifying the merged result. Avoid copying the upstream first-person biography or replacing this repository's installation instructions.
