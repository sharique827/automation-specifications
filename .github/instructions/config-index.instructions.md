---
applyTo: "config/flows/index.yaml,config/actions/index.yaml,config/errors/index.yaml,config/attributes/index.yaml"
---

# Copilot review rules — FIS12 index / manifest configs

Small, high-signal manifest files. Severity: 🔴 blocker · 🟠 should-fix · 🟡 nit.

## `config/flows/index.yaml`
- 🔴 Every `config.$ref` resolves to an existing file.
- 🟠 `id` unique per `usecase`; `usecase` matches the subfolder name.
- 🟠 `tags` from the known set: `WORKBENCH`, `PRAMAAN`, `MANDATORY`, `REPORTABLE`. Flag casing drift (`Mandatory` vs `MANDATORY`).
- 🟡 Large commented-out entries: note them; confirm they're meant to stay disabled.

## `config/actions/index.yaml`
- 🔴 Every action referenced in a `supportedActions` successor list and in `apiProperties.*.async_predecessor` / `transaction_partner` has its own definition.
- 🟠 `apiProperties.<on_x>.async_predecessor` points to the correct request action (`on_search`→`search`, `on_init`→`init`, …).
- 🟡 Commented-out `transaction_partner` lines: confirm intent.

## `config/errors/index.yaml`
- 🔴 `code` values unique.
- 🟠 `From` ∈ {`BAP`, `BPP`}; `Event` and `Description` non-empty.

## `config/attributes/index.yaml`
- 🔴 Each `$ref` points to an existing file. Commented `$ref`s = disabled use cases; confirm intent.

The large files themselves (`config/attributes/*.yaml`, `config/validations/index.yaml`,
`config/specs/openapi.yaml`) are not line-reviewed here — only flag obvious YAML/`$ref` breakage.
