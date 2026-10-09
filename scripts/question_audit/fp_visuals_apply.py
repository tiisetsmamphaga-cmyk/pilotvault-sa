"""Write the Flight Planning picture + KEY FACT card update for one batch, and its change record.

usage: python3 scripts/question_audit/fp_visuals_apply.py <batch> <before.json> <out.sql>
<before.json> is the live rows (id, question, is_hidden, explanation_image_url, explanation_image_title,
explanation_visual_template) for subject flight-planning. Questions in fp_pictures.PICTURE get that picture and
their card; questions in fp_pictures.CARD_ONLY lose any old drawing and show the card alone.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fp_cards import CARDS  # noqa: E402
from fp_pictures import CARD_ONLY, PICTURE, PICTURE_TITLE  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
DATES = {"b1": "2026-10-07", "b2": "2026-10-08"}
FIELDS = ("explanation_image_url", "explanation_image_title", "explanation_visual_template")


def main():
    batch, before_path, sql_path = sys.argv[1:4]
    DATE = DATES[batch]
    record = REPO / f"data/content-fixes/fp-visuals-{batch}-{DATE}.json"
    before = {r["id"]: r for r in json.loads(Path(before_path).read_text())}
    rows, updates = [], []
    for qid in sorted(set(PICTURE) | set(CARD_ONLY)):
        r = before[qid]
        if qid in PICTURE:
            after = {"explanation_image_url": PICTURE[qid], "explanation_image_title": PICTURE_TITLE[qid],
                     "explanation_visual_template": CARDS[qid]}
            why = "phone-first picture and KEY FACT card"
        else:
            after = {"explanation_image_url": None, "explanation_image_title": None,
                     "explanation_visual_template": CARDS[qid]}
            why = "KEY FACT card with the working, shown with the explanation (no picture adds anything)"
        if all(r[f] == after[f] for f in FIELDS):
            continue
        rows.append({"id": qid, "question": r["question"], "is_hidden": r["is_hidden"], "why": why,
                     "before": {f: r[f] for f in FIELDS}, "after": after})
        updates.append({"id": qid, **after})
    record.write_text(json.dumps({
        "date": DATE, "subject": "flight-planning", "batch": batch,
        "change": "Flight Planning to the explanation standard: phone-first pictures and a KEY FACT card per question.",
        "rows": rows}, indent=1, ensure_ascii=False) + "\n")
    body = "[\n" + ",\n".join(json.dumps(u, ensure_ascii=False, separators=(",", ":")) for u in updates) + "\n]"
    assert "$j$" not in body
    Path(sql_path).write_text(
        "update questions q set explanation_image_url = v.explanation_image_url, "
        "explanation_image_title = v.explanation_image_title, explanation_image_caption = null, "
        "explanation_visual_template = v.explanation_visual_template\n"
        f"from jsonb_to_recordset($j${body}$j$::jsonb) as v(id int, explanation_image_url text, "
        "explanation_image_title text, explanation_visual_template text)\n"
        "where q.id = v.id and q.subject = 'flight-planning';\n")
    print(f"{len(rows)} rows; record {record.relative_to(REPO)}; sql {sql_path}")


if __name__ == "__main__":
    main()
