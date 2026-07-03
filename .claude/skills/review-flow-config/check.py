#!/usr/bin/env python3
"""Deterministic mechanical checks for FIS12 flow configs (skill: review-flow-config).

Runs the objectively-checkable subset of checklist.md so the LLM review can focus on
judgment (function logic, inputs/saveData coherence, semantics). Not a full reviewer.

Usage:
    python3 check.py config/flows/BUSINESS_LOAN/business_term_loan_without_aa.yaml [more.yaml ...]
    python3 check.py --changed          # check flow files changed vs main
    python3 check.py --index            # sanity-check config/flows/index.yaml $refs

Run from the repo root. Requires PyYAML.
Exit code is non-zero if any 🔴 blocker is found.
"""
import sys, os, re, base64, subprocess

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

FORM_APIS = {"dynamic_form", "html_form", "html_form_multi"}
BAP_ACTIONS = {"search", "select", "init", "confirm", "update", "status", "cancel", "track"}
# Always forbidden in the sandbox (any kind). `fetch`/XMLHttpRequest handled per-kind below
# (generate may fetch when allow-listed; validate/meetsRequirements must stay pure).
FORBIDDEN = ["eval(", "Function(", "Worker(", "require(", "process.", "Buffer", "__proto__",
             "while(true)", "for(;;)", "with(", "globalThis", "__dirname", "__filename", "module.exports"]
# api -> (yaml field, expected JS declaration)
FN_DECL = {"generate": "function generate", "validate": "function validate",
           "requirements": "function meetsRequirements"}

blockers = 0


def emit(sev, path, msg):
    global blockers
    if sev == "BLOCK":
        blockers += 1
    icon = {"BLOCK": "🔴", "WARN": "🟠", "NIT": "🟡", "OK": "✅"}[sev]
    print(f"  {icon} {msg}")


def load_actions():
    with open("config/actions/index.yaml") as f:
        return yaml.safe_load(f)


