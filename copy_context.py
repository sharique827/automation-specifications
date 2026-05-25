"""
Copies the `context` block from each API in GOLD_LOAN.yaml
and replaces the corresponding `context` in PERSONAL_LOAN.yaml.
APIs missing from Personal Loan (e.g. init, on_init) are added wholesale.
"""
import sys
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
import copy

GOLD_PATH   = Path("config/attributes/GOLD_LOAN.yaml")
PERSONAL_PATH = Path("config/attributes/PERSONAL_LOAN.yaml")

# --- load both files with round-trip parser so all data is preserved ---
ryaml = YAML()
ryaml.preserve_quotes = True

with open(GOLD_PATH) as f:
    gold = ryaml.load(f)

with open(PERSONAL_PATH) as f:
    personal = ryaml.load(f)

gold_attrs     = gold["attribute_set"]
personal_attrs = personal["attribute_set"]

# APIs in Gold Loan that are loan-core (skip issue-management APIs)
SKIP_APIS = {"issue", "on_issue", "on_issue_status"}

copied, added = [], []

for api_name, api_data in gold_attrs.items():
    if api_name in SKIP_APIS:
        continue
    if not isinstance(api_data, dict) or "context" not in api_data:
        continue

    gold_ctx = copy.deepcopy(api_data["context"])

    if api_name in personal_attrs:
        personal_attrs[api_name]["context"] = gold_ctx
        copied.append(api_name)
    else:
        # API entirely missing — add the full section from Gold Loan
        personal_attrs[api_name] = copy.deepcopy(api_data)
        added.append(api_name)

# --- write back with Personal Loan's 4-space indentation style ---
out_yaml = YAML()
out_yaml.preserve_quotes = True
out_yaml.best_map_flow_style = False
out_yaml.indent(mapping=4, sequence=4, offset=2)
out_yaml.width = 10000  # prevent line-wrapping

with open(PERSONAL_PATH, "w") as f:
    out_yaml.dump(personal, f)

print(f"Context replaced in : {copied}")
print(f"APIs added          : {added}")
print("Done — PERSONAL_LOAN.yaml updated.")
