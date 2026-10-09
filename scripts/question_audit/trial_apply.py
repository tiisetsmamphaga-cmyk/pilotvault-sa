"""Write the update for one subject's trial set (the fixed 25-question trial mock) and its change record.

usage: python3 scripts/question_audit/trial_apply.py <trial module> <live.json> <out.sql>
<trial module> is e.g. trial_air_law (TRIAL ids, PICTURE {id: (url, title)}, CARDS {id: card json}).
<live.json> is every live row of the subject (id, subject, question, is_hidden, is_trial_question,
explanation_image_url, explanation_image_title, explanation_visual_template). Questions in TRIAL become trial
questions, any other trial question of the subject stops being one, and PICTURE / CARDS replace the picture
and card where given.
"""
import importlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

REPO = Path(__file__).resolve().parents[2]
FIELDS = ("is_trial_question", "explanation_image_url", "explanation_image_title", "explanation_visual_template")


def main():
    module, live_path, sql_path = sys.argv[1:4]
    m = importlib.import_module(module)
    live = {r["id"]: r for r in json.loads(Path(live_path).read_text())}
    assert len(m.TRIAL) == 25 and len(set(m.TRIAL)) == 25, "the trial mock is exactly 25 questions"
    subject = {live[q]["subject"] for q in m.TRIAL}
    assert len(subject) == 1, subject
    subject = subject.pop()
    rows, updates = [], []
    for qid, r in sorted(live.items()):
        after = {f: r[f] for f in FIELDS}
        after["is_trial_question"] = qid in m.TRIAL
        if qid in m.PICTURE:
            after["explanation_image_url"], after["explanation_image_title"] = m.PICTURE[qid]
        if qid in m.CARDS:
            after["explanation_visual_template"] = m.CARDS[qid]
        if qid in m.TRIAL:
            assert not r["is_hidden"], qid
            assert after["explanation_image_url"] and after["explanation_visual_template"], qid
        if all(bool(r[f]) == bool(after[f]) and r[f] == after[f] for f in FIELDS):
            continue
        why = ("joins the trial set" if after["is_trial_question"] and not r["is_trial_question"] else
               "leaves the trial set (no strong picture for it)" if r["is_trial_question"] and not after["is_trial_question"]
               else "trial question: picture and/or card brought to the standard")
        rows.append({"id": qid, "question": r["question"], "why": why,
                     "before": {f: r[f] for f in FIELDS}, "after": after})
        updates.append({"id": qid, **after})
    record = REPO / f"data/content-fixes/trial-{subject}-2026-10-08.json"
    record.write_text(json.dumps({"date": "2026-10-08", "subject": subject,
                                  "change": "Trial set: 25 questions, each with a strong picture and an answer-first KEY FACT card.",
                                  "rows": rows}, indent=1, ensure_ascii=False) + "\n")
    body = "[\n" + ",\n".join(json.dumps(u, ensure_ascii=False, separators=(",", ":")) for u in updates) + "\n]"
    assert "$j$" not in body
    Path(sql_path).write_text(
        "update questions q set is_trial_question = v.is_trial_question, explanation_image_url = v.explanation_image_url, "
        "explanation_image_title = v.explanation_image_title, explanation_image_caption = null, "
        "explanation_visual_template = v.explanation_visual_template\n"
        f"from jsonb_to_recordset($j${body}$j$::jsonb) as v(id int, is_trial_question boolean, explanation_image_url text, "
        "explanation_image_title text, explanation_visual_template text)\n"
        f"where q.id = v.id and q.subject = '{subject}';\n")
    print(f"{len(rows)} rows ({sum(r['after']['is_trial_question'] for r in rows)} trial); record {record.relative_to(REPO)}")


if __name__ == "__main__":
    main()