def check_flow(path, actions):
    print(f"\n▸ {path}")
    if not os.path.isfile(path):
        emit("BLOCK", path, "file does not exist")
        return
    raw = open(path).read()
    doc = yaml.safe_load(raw)

    meta = doc.get("meta", {}) or {}
    steps = doc.get("steps", []) or []

    # --- A: metadata ---
    if meta.get("domain") != "ONDC:FIS12":
        emit("BLOCK", path, f"meta.domain is {meta.get('domain')!r}, expected ONDC:FIS12")
    if str(meta.get("version")) != "2.3.0":
        emit("BLOCK", path, f"meta.version is {meta.get('version')!r}, expected 2.3.0")
    fid = os.path.splitext(os.path.basename(path))[0]
    if meta.get("flowId") != fid:
        emit("WARN", path, f"meta.flowId {meta.get('flowId')!r} != filename {fid!r}")

    # --- action ids unique (base id = before any '#') ---
    ids = [str(s.get("action_id", "")).split("#")[0] for s in steps]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        emit("WARN", path, f"duplicate action_id(s): {sorted(dupes)} — disambiguate (e.g. suffix) unless intentional")

    # --- B: sequence / owner / responseFor ---
    succ = actions["supportedActions"]
    proto = []
    for s in steps:
        api = str(s.get("api", "")).strip()
        api_l = api.lower()
        # C: casing
        if api != api_l:
            emit("WARN", path, f"step {s.get('action_id')}: api {api!r} not lowercase")
        # owner
        owner = s.get("owner")
        if api_l in FORM_APIS:
            expect = None  # form steps: owner convention varies (commonly BPP) — don't enforce
        elif api_l.startswith("on_"):
            expect = "BPP"
        elif api_l in BAP_ACTIONS:
            expect = "BAP"
        else:
            expect = None
        if expect and owner != expect:
            emit("BLOCK", path, f"step {s.get('action_id')} ({api_l}): owner {owner!r}, expected {expect}")
        # responseFor sanity (skip form apis — not protocol request/response)
        rf = s.get("responseFor")
        if api_l not in FORM_APIS:
            if api_l.startswith("on_") and not s.get("unsolicited") and not rf:
                emit("WARN", path, f"solicited callback {s.get('action_id')} ({api_l}) has null responseFor")
            if not api_l.startswith("on_") and rf:
                emit("WARN", path, f"request step {s.get('action_id')} ({api_l}) has responseFor={rf!r} (expected null)")
        if api_l not in FORM_APIS:
            proto.append(api_l)

    if proto:
        if proto[0] not in (succ.get(None) or succ.get("null") or []):
            emit("BLOCK", path, f"first action {proto[0]!r} not a valid start (allowed: {succ.get('null')})")
        for a, b in zip(proto, proto[1:]):
            allowed = succ.get(a) or []
            if b not in allowed:
                emit("BLOCK", path, f"invalid transition {a} -> {b} (allowed from {a}: {allowed})")

    # --- D (context template) + E (mock fn quality & comments), per step ---
    for s in steps:
        aid = s.get("action_id")
        api_l = str(s.get("api", "")).lower()
        mock = s.get("mock", {}) or {}
        dp = mock.get("defaultPayload", {}) or {}
        ctx = dp.get("context", {}) or {}
        # context inside defaultPayload is a template the runner (generateContext)
        # overwrites at runtime — transaction_id/message_id/timestamp legitimately drift,
        # so we only flag domain/version/action (copy-paste hygiene) as WARN, not blockers.
        if ctx:
            if ctx.get("action") and str(ctx["action"]).lower() != api_l:
                emit("WARN", path, f"{aid}: context.action {ctx.get('action')!r} != api {api_l!r}")
            if ctx.get("domain") and ctx["domain"] != meta.get("domain"):
                emit("WARN", path, f"{aid}: context.domain != meta.domain")
            if ctx.get("version") and str(ctx["version"]) != str(meta.get("version")):
                emit("WARN", path, f"{aid}: context.version != meta.version")

        # E: decode each mock function and check sandbox + best-practices + comments
        for kind, decl in FN_DECL.items():
            b = mock.get(kind)
            if not b:
                emit("WARN", path, f"{aid}: missing mock.{kind}")
                continue
            try:
                src = base64.b64decode(str(b)).decode(errors="replace")
            except Exception:
                emit("BLOCK", path, f"{aid} {kind}: base64 does not decode")
                continue
            nocmt = re.sub(r"//.*", "", re.sub(r"/\*.*?\*/", "", src, flags=re.S))  # strip comments

            # sandbox-forbidden tokens
            for tok in FORBIDDEN:
                if tok in src:
                    emit("BLOCK", path, f"{aid} {kind}: sandbox-forbidden token {tok!r}")
            # fetch/XHR: allowed only in generate (needs allow-list); never in pure fns
            if re.search(r"\bfetch\s*\(|XMLHttpRequest", nocmt):
                if kind == "generate":
                    emit("NIT", path, f"{aid} generate: uses fetch — needs allowedFetchBaseUrls configured at service boot")
                else:
                    emit("BLOCK", path, f"{aid} {kind}: fetch/XHR in a pure function ({kind} must have no side effects)")
            # correct declaration
            if decl not in src:
                emit("WARN", path, f"{aid} {kind}: no `{decl}(...)` declaration found (runner parses as-is)")
            # trivial passthrough generate (`return defaultPayload;`) — a legit, common
            # pattern for steps that need no customization; don't nag it for comments.
            is_stub_gen = kind == "generate" and re.fullmatch(
                r"\s*async\s+function\s+generate\([^)]*\)\s*\{\s*return\s+defaultPayload;?\s*\}\s*",
                nocmt) is not None
            # doc comment (near-universal convention: 99% of validate/requirements)
            if not re.match(r"\s*(/\*|//)", src) and not is_stub_gen:
                sev = "NIT" if kind == "generate" else "WARN"
                emit(sev, path, f"{aid} {kind}: no leading doc comment — add a JSDoc block (purpose/@param/@returns)")
            # return shape for the two predicate functions
            if kind in ("validate", "requirements") and not re.search(r"return\s*\{[^}]*\bvalid\b", nocmt):
                emit("BLOCK", path, f"{aid} {kind}: must return {{ valid, code, description }}")
            # async/await correctness for generate (avoids DataCloneError)
            if kind == "generate":
                if re.search(r"\bawait\b", nocmt) and not re.search(r"async\s+function\s+generate", src):
                    emit("BLOCK", path, f"{aid} generate: uses await but is not declared async")
                if re.search(r"generateConsentHandler\s*\(", nocmt) and not re.search(r"await\s+generateConsentHandler", nocmt):
                    emit("BLOCK", path, f"{aid} generate: generateConsentHandler must be awaited (nested Promise not auto-flattened)")

    print("  (best practices: try/catch + real validation are recommended but not enforced; "
          "semantic rules F/G/H — inputs/saveData coherence, examples, registration — need LLM review)")


def check_index():
    print("\n▸ config/flows/index.yaml ($ref resolution)")
    doc = yaml.safe_load(open("config/flows/index.yaml"))
    for fl in doc.get("flows", []) or []:
        ref = (fl.get("config") or {}).get("$ref")
        if not ref:
            continue
        p = os.path.normpath(os.path.join("config/flows", ref))
        if not os.path.isfile(p):
            emit("BLOCK", "flows/index.yaml", f"$ref does not resolve: {ref}")
        else:
            emit("OK", "flows/index.yaml", f"{fl.get('id')} -> {ref}")


def changed_flow_files():
    out = subprocess.run(["git", "diff", "--name-only", "main...HEAD"],
                         capture_output=True, text=True).stdout
    return [l for l in out.splitlines() if re.match(r"config/flows/.+/.+\.yaml$", l)]


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    if "--index" in args:
        check_index()
        args = [a for a in args if a != "--index"]
    files = []
    if "--changed" in args:
        files += changed_flow_files()
        args = [a for a in args if a != "--changed"]
    files += args
    if files:
        actions = load_actions()
        for f in files:
            check_flow(f, actions)
    print(f"\n=== {blockers} blocker(s) found ===")
    sys.exit(1 if blockers else 0)


if __name__ == "__main__":
    main()
