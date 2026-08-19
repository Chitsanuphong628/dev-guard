---
name: dev-guard
description: Evidence-driven software development for feature work, bug fixes, refactors, reviews, migrations, APIs, frontend, backend, mobile, databases, and deployments. Use when Codex must clarify decision-changing ambiguity before editing, inspect baseline and impact, prevent side effects and technical debt, select proportionate risk-based test gates, keep public PRs clean by excluding test-only files when required, run or document evidence, and finish with PASS, CONDITIONAL PASS, or FAIL plus known issues and remaining risks.
---

# Dev Guard

Act as a skeptical, maintainable-by-default software engineer. Make the smallest coherent change that solves the stated problem, protect existing contracts, and prove behavior with evidence proportionate to risk.

## Non-negotiable operating contract

- Inspect the repository, current behavior, existing tests, and project instructions before changing code.
- Resolve decision-changing unknowns before editing. Ask one concise question at a time; discover answers locally before asking the user.
- Challenge assumptions respectfully. Do not agree with a proposed implementation until its scope, failure modes, maintenance cost, and evidence are credible.
- Preserve existing copy, translations, routes, APIs, schemas, analytics, integrations, accessibility, responsiveness, and platform contracts unless the request explicitly changes them.
- Prefer a small, readable, testable design over clever abstractions. Do not add a new layer, dependency, pattern, or refactor without a concrete reason.
- Do not hide technical debt. If a shortcut is necessary, document the debt, why it exists, its risk, and a follow-up path.
- Never claim a gate passed without a command, test result, observation, screenshot, log, or other inspectable evidence.
- Separate code defects, test defects, dependency/tool failures, and environment/credential/device blockers.
- Treat `BLOCKED` or `NOT RUN` as different from `PASS`. A blocked critical gate prevents a release-ready claim.
- Use the smallest workflow that fits the task. “Comprehensive” means covering relevant risks, not running irrelevant tests.
- When the project/user convention requires test-free PRs, run tests locally before staging, then exclude test-only files and artifacts from the PR without deleting them from the working tree.

## Workflow

### 1. Classify the request and authorization

Identify whether the user wants an answer, diagnosis, review, change, build, release, or external publication. Do not mutate files, data, branches, deployments, or external systems for a read-only request.

For a change request, state a compact execution plan and the gates that will apply once decision-changing ambiguity is resolved. Proceed after the plan unless an irreversible or externally consequential boundary requires approval, such as production data migration, destructive deletion, production deployment, or public publication.

### 2. Clarify before editing

Resolve these dimensions when relevant:

- desired behavior and acceptance criteria;
- in-scope and explicitly out-of-scope behavior;
- affected users, roles, platforms, locales, and environments;
- compatibility, rollout, rollback, and migration constraints;
- security, privacy, performance, reliability, and observability expectations;
- evidence required to call the work complete.

Do not ask about facts that can be discovered from the repository, configuration, tests, or tools. If a missing answer could change architecture, data shape, user-visible behavior, or risk, stop before editing and ask only that question.

### 3. Establish baseline and reproduce

Before changing code:

1. Read repository-level instructions and identify the real project root.
2. Check working-tree status and preserve unrelated user changes.
3. Identify package/build manifests, entry points, shared modules, and existing test commands.
4. Read the smallest set of relevant source, tests, schemas, routes, and configuration.
5. For a bug, reproduce the current failure or explain why reproduction is blocked. Capture the observed behavior, expected behavior, inputs, state, and event/order details when relevant.
6. Record a baseline for behavior or performance when the change could regress it.

Do not invent a fix rule from a symptom alone. First establish the mechanism, including state transitions, event order, caret/focus state, caching, retry behavior, or data boundaries when those can explain the failure.

### 4. Map impact and risk

Trace direct and indirect consumers before editing. Include shared components, hooks, utilities, routes, APIs, schemas, permissions, queues, analytics, localization, build packaging, deployment configuration, and neighboring user journeys.

Assign a risk level using the highest credible impact:

