# Feature knowledge format

The project owns `.estack/knowledge/index.json`. Paths in entries are relative to the project root. Use concrete files or directories, with no globs, absolute paths, or traversal outside the project.

```json
{
  "version": 1,
  "features": [
    {
      "id": "csv-export",
      "summary": "Export filtered search results as CSV",
      "status": "implemented",
      "document": ".estack/knowledge/features/csv-export.md",
      "source_paths": ["src/export.ts", "tests/export.test.ts"],
      "reviewed_commit": null,
      "reviewed_at": "2026-10-26",
      "verification": "Not run; source review only"
    }
  ]
}
```

`status` is `implemented`, `partial`, or `removed`. `reviewed_commit` is a full 40- or 64-character Git object ID for the inspected source snapshot, or null for uncommitted work or unavailable history. `reviewed_at` is an ISO date of actual inspection. `verification` is a nonempty account of checks and their results, including limitations. An implemented feature can have unverified behavior; the two fields answer different questions.

A feature document should explain what a user or caller can do, how to reach it, the source files that implement it, dependencies or constraints that matter for changes, meaningful design decisions and their evidence, how it was verified, and current limitations. Use only the sections needed. Link an existing verification map or decision record rather than duplicating it. Do not store raw chat logs, credentials, speculative decisions, or every internal helper.

Keep the manifest summaries short enough to scan. Split a document when unrelated tasks would otherwise read large amounts of irrelevant context. Keep removed entries if they prevent future agents from mistakenly restoring obsolete behavior, and explain the replacement in their document.
