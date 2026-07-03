---
applyTo: "config/flows/*/*.yaml"
---

# Copilot review rules — FIS12 flow configs

Review each changed flow config against these rules. (Kept in sync with
`.claude/skills/review-flow-config/checklist.md` — the fuller version.)
Severity: 🔴 blocker · 🟠 should-fix · 🟡 nit.

## Structure & metadata
- 🔴 `meta.domain` == `ONDC:FIS12`, `meta.version` == `2.3.0`.
- 🟠 `meta.flowId` matches the filename; `meta.description` and `config_version` present.
- 🟡 `transaction_data.transaction_id` is a UUID. Do NOT require `context.transaction_id`/`message_id`/`timestamp` in `defaultPayload` to match — the runner overwrites them at runtime.
- 🔴 Each step has `api`, `action_id`, `owner`, `responseFor`, `unsolicited`, `description`, `mock`.
- 🟠 `action_id` base ids (before `#`) unique in the file unless intentional for repeated pushes.

## Action sequence (cross-check `config/actions/index.yaml`)
- 🔴 The ordered `api` values form a valid path through `supportedActions`: first api is under the `"null"` key (`search`/`init`); each next api is in the previous api's successor list. Exclude form apis (`dynamic_form`/`html_form`) from this path check — they are local UI steps, not protocol-graph nodes.
- 🔴 `owner`: `search select init confirm update status cancel track` → **BAP**; every `on_*` → **BPP**. Form apis (`dynamic_form`/`html_form`) are local UI steps — owner varies (commonly BPP), don't flag.
- 🔴 A solicited `on_X` step sets `responseFor` to the matching `X` step's `action_id`; request steps set `responseFor: null`.
- 🟠 `unsolicited: true` only for pushed callbacks, which must also have `responseFor: null`.

## api casing
- 🟠 Step `api` must be lowercase (`dynamic_form`, `html_form`, `on_search`) — never `DYNAMIC_FORM`/`HTML_FORM`.

## context ↔ meta consistency (inside `mock.defaultPayload`)
`context` is a template; the runner overwrites `transaction_id`/`message_id`/`timestamp`. Check static fields only:
- 🟠 `context.action` == step `api`; `context.domain` == `meta.domain`; `context.version` == `meta.version`.
- 🟡 `bap_id`/`bap_uri`/`bpp_id`/`bpp_uri` consistent across steps; `ttl` present; `location.country.code` == `IND`.
- Do NOT flag `transaction_id`/`message_id`/`timestamp` drift.

## Base64 mock functions — DECODE `generate` / `validate` / `requirements`
- 🔴 Decodes cleanly and is a COMPLETE function declaration (parsed as-is): `function generate(defaultPayload, sessionData)`, `function validate(targetPayload, sessionData)`, `function meetsRequirements(sessionData)`.
- 🔴 No sandbox-forbidden tokens: `eval`, `Function`, `Worker`, `require`, `process`, `Buffer`, `globalThis`, `__dirname`, `__filename`, `module`/`exports`, `__proto__`, `while(true)`, `for(;;)`, `with`.
- 🔴 `fetch`/`XMLHttpRequest` only allowed in `generate` (allow-listed); never in `validate`/`meetsRequirements` (must be pure).
- 🔴 `validate`/`meetsRequirements` return `{ valid, code, description }`; `generate` returns the awaited payload. A `generate` using `await` must be `async`; `generateConsentHandler` must be awaited (else `DataCloneError`).
- 🟠 Every `sessionData.<key>` read by `generate`/`meetsRequirements` is produced by an earlier step's `saveData` or declared in `inputs`.

## Comments & best practices
- 🟠 `validate` and `meetsRequirements` have a leading JSDoc doc comment (purpose/`@param`/`@returns`) — near-universal convention.
- 🟡 `generate` with real logic (not a trivial `return defaultPayload;` passthrough) should have a doc comment; non-trivial logic should have inline comments.
- Recommended (don't block): wrap real logic in `try/catch` with a safe fallback; make `validate` do meaningful checks. `console.*` in catch blocks is fine — don't flag.

## inputs / saveData / defaultPayload coherence
- 🟠 `inputs.jsonSchema` is draft-07 with `additionalProperties: false`; `required` lists only real `properties`.
- 🟠 `defaultPayload` values satisfy `inputs` constraints (e.g. `pan` matches `^[A-Z]{5}[0-9]{4}[A-Z]$`).
- 🔴 `saveData` values are valid JSONPath; saved keys are exactly what later steps read; `APPEND#`/`EVAL#` prefixes used correctly.

## Cross-file
- 🔴 A new flow file must be registered in `config/flows/index.yaml` (`$ref` + `id` + `usecase` + `tags` + `description`).
- 🟠 Error codes emitted by mock functions should exist in `config/errors/index.yaml`.
