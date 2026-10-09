"""Write the Human Performance picture + KEY FACT card update and its change record.

usage: python3 scripts/question_audit/hp_visuals_apply.py <before.json> <out.sql> [record name]
<before.json> is the live rows (id, question, is_hidden, explanation_image_url, explanation_image_title,
explanation_visual_template) for subject human-performance. Every question gets its answer-first card
(hp_cards.CARDS); questions in hp_pictures.PICTURE get that picture, the others keep the textbook figure they
have (or none). A picture listed in hp_pictures.BROKEN is never kept.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hp_cards import CARDS  # noqa: E402
from hp_pictures import BROKEN, CARD_ONLY, PICTURE, PICTURE_TITLE  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
RECORD = REPO / "data/content-fixes/hp-visuals-2026-10-08.json"
FIELDS = ("explanation_image_url", "explanation_image_title", "explanation_visual_template")


def main():
    before_path, sql_path = sys.argv[1:3]
    record = REPO / "data/content-fixes" / (sys.argv[3] if len(sys.argv) > 3 else RECORD.name)
    before = {r["id"]: r for r in json.loads(Path(before_path).read_text())}
    assert set(before) == set(CARDS), "every question needs a card"
    rows, updates = [], []
    for qid in sorted(before):
        r = before[qid]
        if qid in PICTURE:
            url, title, why = PICTURE[qid], PICTURE_TITLE[qid], "new picture and answer-first KEY FACT card"
        elif qid in CARD_ONLY:
            url, title, why = None, None, "KEY FACT card only (the manual has no figure for it)"
        else:
            url, title = r["explanation_image_url"], r["explanation_image_title"]
            assert url not in BROKEN and "/refined-batch-11/" not in (url or ""), qid
            why = "answer-first KEY FACT card" + (" (textbook figure kept)" if url else ", shown with the explanation")
        after = {"explanation_image_url": url, "explanation_image_title": title, "explanation_visual_template": CARDS[qid]}
        if all(r[f] == after[f] for f in FIELDS):
            continue
        rows.append({"id": qid, "question": r["question"], "is_hidden": r["is_hidden"], "why": why,
                     "before": {f: r[f] for f in FIELDS}, "after": after})
        updates.append({"id": qid, **after})
    record.write_text(json.dumps({
        "date": "2026-10-08", "subject": "human-performance",
        "change": "Human Performance to the explanation standard: an answer-first KEY FACT card per question and "
                  "phone-first approach-illusion pictures; textbook figures kept.",
        "rows": rows}, indent=1, ensure_ascii=False) + "\n")
    body = "[\n" + ",\n".join(json.dumps(u, ensure_ascii=False, separators=(",", ":")) for u in updates) + "\n]"
    assert "$j$" not in body
    Path(sql_path).write_text(
        "update questions q set explanation_image_url = v.explanation_image_url, "
        "explanation_image_title = v.explanation_image_title, explanation_image_caption = null, "
        "explanation_visual_template = v.explanation_visual_template\n"
        f"from jsonb_to_recordset($j${body}$j$::jsonb) as v(id int, explanation_image_url text, "
        "explanation_image_title text, explanation_visual_template text)\n"
        "where q.id = v.id and q.subject = 'human-performance';\n")
    print(f"{len(rows)} rows; record {record.relative_to(REPO)}; sql {sql_path}")


if __name__ == "__main__":
    main()
