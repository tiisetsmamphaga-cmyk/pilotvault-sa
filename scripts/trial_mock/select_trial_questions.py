"""Choose the fixed 25-question trial mock exam for each subject.

Input: a JSON list of question metadata (id, s=subject, t=topic, q=stem, img, eimg, card, tr, n),
exported from the questions table. eimg is true when the explanation has an image that renders in the
app (it passes the approved-folder gates in explanation-image.tsx). Output: {subject: [ids]} written
to data/trial-mock/.

Rules
- 25 questions per subject; CPL Air Law is left out (not offered in the trial).
- Only questions whose explanation already shows a diagram are used, so every trial explanation has a
  visual. Every topic that has such questions gets at least one slot; the rest are shared in proportion
  to the topic's size in the full bank (largest remainder), never more than the topic can supply.
- If a subject has fewer than 25 questions with a diagram (Air Law), all of them are used and the
  remaining slots go to the topics not yet covered, then to the largest topics.
- Within a topic, prefer questions with a KEY FACT card, then 4-option questions, then questions
  already in the trial set, then the lowest id. Near-duplicate stems are skipped.
"""
import difflib
import json
import pathlib
import re
import sys
from collections import defaultdict

PER_SUBJECT = 25
SKIP_SUBJECTS = {"cpl-air-law"}
ROOT = pathlib.Path(__file__).resolve().parents[2]


def norm(text):
    return re.sub(r"[^a-z0-9 ]", "", text.lower())


def allocate(sizes, caps, k=PER_SUBJECT):
    """One slot per topic, the rest by size (largest remainder), each topic capped at caps[t]."""
    alloc = {t: min(1, caps[t]) for t in sizes}
    while True:
        left = k - sum(alloc.values())
        open_ = [t for t in sizes if alloc[t] < caps[t]]
        if left <= 0 or not open_:
            return alloc
        total = sum(sizes[t] for t in open_)
        shares = {t: left * sizes[t] / total for t in open_}
        for t in open_:
            alloc[t] = min(caps[t], alloc[t] + int(shares[t]))
        left = k - sum(alloc.values())
        for t in sorted(open_, key=lambda t: (shares[t] - int(shares[t]), sizes[t]), reverse=True):
            if left <= 0:
                break
            if alloc[t] < caps[t]:
                alloc[t] += 1
                left -= 1


def pick(questions, k, taken_stems):
    def score(r):
        return r["card"] + (r["n"] == 4) + 0.5 * r["tr"]

    chosen = []
    for r in sorted(questions, key=lambda r: (-score(r), r["id"])):
        if len(chosen) == k:
            break
        stem = norm(r["q"])
        if any(difflib.SequenceMatcher(None, stem, s).ratio() > 0.8 for s in taken_stems):
            continue
        chosen.append(r)
        taken_stems.append(stem)
    return chosen


def select_subject(topics):
    sizes = {t: len(qs) for t, qs in topics.items()}
    with_visual = {t: [r for r in qs if r["eimg"]] for t, qs in topics.items()}
    with_visual = {t: qs for t, qs in with_visual.items() if qs}
    stems, ids = [], []
    if sum(len(qs) for qs in with_visual.values()) >= PER_SUBJECT:
        alloc = allocate({t: sizes[t] for t in with_visual}, {t: len(qs) for t, qs in with_visual.items()})
        for topic in sorted(alloc):
            ids += [r["id"] for r in pick(with_visual[topic], alloc[topic], stems)]
        if len(ids) < PER_SUBJECT:  # duplicates were skipped: top up from any remaining visual question
            pool = [r for qs in with_visual.values() for r in qs if r["id"] not in ids]
            ids += [r["id"] for r in pick(pool, PER_SUBJECT - len(ids), stems)]
        if len(ids) < PER_SUBJECT:  # similar wording but different data (e.g. two readings of one table)
            pool = [r for qs in with_visual.values() for r in qs if r["id"] not in ids]
            ids += [r["id"] for r in pick(pool, PER_SUBJECT - len(ids), [])]
        return ids
    for qs in with_visual.values():  # too few visuals: take them all, then cover the other topics
        ids += [r["id"] for r in pick(qs, len(qs), stems)]
    rest = {t: [r for r in qs if r["id"] not in ids] for t, qs in topics.items()}
    uncovered = {t: sizes[t] for t, qs in rest.items() if qs and t not in with_visual}
    alloc = allocate(uncovered, {t: len(rest[t]) for t in uncovered}, PER_SUBJECT - len(ids)) if uncovered else {}
    for topic in sorted(alloc):
        ids += [r["id"] for r in pick(rest[topic], alloc[topic], stems)]
    if len(ids) < PER_SUBJECT:
        pool = sorted((r for qs in rest.values() for r in qs if r["id"] not in ids),
                      key=lambda r: (-sizes[r["t"] or "General"], r["id"]))
        ids += [r["id"] for r in pick(pool, PER_SUBJECT - len(ids), stems)]
    return ids


def select(rows):
    by_subject = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r["s"] not in SKIP_SUBJECTS:
            by_subject[r["s"]][r["t"] or "General"].append(r)
    result = {}
    for subject, topics in sorted(by_subject.items()):
        ids = select_subject(topics)
        assert len(ids) == PER_SUBJECT, (subject, len(ids))
        result[subject] = sorted(ids)
    return result


if __name__ == "__main__":
    rows = json.load(open(sys.argv[1]))
    out = ROOT / "data/trial-mock/trial-questions.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(select(rows), indent=1) + "\n")
    print(out)
