"""Write the Navigation picture + KEY FACT card update and its change record.

usage: python3 scripts/question_audit/nav_visuals_apply.py <before.json> <out.sql>
<before.json> is the live rows (id, question, is_hidden, explanation_image_url, explanation_image_title,
explanation_visual_template) for subject navigation. Questions on the textbook figures in
navigation/refined-batch-1 are left as they are; every other question gets its new picture and card
(nav_pictures.PICTURE) or a card only (nav_pictures.CARD_ONLY), which also drops the old generic SVG.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from nav_cards import CARDS  # noqa: E402
from nav_pictures import CARD_ONLY, PICTURE, PICTURE_TITLE  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
RECORD = REPO / "data/content-fixes/nav-visuals-2026-10-07.json"
FIELDS = ("explanation_image_url", "explanation_image_title", "explanation_visual_template")


def main():
    before = {r["id"]: r for r in json.loads(Path(sys.argv[1]).read_text())}
    rows, updates = [], []
    for qid, r in sorted(before.items()):
        if qid in PICTURE:
            after = {"explanation_image_url": PICTURE[qid], "explanation_image_title": PICTURE_TITLE[qid],
                     "explanation_visual_template": CARDS[qid]}
            why = "old generic drawing failed check.py; phone-first picture and KEY FACT card"
        elif qid in CARD_ONLY:
            after = {"explanation_image_url": None, "explanation_image_title": None,
                     "explanation_visual_template": CARDS[qid]}
            why = "no picture adds anything; old generic drawing removed, KEY FACT card shown with the explanation"
        else:
            assert "/refined-batch-1/" in (r["explanation_image_url"] or ""), qid
            continue
        if all(r[f] == after[f] for f in FIELDS):
            continue
        rows.append({"id": qid, "question": r["question"], "is_hidden": r["is_hidden"], "why": why,
                     "before": {f: r[f] for f in FIELDS}, "after": after})
        updates.append({"id": qid, **after})
    RECORD.write_text(json.dumps({
        "date": "2026-10-07", "subject": "navigation",
        "change": "Replaced the old generic Navigation drawings with phone-first pictures "
                  "(scripts/trial_visuals/nav_phone.py) and gave every question a KEY FACT card.",
        "rows": rows}, indent=1, ensure_ascii=False) + "\n")
    payload = json.dumps(updates, ensure_ascii=False)
    assert "$j$" not in payload
    Path(sys.argv[2]).write_text(
        "update questions q set explanation_image_url = v.explanation_image_url, "
        "explanation_image_title = v.explanation_image_title, explanation_image_caption = null, "
        "explanation_visual_template = v.explanation_visual_template\n"
        f"from jsonb_to_recordset($j${payload}$j$::jsonb) as v(id int, explanation_image_url text, "
        "explanation_image_title text, explanation_visual_template text)\n"
        "where q.id = v.id and q.subject = 'navigation';\n")
    print(f"{len(rows)} rows; record {RECORD.relative_to(REPO)}; sql {sys.argv[2]}")


if __name__ == "__main__":
    main()
