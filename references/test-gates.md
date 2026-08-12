# Dev Guard test-gate catalogue

Use this catalogue to choose gates by risk and affected surface. Do not run irrelevant gates just to make a checklist look complete. Do not omit a directly relevant gate because the task is small.

## Common gates for every change

| Gate | Question | Evidence |
| --- | --- | --- |
| Requirement / scope | What must change, what must not change, and how will success be recognized? | acceptance criteria, scope note |
| Ambiguity | Could an unanswered question change architecture, data, behavior, or risk? | questions resolved or explicit low-risk assumptions |
| Baseline | What happens before the change? Can the bug or current behavior be reproduced? | command, test, observation, screenshot, or log |
| Impact | Which direct and indirect consumers can be affected? | impact map and preservation matrix |
| Risk | What is the highest credible failure impact and why? | risk level, threats, rollback/recovery note |
| Design / maintainability | Is the solution readable, local to its domain, and free of avoidable debt? | design note and diff review |
| Scope discipline | Did the patch avoid unrelated refactors, formatting, and behavior changes? | `git diff`, changed-file list |
| Static quality | Does the project still format, lint, typecheck, compile, and validate schemas? | actual commands and output |
| Evidence integrity | Can every important claim be traced to an executed check? | evidence log |
| Final decision | Is the outcome PASS, CONDITIONAL PASS, or FAIL? | final report with remaining risks |

## Correctness and regression gates

| Gate | Select when | Minimum focus |
| --- | --- | --- |
| Unit | business logic, calculation, parser, validator, utility, state transition | happy path, boundaries, failure behavior |
| Component | component, hook, form, local state, interaction | render states, events, focus, errors, loading |
| Integration | modules cross a boundary or use real persistence/network | serialization, error propagation, transaction boundary |
| Contract/API | request/response, status, schema, event, or public method changes | valid/invalid contract, compatibility, auth |
| E2E/critical journey | login, checkout, submit, upload, send, publish, or other business-critical flow | real user path plus failure exit |
| Regression | shared code, routing, auth, state, API, or behavior used by neighbors | changed path and nearest consumers |
| Backward compatibility | existing clients, persisted data, plugins, or external consumers remain | old version against new boundary |

## Negative, boundary, and resilience gates

Select cases that match the system boundary. Prefer a focused test over a generic list.

- empty, malformed, whitespace-only, special-character, oversized, and unsupported input;
- duplicate submit, duplicate event, replay, idempotency, and out-of-order delivery;
- unauthorized, forbidden, wrong tenant, wrong owner, expired session, and stale token;
- timeout, cancellation, network loss, DNS failure, server error, rate limit, retry, and backoff;
- partial success, transaction rollback, queue redelivery, and cleanup after failure;
- concurrent update, race condition, stale cache, reload, refresh, back navigation, and lifecycle restart;
- offline/online transition, low memory, low disk, closed app, killed process, and interrupted upload when applicable.

## Security and privacy gates

Select when the task touches identity, permissions, user-controlled input, files, URLs, secrets, logs, or personal data.

- authentication, session expiry, logout, refresh, and account switching;
- authorization at role, tenant, object, and field level;
- validation and encoding against the relevant injection or script risks;
- secret/token handling, redaction, storage, rotation, and accidental logging;
- file upload type/size/path checks, redirects, webhooks, callbacks, and CORS/CSRF behavior;
- personal-data minimization, retention, export/delete behavior, and audit trail;
- dependency vulnerability and license review when dependencies change.

Do not claim a security review from a passing unit test alone. State the security boundary and what was actually checked.

## Database and data gates

Select for schema, query, migration, backfill, data import/export, or persistence changes.

- schema compatibility with old and new application versions;
- null/default/constraint/index behavior and referential integrity;
- query correctness, pagination, filtering, ordering, and N+1 risk;
- transaction boundary, atomicity, idempotency, and partial-failure behavior;
- duplicate, missing, corrupted, orphaned, and legacy data;
- migration repeatability, ordering, rollback/recovery, and deploy sequencing;
- backup/restore or a verified recovery path for production-impacting data;
- representative volume/performance and lock/contention behavior.

