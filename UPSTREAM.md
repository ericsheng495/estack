# Upstream provenance

- Original project: pstack, by Lauren Tan (poteto).
- Repository: https://github.com/cursor/plugins
- Source directory: `pstack/`
- Source commit: `e73df471cd4bd918367e99f3dd9c51bd53ddf5f0`
- Source URL: https://github.com/cursor/plugins/tree/e73df471cd4bd918367e99f3dd9c51bd53ddf5f0/pstack
- Upstream plugin version: `0.15.32`.
- License: MIT; the original copyright notice is preserved in LICENSE.

## GitHub fork and history

`ericsheng495/estack` is a GitHub fork of `cursor/plugins`. Pstack is a subdirectory of that repository; GitHub does not fork an individual directory. Estack keeps the existing standalone working tree so its installation paths and local additions continue to work.

On October 27, 2026, upstream history through `ab1f702ce8e8b6557edb56b09f52cde8bfb83f17` was joined to estack's original commit history with an explicit `ours` merge. Both histories remain reachable. That merge preserves the estack tree; it does **not** claim to import newer upstream implementation changes. The actual code baseline remains the source snapshot recorded above. Unrelated sibling plugins from the marketplace are absent from the standalone working tree.

The old independent repository is preserved at https://github.com/ericsheng495/estack-standalone-backup. It contains the pre-migration commits and prior GitHub Actions results. The active fork is https://github.com/ericsheng495/estack.

## Variation

Renamed pstack to estack, poteto-mode to eric-mode, poteto-help to eric-help, poteto-agent to eric-agent, and setup-pstack to setup-estack. Updated internal references, public file links, plugin metadata, and installation instructions. Replaced the upstream first-person introduction with attribution to its author.

Estack adds `project-knowledge`, a repository-local feature catalog with bounded retrieval and source freshness checks, and `delegate-work`, a cost-aware policy overriding inherited mandatory fanout and hardcoded model defaults. Routed workflows load the policy before delegating. Recall checks feature knowledge first. These are local additions, documented with research in `docs/project-knowledge.md` and `docs/delegation.md`; the source snapshot above still identifies the upstream baseline.

## Updating

The local `upstream` remote points to `https://github.com/cursor/plugins.git`. In a fresh clone, add that remote once, then fetch it:

```bash
git remote add upstream https://github.com/cursor/plugins.git
git fetch upstream main
git diff e73df471cd4bd918367e99f3dd9c51bd53ddf5f0 upstream/main -- pstack/
```

Review the `pstack/` changes and port them into the standalone root, applying the existing name mapping and preserving local additions. Do not use GitHub's one-click Sync fork or blindly merge the whole marketplace: the working-tree layout intentionally differs from upstream. Update the code baseline above only after actually integrating and verifying its changes. Preserve the fork-history record separately from the implementation baseline. Avoid copying the upstream first-person biography or replacing this repository's installation instructions.