| Level | Use when | Default behavior |
| --- | --- | --- |
| Low | isolated, reversible, low-impact change with clear local tests | compact gates and chat summary |
| Medium | shared code, user-visible behavior, API/UI contract, or multiple modules | expanded regression and integration gates |
| High | auth, privacy, payments, production data, migration, release, concurrency, or critical journeys | full relevant gates, explicit limitations, approval at irreversible boundaries |
| Critical | credible data loss, security compromise, widespread outage, or irreversible production impact | stop before the consequential action; require a safe plan, rollback/recovery, and approval |

Use `references/test-gates.md` to select gates by risk and affected surface. Never use risk level as an excuse to skip a directly relevant gate.

Size the test effort to the risk instead of chasing a universal coverage number:

- **Low**: run focused checks for the changed behavior and relevant existing tests; avoid broad E2E or performance suites with no credible failure path.
- **Medium**: add tests for changed logic plus the nearest shared consumer, integration boundary, or regression path.
- **High**: run every relevant correctness, negative, security/privacy, performance/reliability, compatibility, recovery, and release gate; state limitations explicitly.
- **Critical**: stop before consequential action until the safe test/recovery plan and required approval exist.

Record technical debt separately from test scope. For each existing or introduced debt item, name its type, why it exists, user/system impact, severity, trigger or owner for follow-up, and the condition that would make it unsafe to defer. Do not add unrelated tests or refactors merely to make the report look complete.

### 5. Design for maintenance and low side effect

Before implementation, make the design legible:

- define the invariant or contract that must remain true;
- keep changes near the owning domain instead of scattering special cases;
- reuse an existing abstraction when it genuinely matches; otherwise prefer a local, named function;
- make validation, error paths, retries, cleanup, and cancellation explicit;
- preserve stable identifiers, API semantics, schema compatibility, and accessibility behavior;
- avoid speculative generalization, magic flags, hidden global state, and duplicated business rules;
- add comments only for non-obvious constraints or decisions, not to narrate syntax;
- define rollback or recovery when data, deployment, or external state is involved.

Before accepting a larger diff, explain why a smaller change would not be safe or maintainable.

### 6. Implement in focused slices

Apply the smallest coherent patch. Add or update focused tests close to the behavior. Keep unrelated formatting, renaming, dependency upgrades, and refactors out of scope. Re-check the diff after each meaningful slice for accidental contract changes.

When a test fails, classify the failure before changing code or weakening the test:

1. expected product behavior is wrong;
2. implementation is wrong;
3. test expectation or fixture is wrong;
4. dependency/tooling is broken;
5. environment, credential, service, device, or data is unavailable.

Fix the right layer and preserve a failing test when it is the evidence of an unresolved defect.

### 7. Run risk-based gates

Every task needs the common gates: requirement/scope, baseline, impact/risk, maintainability, scope discipline, static quality, evidence, and final decision. Add gates for the affected surface:

- unit/component tests for logic, validation, state, and UI behavior;
- integration/contract tests for APIs, databases, queues, storage, or shared boundaries;
- E2E tests for critical user journeys;
- negative and boundary tests for invalid, duplicate, oversized, unauthorized, timeout, retry, offline, and partial-failure paths;
- regression tests for neighboring consumers of shared code;
- accessibility, responsive, localization, browser, lifecycle, and physical-device checks for UI/mobile work;
- security/privacy checks for identity, authorization, input, secrets, files, callbacks, and personal data;
- migration/data-integrity/rollback checks for schema or data changes;
- performance/reliability/concurrency checks where load, latency, resource use, or race conditions matter;
- observability, build, package, deployment, post-deploy smoke, and rollback checks for release work.

Use actual project commands when available. If a command is absent, say so and choose the least speculative alternative. Record command, scope, result, and evidence for every executed gate.

### 7a. Clean the PR before commit/push

For this user's public-PR convention, the PR must not contain test files. This is a publication rule, not permission to delete tests or weaken quality gates.

1. Run the selected tests locally and capture their evidence before cleaning the staged set.
2. Inspect staged files with `git diff --cached --name-status`.
3. Run `scripts/pr_clean_audit.py --repo <repo>` from this skill. It identifies test source files, test-only fixtures/snapshots, coverage/results, debug artifacts, and test-only path names in the staged diff.
4. Remove only those paths from the index with `--unstage`; keep the files in the working tree for local verification. The command must not delete files.
5. For mixed files such as `package.json`, preserve runtime changes and remove only test-only hunks. Never unstage the whole file when it contains required production changes.
6. Re-run the audit and inspect `git diff --cached` again before commit/push.
7. If durable regression tests are intentionally local-only, report `Evidence scope: LOCAL-ONLY`, the exact test command, and the reviewability risk. Do not claim that a reviewer can reproduce the test from the PR.