## Frontend, accessibility, and localization gates

Select for UI, interaction, layout, content, or client-side state changes.

- loading, empty, error, success, retry, disabled, and permission states;
- desktop, tablet, mobile, viewport overflow, resize, zoom, and orientation;
- keyboard order, focus visibility, semantic roles, labels, contrast, and screen-reader behavior;
- touch targets, gestures, reduced motion, animation cancellation, and pointer/keyboard parity;
- browser compatibility for supported browsers;
- Thai/English text expansion, wrapping, truncation, dates, numbers, time zones, and RTL if relevant;
- analytics, deep links, routing, history, refresh, and back behavior.

## Mobile and device gates

Select for native wrappers, Android/iOS behavior, permissions, lifecycle, or release artifacts.

- clean install, upgrade install, uninstall/reinstall, package/bundle identity, and signing;
- login, deep link, foreground/background, rotation, process death, and network change;
- permission granted/denied/revoked and OS-version differences;
- native bridge contracts, WebView navigation, URL history versus domain/data undo;
- physical-device smoke test for any release-ready claim; emulator-only evidence is conditional;
- artifact inspection and installation of the exact APK/IPA/bundle intended for delivery.

## Performance, reliability, and concurrency gates

Select when the change touches hot paths, large data, long-running work, parallel requests, or production scale.

- latency, throughput, startup/render time, bundle/asset size, and query plan;
- memory/resource cleanup, connection/file handle lifecycle, and leak checks;
- concurrency, race, ordering, locking, optimistic/pessimistic conflict behavior;
- retry/backoff, circuit breaking, cancellation, timeout, queue visibility, and duplicate delivery;
- rate limits, backpressure, pagination, batching, and large input;
- comparison to a baseline when a measurable regression is plausible.

## Observability and operations gates

Select for production behavior, background jobs, distributed flows, or operational changes.

- structured logs with correlation/request identifiers;
- metrics for success, failure, latency, volume, retries, queue depth, and saturation;
- traces across service boundaries where diagnosis requires them;
- actionable error tracking and alerts with clear thresholds and owners;
- health/readiness checks and safe degraded behavior;
- audit events for security/data-sensitive actions;
- runbook, dashboard, rollout guard, feature flag, and rollback/recovery path.

## Build, release, and deployment gates

Select for release, deployment, packaging, configuration, or environment changes.

- clean install from lockfile and reproducible build;
- exact artifact identity, version, package name, signing, and checksums where relevant;
- environment variables, secrets, feature flags, migrations, and deployment ordering;
- post-deploy smoke in the real target environment;
- critical journey, auth/permissions, integrations, logs, metrics, and alerts after deploy;
- rollback or forward-fix plan tested or explicitly blocked;
- distinguish a successful endpoint/HTTP response from a successful deployment workflow.

## Test quality gate

Review tests themselves:

- assert user-visible behavior or domain contracts rather than incidental implementation;
- cover both success and failure paths where failure can harm users or data;
- remain deterministic and independent of test order;
- use realistic fixtures without hiding the boundary behind excessive mocks;
- fail with a diagnostic message;
- protect the reproduced bug or acceptance criterion;
- never delete, disable, weaken, or over-mock a test just to make CI green.

## Result rules

For each selected gate record:

1. gate name and scope;
2. method or command;
3. result: `PASS`, `FAIL`, `BLOCKED`, `NOT RUN`, or `N/A`;
4. evidence path, output, screenshot, log, or observation;
5. failure classification and root cause;
6. consequence and remaining risk;
7. follow-up owner/action when not passed.

`BLOCKED` means the check was required but could not execute. `NOT RUN` means it was relevant but intentionally omitted. Neither is a pass.
