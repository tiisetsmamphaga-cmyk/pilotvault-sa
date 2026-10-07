"""Write the KEY FACT card update for the Navigation questions that keep their textbook figure, and its record.

usage: python3 scripts/question_audit/nav_keep_cards_apply.py <before.json> <out.sql>
<before.json> is the live rows (id, question, is_hidden, explanation_image_url, explanation_visual_template).
Only explanation_visual_template changes; the picture stays.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from nav_cards import KEEP_CARDS  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
RECORD = REPO / "data/content-fixes/nav-keep-cards-2026-10-07.json"


def main():
    before = {r["id"]: r for r in json.loads(Path(sys.argv[1]).read_text())}
    rows, updates = [], []
    for qid, tpl in sorted(KEEP_CARDS.items()):
        r = before[qid]
        assert "/navigation/refined-batch-1/" in r["explanation_image_url"], qid
        if r["explanation_visual_template"] == tpl:
            continue
        rows.append({"id": qid, "question": r["question"], "is_hidden": r["is_hidden"],
                     "why": "card stated a general rule; headline now names the answer (textbook picture kept)",
                     "before": {"explanation_visual_template": r["explanation_visual_template"]},
                     "after": {"explanation_visual_template": tpl}})
        updates.append({"id": qid, "explanation_visual_template": tpl})
    RECORD.write_text(json.dumps({
        "date": "2026-10-07", "subject": "navigation",
        "change": "Answer-first KEY FACT cards for the Navigation questions that keep their textbook figure.",
        "rows": rows}, indent=1, ensure_ascii=False) + "\n")
    body = "[\n" + ",\n".join(json.dumps(u, ensure_ascii=False, separators=(",", ":")) for u in updates) + "\n]"
    assert "$j$" not in body
    Path(sys.argv[2]).write_text(
        "update questions q set explanation_visual_template = v.explanation_visual_template\n"
        f"from jsonb_to_recordset($j${body}$j$::jsonb) as v(id int, explanation_visual_template text)\n"
        "where q.id = v.id and q.subject = 'navigation';\n")
    print(f"{len(rows)} rows; record {RECORD.relative_to(REPO)}; sql {sys.argv[2]}")


if __name__ == "__main__":
    main()
