---
name: review-flow-config
description: Review a PR or working diff that changes ONDC:FIS12 mock/flow configs under config/ (flow YAMLs, flows/actions/errors/attributes index files). Decodes the base64 generate/validate/requirements functions and checks them against the Mock Runner Author's Guide and the action graph. Use when reviewing changes to config/flows/**, config/actions/index.yaml, config/errors/index.yaml, config/flows/index.yaml, or config/attributes/index.yaml. Skips the big files (attributes/*.yaml, validations, openapi).
---

# Review FIS12 flow / mock configs

Review the changed `config/` files against `checklist.md` (in this folder — the canonical
rule set) and report findings. Report-only by default: do not edit files or post to the PR
unless the user explicitly asks.

## 1. Determine the diff

- If given a PR number/URL: `gh pr diff <n> --name-only` for the file list, `gh pr diff <n>` for the patch.
- Otherwise review the working diff vs the base branch (default `main`):
  `git diff --name-only main...HEAD` and `git diff main...HEAD -- config/`.
- Keep only paths under `config/`. Bucket them:
  - **Flow configs**: `config/flows/*/*.yaml` → full checklist A–H.
  - **Index/manifest**: `config/flows/index.yaml`, `config/actions/index.yaml`, `config/errors/index.yaml`, `config/attributes/index.yaml` → the "Index / manifest configs" section.
  - **Skipped big files**: `config/attributes/{UNIFIED_CREDIT,BUSINESS_LOAN,LAMF_LOAN}.yaml`, `config/validations/index.yaml`, `config/specs/openapi.yaml` → do NOT deep-review; only sanity-check the diff doesn't break YAML/`$ref` structure, and say they were skipped.

## 2. Load cross-file context (once)

Read `config/actions/index.yaml` (the `supportedActions` graph + `apiProperties`) and
`config/flows/index.yaml`. You need these for rules B (sequence/owner/responseFor) and H
(registration). Read `config/errors/index.yaml` if any mock function emits error codes.

## 3. Fast mechanical pass — run `check.py`

Run the bundled helper first; it does the deterministic subset (metadata, action-graph path,
owner, base64 decode + forbidden-token scan, `$ref` resolution) so you can focus on judgment:

```bash
python3 .claude/skills/review-flow-config/check.py <changed_flow_files...> --index
# or: python3 .claude/skills/review-flow-config/check.py --changed   # flow files changed vs main
```

Exit code is non-zero on any 🔴 blocker. Treat its output as findings to confirm, not gospel —
then do the semantic review below (rules E–H) which the script can't fully judge.

## 4. For each changed flow config — semantic review

Read the file. The step `mock.generate` / `mock.validate` / `mock.requirements` fields are
base64-encoded JS — **decode them before reviewing** (rules E–F need the source):

```bash
# decode one field value
echo '<BASE64>' | base64 -d
```

To dump every function in a flow file with context, extract the values and decode each; e.g.
in a scratch script pull `generate|validate|requirements` scalars and pipe through `base64 -d`.
Do not skip decoding — most real bugs (forbidden sandbox APIs, wrong `context.action`,
missing session keys, malformed return shape) live inside these functions.

Then walk checklist sections A–H. Cross-check the api sequence and `owner`/`responseFor`
against the action graph you loaded in step 2.

## 5. For each changed index/manifest config

Apply the matching "Index / manifest configs" rules. For `flows/index.yaml`, verify each
`config.$ref` resolves on disk (the helper's `--index` mode does this).

## 6. Report

Use the output format at the bottom of `checklist.md`: findings grouped by file, each as
`SEVERITY  file:line — rule(letter) — what & why → fix`, then a per-file verdict
(**PASS** / **CHANGES REQUESTED**) and a summary count. State explicitly which files were
skipped as "too big to line-review". Don't imply a file passed a check you didn't actually run.

## Notes

- Rules and rationale live in `checklist.md` (sections A–H, incl. **E** correctness/sandbox and **E2** comments & best practices); read it fully before reviewing.
- Sandbox-forbidden (rule E): `eval`, `Function`, `Worker`, `require`, `process`, `Buffer`, `globalThis`, `__dirname`, `__filename`, `module`/`exports`, `__proto__`, `while(true)`, `for(;;)`, `with`. `fetch`/`XMLHttpRequest` only in `generate` (allow-listed) — never in `validate`/`meetsRequirements`.
- Comments/best-practices (rule E2): flag missing JSDoc on `validate`/`meetsRequirements` (WARN) and on non-stub `generate` (nit); `generate` using `await` must be `async` and must await `generateConsentHandler`. Do NOT flag: missing try/catch, `return defaultPayload;` stubs, no-op validators, or `console.*` — these are the repo norm (measured), not defects.
- BAP actions: `search select init confirm update status cancel track`. BPP: every `on_*`. Form apis (`dynamic_form`/`html_form`) are local UI steps — owner varies (commonly BPP), don't flag owner on them.
- If the user asks to post the review, use `gh pr comment` (summary) or `gh api` for inline comments — only when explicitly requested.
