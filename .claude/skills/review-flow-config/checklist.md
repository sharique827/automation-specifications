# FIS12 mock/flow config review checklist

Canonical rules for reviewing changes under `config/`. Source of truth for both the
`review-flow-config` skill and `.github/instructions/*` (keep those in sync with this file).

Grounded in the **Mock Runner Author's Guide** (`@ondc/automation-mock-runner`
`CLAUDE.md` / `README.md`), this repo's `README.md`, and `config/docs/*`.

Severity legend: 🔴 blocker · 🟠 should-fix · 🟡 nit.

---

## Scope — review now vs skip

Review now (small, high-signal):

- `config/flows/<UseCase>/*.yaml` — individual flow configs (main target)
- `config/flows/index.yaml` — flow manifest
- `config/actions/index.yaml` — action graph + api properties
- `config/errors/index.yaml` — error codes
- `config/attributes/index.yaml` — attribute `$ref` list

Skip for now (too large to review line-by-line here — flag only if a diff obviously
breaks YAML/`$ref` structure): `config/attributes/{UNIFIED_CREDIT,BUSINESS_LOAN,LAMF_LOAN}.yaml`
(~500K each), `config/validations/index.yaml` (~108K), `config/specs/openapi.yaml` (~100K).

---

## A. Flow config — structure & metadata

