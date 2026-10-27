# Cost-aware delegation

Estack defaults to focused subagents when they reduce repeated context or isolate substantial work. Invoke `/delegate-work` directly, or use `/eric-mode`, which loads the same policy. Standalone workflows that spawn agents, such as `how`, `architect`, and `recall`, also load the policy before delegating. Routine work stays in the main agent. This is an instruction policy, not a scheduler or billing controller; it works through the host's available subagent tools.

## What the research supports

Subagents have their own context and return summaries, but also make their own billable requests. Scoped discovery can protect the coordinator from disposable output. Claude Code also supports cheaper worker models when configured. See [Claude Code subagent documentation](https://code.claude.com/docs/en/sub-agents).

Delegation does not inherently reduce total tokens. Anthropic reported about 15 times the tokens of chat interactions for its multi-agent research system, compared with about four times for its agent interactions. Those are observations from that research product, not a universal multiplier or a comparison with the same coding task. The report also stresses clear task boundaries and proportional effort. See [Anthropic's research system account](https://www.anthropic.com/research/multi-agent-research-system).

Prompt caching reuses matching prefixes; starting or maintaining a session does not guarantee reuse. Stable instructions can help, while rewritten history or compaction can reduce cache hits. The host controls the actual caching behavior. These skills do not set API cache parameters or promise cache savings. See [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching).

Measure complete task cost across coordinator and workers, retries, reasoning, and tool charges. A high cached-token percentage alone does not prove lower total spend. See [OpenAI usage accounting](https://developers.openai.com/api/docs/guides/agents-api/observability).

## Estack's policy choices

These are practical defaults inferred from the research, not benchmarked optimums.

| Work | Default |
| --- | --- |
| Small edit or brief lookup | Main agent |
| Large repository search or log investigation | One focused worker returning evidence and paths |
| Two substantial independent changes | Up to two workers with separate file ownership |
| Architecture with subtle correctness risks | Capable coordinator or configured specialist; targeted review when needed |
| Routine implementation verification | Implementer checks behavior; coordinator checks integration |
| Repeated failed delegation | One corrective follow-up, then revise the split or solve directly |

Workers use the original pstack model for their role unless the user configures an override. Code, exploration, tooling, and verification default to `grok-4.7-xhigh-fast`. Judgment, prose, explanation, synthesis, and the hardest tasks default to `claude-opus-5-5-xhigh`. Arena, architect, and interrogate panels keep their upstream diverse-model composition when used. The complete role mapping remains in [setup-estack](../skills/setup-estack/SKILL.md), and eric-mode retains the upstream effort/speed rules. Parent-model inheritance is an explicit configuration choice, not the default. If a host cannot run a required model, report that limitation and obtain a supported mapping before dispatching the affected delegate.

Cost control applies to worker counts, context size, and retries rather than silently changing role models. Estack does not assume that a faster model is cheaper or invent supported provider slugs. A user's explicit choice of broader review or exploration still applies.

A worker receives a narrow outcome, file pointers, writable ownership, task limits, and a stop condition. It returns a short report with evidence, tests, and unresolved risks. File ownership prevents conflicting concurrent writes. Reuse a relevant worker for a small correction when supported; avoid reloading full history into fresh workers by default.

## Check whether it helps

Compare representative tasks completed directly and with delegation at the same acceptance criteria. Include startup context, root and worker input/output, cached input where reported, retries, tools, total elapsed time, and correctness. Use current host pricing if converting usage to money. Where usage is hidden, report agent count and outcomes and label cost savings as unmeasured. No savings benchmark has been run for these instruction changes.

Read implemented-feature records selectively before dispatching and give each worker only relevant records plus source pointers. Update those records after verified behavior changes. A feature knowledge base avoids repeated discovery; it should not become a transcript dump copied into every worker.

Research reviewed October 26, 2026. Provider features and pricing may change; verify host support before applying model or caching options.
