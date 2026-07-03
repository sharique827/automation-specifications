# Copilot instructions — ONDC:FIS12 automation specifications

This repo holds the **ONDC:FIS12 v2.3.0** domain spec + mock/flow configs used by the
automation playground (`@ondc/automation-mock-runner`). It is config, not an app.

## Layout

- `config/flows/<UseCase>/<FlowId>.yaml` — individual transaction flow configs (the main review target).
- `config/flows/index.yaml` — flat manifest of active flows (`$ref` into the files above).
- `config/actions/index.yaml` — `supportedActions` (action-transition graph) + `apiProperties` (async predecessor / transaction partner).
- `config/errors/index.yaml` — error codes.
- `config/attributes/index.yaml` — `$ref` list of per-use-case attribute files.
- `config/attributes/*.yaml`, `config/validations/index.yaml`, `config/specs/openapi.yaml` — **large generated files**; do not line-review, only flag obvious YAML/`$ref` breakage.

## A flow config, in brief

`meta` (domain/version/flowId) → `transaction_data` (shared ids) → `steps[]`. Each step has
`api`, `action_id`, `owner` (BAP/BPP), `responseFor`, `unsolicited`, `description`, and a
`mock` block. `mock.generate` / `mock.validate` / `mock.requirements` are **base64-encoded
JavaScript**; `mock.defaultPayload` / `saveData` / `inputs` shape the payload and session.

## Review priorities (see `.github/instructions/*.instructions.md` for the full rules)

1. Step `api` sequence must be a valid path through `config/actions/index.yaml` `supportedActions`; `owner` and `responseFor` must match the action (BAP for requests, BPP for `on_*`).
2. `context` inside `defaultPayload` must agree with `meta` and `transaction_data` (domain, version, transaction_id, and `context.action` == step `api`).
3. Decode base64 mock functions; reject sandbox-forbidden APIs (`eval`, `Function`, `fetch`, `require`, `process`, `Buffer`, `while(true)`, …).
4. `inputs` / `saveData` / `defaultPayload` must be coherent; new flow files must be registered in `config/flows/index.yaml`.
5. Step `api` values must be lowercase (`dynamic_form`, not `DYNAMIC_FORM`).

Authoritative source: the Mock Runner **Author's Guide** (`@ondc/automation-mock-runner`
`CLAUDE.md` / `README.md`) and this repo's `README.md` + `config/docs/*`.
