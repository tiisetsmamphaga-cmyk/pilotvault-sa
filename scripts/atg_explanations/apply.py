"""Validate ATG explanation rewrites and emit guarded SQL.

Each module in rewrites/ defines R = {question_id: {"e": explanation, "a".."d": replacement option, "q": stem}}.
Option keys are present only where a filler distractor is replaced, and "q" only where the stem itself
needs rewording; the correct answer is never changed here.

    python3 apply.py                 validate every module
    python3 apply.py airframes ...   validate and write <module>.sql next to this script's output dir

The UPDATE is guarded on the row's original correct answer, options and explanation (from
data/atg-explanations/original.json), so it only applies to a row that has not changed since the snapshot.
"""
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
REPO = HERE.parents[1]
WORK = Path(os.environ.get("ATG_WORK", "/tmp/atg-work")) / "sql"
ORIGINAL = {r["id"]: r for r in json.loads((REPO / "data/atg-explanations/original.json").read_text())}
SLOTS = {"a": "option_a", "b": "option_b", "c": "option_c", "d": "option_d"}


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / "rewrites" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.R


def md5(s):
    return hashlib.md5((s or "").encode("utf-8")).hexdigest()


def q(s):
    assert "$x$" not in s
    return f"$x${s}$x$"


def check(qid, change):
    errs, warns = [], []
    row = ORIGINAL.get(qid)
    if row is None:
        return [f"{qid}: not an ATG question"], []
    e = change.get("e", "")
    if not 180 <= len(e) <= 800:
        errs.append(f"{qid}: explanation length {len(e)}")
    if "  " in e or e != e.strip() or not e.endswith((".", ".\"", ")")):
        errs.append(f"{qid}: explanation spacing/ending")
    if re.search(r"\b(claude|opus|sonnet|anthropic)\b", e, re.I):
        errs.append(f"{qid}: model name in text")
    new = {s: change.get(k, row[s]) for k, s in SLOTS.items()}
    for k in change:
        if k not in ("e", "q", *SLOTS):
            errs.append(f"{qid}: unknown key {k}")
        elif k in SLOTS and row[SLOTS[k]] == row["correct_answer"]:
            errs.append(f"{qid}: tried to replace the correct answer in slot {k}")
    vals = list(new.values())
    if vals.count(row["correct_answer"]) != 1:
        errs.append(f"{qid}: correct answer not present exactly once")
    if len({v.strip().lower() for v in vals}) != 4:
        errs.append(f"{qid}: duplicate options")
    lens = sorted(len(v) for v in vals)
    if len(row["correct_answer"]) == lens[-1] and lens[-1] > 1.6 * lens[-2] and lens[-1] > 30:
        warns.append(f"{qid}: correct answer is by far the longest option")
    return errs, warns


FIELDS = ["question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "explanation"]
GUARD = "md5(concat_ws(chr(31), " + ", ".join(f"t.{f}" for f in FIELDS) + "))"


def row_md5(row):
    return md5("\x1f".join(row[f] for f in FIELDS))


def sql_for(changes):
    """One UPDATE for the module. Unchanged stems and options are sent as NULL; every row is guarded on
    an md5 of its original stem, options, answer and explanation, so it only applies to an unchanged row."""
    rows = []
    for qid, change in sorted(changes.items()):
        row = ORIGINAL[qid]
        vals = [q(change["e"])]
        vals.append(q(change["q"]) if change.get("q", row["question"]) != row["question"] else "null")
        for k, slot in SLOTS.items():
            vals.append(q(change[k]) if change.get(k, row[slot]) != row[slot] else "null")
        rows.append(f"({qid},{','.join(vals)},'{row_md5(row)}')")
    return (
        "update questions t set explanation=v.e, question=coalesce(v.nq, t.question),\n"
        "  option_a=coalesce(v.na, t.option_a), option_b=coalesce(v.nb, t.option_b),\n"
        "  option_c=coalesce(v.nc, t.option_c), option_d=coalesce(v.nd, t.option_d)\n"
        "from (values\n" + ",\n".join(rows) + "\n) as v(id,e,nq,na,nb,nc,nd,guard)\n"
        f"where t.id=v.id and {GUARD}=v.guard\n"
        "returning t.id;\n"
    )


def main(names):
    all_names = sorted(p.stem for p in (HERE / "rewrites").glob("*.py"))
    bad = 0
    seen = {}
    combined = {}
    for name in names or all_names:
        R = load(name)
        errs, warns = [], []
        for qid, ch in R.items():
            if qid in seen:
                errs.append(f"{qid}: also in {seen[qid]}")
            seen[qid] = name
            e, w = check(qid, ch)
            errs += e
            warns += w
        replaced = sum(1 for ch in R.values() for k in ch if k in SLOTS)
        print(f"{name}: {len(R)} questions, {replaced} options replaced, {len(errs)} errors, {len(warns)} warnings")
        for m in errs + warns:
            print("   ", m)
        bad += len(errs)
        combined.update(R)
    if names and not bad:
        WORK.mkdir(parents=True, exist_ok=True)
        out = WORK / f"{'+'.join(names)}.sql"
        out.write_text(sql_for(combined))
        print(f"wrote {out} ({len(combined)} rows)")
    if not names:
        missing = sorted(set(ORIGINAL) - set(seen))
        print(f"covered {len(seen)}/{len(ORIGINAL)}; missing: {missing[:20]}{' ...' if len(missing) > 20 else ''}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
