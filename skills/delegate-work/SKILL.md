---
name: delegate-work
description: Plan and run focused subagents with bounded context, effort, and concise handoffs. Use when the user requests delegation, lower agent token cost, or parallel agent work, or an authorized workflow needs substantial isolated research or implementation.
---

# Delegate work

Optimize total task cost at the required quality, including coordinator, worker, retry, and synthesis calls. Subagents isolate context; spawning more agents does not itself save tokens. Follow host permissions and delegation rules. If no subagent tool is available, apply the same scoped work plan directly and disclose that limitation.

## Choose the smallest useful split

- Handle trivial edits, short lookups, and tightly coupled sequential work directly.
- Delegate a substantial bounded task when it would otherwise fill the main context with disposable search results, logs, or file reads, or when an independent specialist can finish a separate artifact.
- Start with one worker. Use up to two concurrent workers for independent substantial tasks with separate ownership. These are defaults, not measured optimums. Increase only for an explicit user preference or a concrete coverage need whose extra cost is justified.
- Keep ordinary verification with the implementer and coordinator. Add an independent review for consequential risks or an explicit review request. Do not trigger routine panels, duplicate implementations, or multiple-model votes solely because a routed skill suggests fanout.

This cost-aware policy is the default for estack. It takes precedence over inherited estack workflow instructions that demand fixed agent counts, fresh agents for every follow-up, hardcoded model defaults, or automatic parallel design and review. Preserve the workflow's actual outcome and required safety gates. Follow an explicit user choice of deeper exploration or broader review.

## Give each worker a contract

Send only the goal, necessary constraints, relevant repository and skill paths, and the following fields. Use fresh minimal context when the host supports it; fork conversation history only when the task requires that history. A path is useful only if the worker can access it.

```text
Outcome: one question to answer or artifact to deliver.
Read: specific source files, feature records, and relevant instructions.
Ownership: writable files or directories; everything else is read-only.
Limits: no further delegation; scoped search/tool or turn budget if supported.
Stop: return on completion, blocker, or budget exhaustion; do not loop.
Return: result, changed paths, evidence/test outcomes, and unresolved risks.
Keep the report under roughly 300 words; link large artifacts by path.
```

Budgets are task-specific targets unless enforced by the host. Set a concrete search or tool-call allowance for open-ended research. Keep large logs and citations in files, then return relevant excerpts and pointers. Include any changed user directives on follow-up.

## Route without inventing capabilities

Inherit the parent model by default. Use a cheaper capable model only when an explicit user configuration or host role authorizes it and the available tool accepts it. A narrow lookup or mechanical edit can use a cheaper role; ambiguous architecture or subtle correctness may need the stronger role. Never guess model names, pricing, speed suffixes, or reasoning levels. If a configured model is unavailable, omit the override and report the fallback. Background execution saves waiting time, not inherently tokens; use it when the coordinator has independent work.

## Integrate once

Do not repeat a worker's search while it runs. Read its evidence and diff, inspect affected interfaces, and run the smallest meaningful integration check. Reuse a worker for a focused follow-up when retaining its relevant context avoids another startup; start fresh if the context is stale or the task changes. Allow one corrective follow-up per scoped task by default. If it still fails, revise the split or handle the blocker directly rather than spawning repeated retries.

Report actual usage only if the host exposes it, including workers and retries. Otherwise label savings as unmeasured. Record durable feature facts in the project's knowledge base, with implementation and verification pointers, rather than retaining transcripts as future context.