- 🔴 `meta.domain` == `ONDC:FIS12` and `meta.version` == `2.3.0` (must match repo `README.md` / `config/index.yaml`).
- 🟠 `meta.flowId` matches the filename (snake_case, no extension).
- 🟠 `meta.description` present and non-generic; `config_version` present.
- 🟡 `transaction_data.transaction_id` is a UUID. (Do NOT require it to equal `context.transaction_id` inside `defaultPayload` — the runner's `generateContext` overwrites transaction_id/message_id/timestamp at runtime, so those template values legitimately drift.)
- 🔴 Each step has: `api`, `action_id`, `owner`, `responseFor`, `unsolicited`, `description`, `mock`.
- 🟠 `action_id` base ids (before any `#`) are unique within the file; literal duplicates are a smell unless intentional for repeated pushes.

## B. Action sequence validity — cross-check `config/actions/index.yaml`

- 🔴 Ordered `api` values form a valid path through `supportedActions`: the first api must appear under the `"null"` key (i.e. `search` or `init`), and each subsequent api must be listed among the previous api's allowed successors. **Exclude form apis** (`dynamic_form`, `html_form`, `html_form_multi`) from this path check — they are local buyer-side UI steps, not nodes in the protocol graph; check the path over the remaining protocol actions only.
- 🔴 `owner` correctness: request actions (`search`, `select`, `init`, `confirm`, `update`, `status`, `cancel`, `track`) → **BAP**; every `on_*` callback → **BPP**. Form apis (`dynamic_form`, `html_form`) are local UI steps — owner convention varies (commonly **BPP**); do NOT flag owner on form steps.
- 🔴 `responseFor`: a solicited `on_X` step must set `responseFor` to the `action_id` of the matching `X` request (consistent with `apiProperties.<action>.async_predecessor`). Request actions set `responseFor: null`.
- 🟠 `unsolicited: true` only for pushed callbacks (e.g. unsolicited `on_status`/`on_update`); those should also have `responseFor: null`. Solicited callbacks must be `unsolicited: false`.

## C. api casing

- 🟠 Step `api` MUST be lowercase (`dynamic_form`, `html_form`, `on_search`), never `DYNAMIC_FORM`/`HTML_FORM`. The runner only accepts uppercase via `convertToFlowConfig`; raw configs use lowercase. (Repo currently mixes both — flag new uppercase.)

## D. context ↔ meta consistency (inside `mock.defaultPayload`)

The `context` in `defaultPayload` is a template; the runner (`generateContext`) overwrites
`transaction_id`, `message_id`, and `timestamp` at runtime. So only check the static fields:

- 🟠 `context.action` == the step's `api` (copy-paste hygiene).
- 🟠 `context.domain` == `meta.domain`; `context.version` == `meta.version`.
- 🟡 `bap_id`/`bap_uri`/`bpp_id`/`bpp_uri` consistent across steps.
- 🟡 `ttl` present; `location.country.code` == `IND`.
- Do NOT flag `context.transaction_id`/`message_id`/`timestamp` drift — runtime-overwritten.

## E. mock functions (`generate` / `validate` / `requirements`) — DECODE the base64

Each is base64-encoded JS. Decode before reviewing (see skill for the loop). Correctness &
sandbox rules:

- 🔴 Decodes cleanly and parses as a COMPLETE function declaration (the runner parses as-is, does not wrap): `function generate(defaultPayload, sessionData)`, `function validate(targetPayload, sessionData)`, `function meetsRequirements(sessionData)`.
- 🔴 No sandbox-forbidden tokens: `eval`, `Function`, `Worker`, `require`, `process`, `Buffer`, `global`/`globalThis`, `__dirname`, `__filename`, `module`/`exports`, `__proto__`, `while(true)`, `for(;;)`, `with`. (`setTimeout` allowed, clamped 1–35000ms.)
- 🔴 `fetch`/`XMLHttpRequest` are allowed ONLY in `generate` (and only with `allowedFetchBaseUrls` configured at service boot); `validate` and `meetsRequirements` MUST stay pure — flag any fetch/XHR there.
- 🔴 `validate` and `meetsRequirements` return `{ valid, code, description }`; `generate` returns the (awaited) payload object.
- 🔴 `generate` that uses `await` must be declared `async`; async helpers (esp. `generateConsentHandler`) must be `await`ed — an un-awaited Promise in the payload throws `DataCloneError`.
- 🟠 `generate` reads user input only from `sessionData.user_inputs` and prior-step values from `sessionData.<savedKey>` — every key it reads should be produced by an earlier step's `saveData` or declared in `inputs`.
- 🟡 Helpers needing request scope (`createFormURL`, `getSubscriberUrl`, `generateConsentHandler`) take `sessionData` explicitly — free-variable refs don't resolve in the sandbox.

## E2. Comments & best practices (per the Author's Guide scaffold)

The scaffolded functions ship with a JSDoc block and a defensive structure. Enforce the parts
that are genuine repo conventions; recommend (don't block) the rest.

- 🟠 `validate` and `meetsRequirements` carry a **leading doc comment** (JSDoc: purpose, `@param`, `@returns`) — ~99% do, so a missing one is a real gap.
- 🟡 `generate` with real logic (i.e. not the trivial `return defaultPayload;` passthrough) should also carry a doc comment. Trivial passthrough stubs need none — don't nag them.
- 🟡 Non-trivial logic has explanatory inline comments (e.g. `// build payload`, `// validate required fields`).
- Recommended, NOT enforced (majority of existing functions omit these — don't auto-flag, raise only when the function's logic clearly warrants it):
    - wrap real logic in `try/catch` returning a safe fallback (`generate`→`defaultPayload`; predicates→`{ valid:false, code:500, description }`);
    - `validate` doing meaningful checks (e.g. asserting `context.action`) rather than an unconditional `return { valid:true }`.
- `console.log`/`console.error` are used by the scaffold's catch blocks — do NOT flag them.

## F. inputs / saveData / defaultPayload coherence

- 🟠 `mock.inputs.jsonSchema`: draft-07, `additionalProperties: false`, `required` lists only real `properties`.
- 🟠 Every field `generate`/`meetsRequirements` treats as required exists in `inputs.properties`, and `inputs.required` ⊇ the requirements' required list.
- 🟠 `defaultPayload` example values satisfy `inputs` constraints (e.g. `pan` matches `^[A-Z]{5}[0-9]{4}[A-Z]$`).
- 🔴 `mock.saveData` values are valid JSONPath (`$.context...`); keys saved here are exactly the ones later steps read from `sessionData`. `APPEND#key` (array-append) and `EVAL#<base64>` (custom extractor) prefixes used correctly.

## G. examples

- 🟠 If `examples` present: `payload.context.action` == step `api`; `type` (`request`/`response`) matches `owner` (BAP→request, BPP→response).

## H. cross-file

- 🔴 A NEW flow file must be registered in `config/flows/index.yaml`: a `$ref` to the correct relative path, plus `id`, `usecase` (matches subfolder), `tags`, `description`. If intentionally disabled, it should be commented out — don't leave a dangling `$ref`.
- 🟠 Error codes emitted by `validate`/`requirements` should exist in `config/errors/index.yaml`.

---

## Index / manifest configs

### `config/flows/index.yaml`

- 🔴 Every `config.$ref` resolves to an existing file.
- 🟠 `id` unique per `usecase`; `usecase` matches the subfolder name.
- 🟠 `tags` from the known set: `WORKBENCH`, `PRAMAAN`, `MANDATORY`, `REPORTABLE`. Flag casing drift (`Mandatory` vs `MANDATORY`).
- 🟡 Large commented-out blocks: note them (informational — confirm they're meant to stay disabled).

### `config/actions/index.yaml`

- 🔴 Every action referenced in `supportedActions` successors and in `apiProperties.*.async_predecessor` / `transaction_partner` has a definition.
- 🟠 `apiProperties.<on_x>.async_predecessor` points to the correct request action (`on_search`→`search`, `on_init`→`init`, …).
- 🟡 Commented-out `transaction_partner` lines: confirm intent.

### `config/errors/index.yaml`

- 🔴 `code` values unique.
- 🟠 `From` ∈ {`BAP`, `BPP`}; `Event` and `Description` non-empty.

### `config/attributes/index.yaml`

- 🔴 Each `$ref` points to an existing file. Commented `$ref`s = disabled use cases; confirm intent.

---

## Output format (for the skill)

Group findings by file. For each: `SEVERITY  file:line — rule (letter) — what & why → fix`.
End with a one-line verdict per changed file: **PASS** / **CHANGES REQUESTED**, and a summary count.
Only report issues you can point to; if a rule can't be checked (e.g. big skipped file), say so explicitly rather than implying it passed.
