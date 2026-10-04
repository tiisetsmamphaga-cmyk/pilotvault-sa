"""Choose the fixed 25-question trial mock exam for each subject.

Input: a JSON list of question metadata (id, s=subject, t=topic, q=stem, img, eimg, card, tr, n),
exported from the questions table. Output: {subject: [ids]} written to data/trial-mock/.

Rules
- 25 questions per subject; CPL Air Law is left out (not offered in the trial).
- Every topic with at least 3 questions gets one slot; the remaining slots go to topics in
  proportion to their size (largest remainder).
- Within a topic, prefer questions that show a diagram or key card in the explanation, then
  4-option questions, then questions already in the trial set, then the lowest id.
- Near-duplicate stems are skipped so the 25 are all different questions.
"""
import difflib
import json
import pathlib
import re
import sys
from collections import defaultdict

PER_SUBJECT = 25
MIN_TOPIC_SIZE = 3
SKIP_SUBJECTS = {"cpl-air-law"}
ROOT = pathlib.Path(__file__).resolve().parents[2]


def norm(text):
    return re.sub(r"[^a-z0-9 ]", "", text.lower())


def allocate(sizes):
    eligible = {t: n for t, n in sizes.items() if n >= MIN_TOPIC_SIZE}
    alloc = {t: 1 for t in eligible}
    left = PER_SUBJECT - len(alloc)
    total = sum(eligible.values())
    shares = {t: left * n / total for t, n in eligible.items()}
    for t, share in shares.items():
        alloc[t] += int(share)
    left = PER_SUBJECT - sum(alloc.values())
    for t in sorted(shares, key=lambda t: shares[t] - int(shares[t]), reverse=True)[:left]:
        alloc[t] += 1
    for t in alloc:  # never ask a topic for more than it has
        alloc[t] = min(alloc[t], eligible[t])
    return alloc


def pick(questions, k, taken_stems):
    def score(r):
        return (2 * r["eimg"] + r["card"]) + (r["n"] == 4) + 0.5 * r["tr"]

    ranked = sorted(questions, key=lambda r: (-score(r), r["id"]))
    chosen = []
    for r in ranked:
        if len(chosen) == k:
            break
        stem = norm(r["q"])
        if any(difflib.SequenceMatcher(None, stem, s).ratio() > 0.8 for s in taken_stems):
            continue
        chosen.append(r)
        taken_stems.append(stem)
    return chosen


def select(rows):
    by_subject = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r["s"] not in SKIP_SUBJECTS:
            by_subject[r["s"]][r["t"] or "General"].append(r)
    result = {}
    for subject, topics in sorted(by_subject.items()):
        alloc = allocate({t: len(qs) for t, qs in topics.items()})
        stems, ids = [], []
        for topic in sorted(alloc):
            ids += [r["id"] for r in pick(topics[topic], alloc[topic], stems)]
        if len(ids) < PER_SUBJECT:  # top up from the largest topics if duplicates were skipped
            pool = sorted((r for qs in topics.values() for r in qs if r["id"] not in ids),
                          key=lambda r: (-len(topics[r["t"] or "General"]), r["id"]))
            ids += [r["id"] for r in pick(pool, PER_SUBJECT - len(ids), stems)]
        assert len(ids) == PER_SUBJECT, (subject, len(ids))
        result[subject] = sorted(ids)
    return result


if __name__ == "__main__":
    rows = json.load(open(sys.argv[1]))
    out = ROOT / "data/trial-mock/trial-questions.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(select(rows), indent=1) + "\n")
    print(out)