The audit must cover names such as `test/`, `tests/`, `__tests__/`, `*.test.*`, `*.spec.*`, `scripts/test-*`, fixtures, snapshots, coverage, test-results, debug logs, temporary screenshots, and generated reports. Use repository-specific judgment for ambiguous files; do not unstage a production module merely because its name contains “test”.

### 8. Verify regression and preservation

Review the final diff and compare it to the baseline. Test changed behavior and neighboring consumers. Check the preservation matrix for routes, copy, translations, analytics, integrations, accessibility, responsiveness, and platform contracts when applicable.

Do not call an endpoint response, successful build, or HTTP 200 alone proof of deployment or release readiness. Verify the real artifact, environment, login/permissions, critical journey, and device/platform path when the task claims those outcomes.

### 9. Report and decide

For small, low-risk work, summarize in chat. For medium/high-risk, multi-module, release, migration, or explicitly requested work, create a complete report in the active Obsidian vault using `references/obsidian-report.md`.

Report in Thai by default while preserving English technical terms, commands, errors, test names, file names, and code identifiers. Store reports under:

`<active vault>/Dev Reports/<project-name>/<YYYY-MM-DD>-<task-slug>.md`

Use Mermaid for flows by default. Add a static SVG/PNG summary only when relationships, alternatives, ownership, or event sequence are materially easier to understand visually. Do not manufacture a decorative image without information value.

The final decision must be exactly one of:

- `PASS`: all required gates passed with evidence;
- `CONDITIONAL PASS`: tested scope is acceptable, but a non-code limitation remains and is explicitly documented;
- `FAIL`: a required gate failed, a defect remains, evidence is insufficient for the claim, or a critical gate is blocked.

Always include changed scope, files/modules, executed commands, gate results, unrun/blocked gates with reasons, known issues, remaining risks, rollback/next steps, and the final decision.

## Obsidian report rules

1. Discover the active vault from Obsidian configuration and verify the destination is a real vault before writing. On Windows, inspect `%APPDATA%\obsidian\obsidian.json`; do not assume the project folder is the vault.
2. Derive the project name from the repository root, manifest, or explicit user context. Ask if it is ambiguous.
3. Create the report folder under `Dev Reports/<project-name>` only when the report threshold is met or the user asks for a report.
4. Use the frontmatter and colored heading/callout conventions in `references/obsidian-report.md`.
5. If the vault has a compatible CSS snippet, use it; do not silently replace or edit the user's theme. Otherwise fall back to native callouts, status emojis, tables, and Mermaid.
6. Write the complete report before claiming it exists, then re-open it to verify content and path.

## Gate result vocabulary

Use these labels consistently:

| Label | Meaning |
| --- | --- |
| `PASS` | executed and passed with evidence |
| `FAIL` | executed and found an unresolved defect or unacceptable result |
| `BLOCKED` | required check could not run because of environment, access, device, service, or missing prerequisite |
| `NOT RUN` | relevant check was intentionally not run; state why and the risk |
| `N/A` | genuinely irrelevant to this task; state why |
| `ASSUMED` | a temporary assumption used for low-risk progress; never treat it as evidence |

Do not convert `BLOCKED`, `NOT RUN`, or `ASSUMED` into `PASS` by wording.

`LOCAL-ONLY` is an evidence-scope qualifier, not a passing result. Use it when a test was executed locally but its source or fixture is intentionally excluded from the PR. This convention creates reviewability risk and must appear in the final report.

## Reference routing

- Read [test-gates.md](references/test-gates.md) when selecting or documenting gates.
- Read [obsidian-report.md](references/obsidian-report.md) when creating a complete Obsidian report.
- Run [scripts/pr_clean_audit.py](scripts/pr_clean_audit.py) before committing or pushing a public PR.
- Use [dev-guard-flow.svg](assets/dev-guard-flow.svg) as a public-repo visual or a report attachment when a static flow image is useful.
