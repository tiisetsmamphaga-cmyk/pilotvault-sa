"""Replace AI-style dashes (—, --, spaced – and spaced - between words) with ordinary punctuation."""
import json, re

DASH = r"(?:\s*—\s*|\s*--\s*|\s+–\s+|(?<=[^\s\d=+×÷/<>]) - (?=[^\s\d=]))"
DASH_RE = re.compile(DASH)
RANGE = re.compile(r"(?<=[\d°%])\s+–\s+(?=[\d°])")           # 180° – 359° → 180°–359°
CONT = set("""which who whom whose where when so and but or as since because while whereas though although yet
leaving making meaning giving producing shifting creating causing allowing letting forcing turning keeping
repeated often typically usually especially e.g. i.e. for not unlike including such even exactly just
particularly mainly mostly only plus with without rather than then""".split())
PRON = set("it this that these those they there he she we you its".split())
VERBS = set("""is are was were be been being has have had can cannot can't will won't would must may might should shall
does do did doesn't don't didn't isn't aren't wasn't include includes means mean makes make gives give keeps keep
falls fall rises rise stays stay remains remain becomes become changes change occurs occur happens happen lets let
needs need sits sit reads read shows show acts act works work takes take puts put brings bring produces produce
causes cause increases increase decreases decrease drops drop moves move flows flow forms form applies apply
requires require depends depend matters matter happens""".split())


def upper_label(left, right):
    """Chart axis names quoted from the manual, e.g. RATE OF CLIMB - FPM: keep."""
    lw = re.findall(r"[A-Za-z]+", left[-25:])
    rw = re.findall(r"[A-Za-z°]+", right[:12])
    return bool(lw and rw and lw[-1].isupper() and len(lw[-1]) > 1 and (rw[0].isupper() or rw[0].startswith("°") or rw[0] in ("degC",)))


def is_clause(rest):
    words = re.findall(r"[A-Za-z'’.]+", rest)[:8]
    if not words:
        return False
    if words[0].lower() in PRON and len(words) > 1:
        return True
    for w in words:
        lw = w.lower()
        if lw in ("that", "which", "who", "where", "whose"):
            return False
        if lw in VERBS:
            return True
    return False


def cap(s):
    i = 0
    while i < len(s) and not s[i].isalnum():
        i += 1
    return s[:i] + s[i:i + 1].upper() + s[i + 1:] if i < len(s) else s


def fix_sentence(s, card=False):
    parts = DASH_RE.split(s)
    if len(parts) == 1:
        return s
    # drop splits that are chart labels: rejoin with the original dash
    seps = DASH_RE.findall(s)
    keep = [not card and seps[i].strip() == "-" and upper_label(parts[i], parts[i + 1]) for i in range(len(seps))]
    out, i = parts[0], 0
    while i < len(seps):
        if keep[i]:
            out += seps[i] + parts[i + 1]; i += 1; continue
        # a pair: this dash and the next (non-kept) one bracket an aside
        if i + 1 < len(seps) and not keep[i + 1] and len(parts[i + 1]) <= 110:
            aside = parts[i + 1].strip()
            after = parts[i + 2]
            if "," in aside:
                out = out.rstrip() + " (" + aside + ")" + ("" if after[:1] in ".,;:!?)" else " ") + after.lstrip()
            else:
                out = out.rstrip() + ", " + aside + ("" if after[:1] in ".,;:!?)" else ", ") + after.lstrip()
            i += 2
            continue
        rest = parts[i + 1].lstrip()
        first = (re.findall(r"[A-Za-z'’.]+", rest) or [""])[0].lower()
        if card:
            out = out.rstrip() + ": " + rest
        elif first in CONT or first.rstrip(".") in CONT:
            out = out.rstrip() + ", " + rest
        elif is_clause(rest):
            out = out.rstrip().rstrip(",;:") + ". " + cap(rest)
        elif re.search(r",.*\band\b|,.*\bor\b", rest):
            out = out.rstrip() + ": " + rest
        else:
            out = out.rstrip() + ", " + rest
        i += 1
    return out


def fix_text(t, card=False):
    if not t:
        return t
    t = RANGE.sub("–", t)
    lines = t.split("\n")
    for k, ln in enumerate(lines):
        if "=" in ln and len(ln) <= 100 and not card:          # a maths line: leave its signs alone
            continue
        sents = re.split(r"(?<=[.!?])(\s+)", ln)
        lines[k] = "".join(fix_sentence(x, card) if not x.isspace() else x for x in sents)
    t = "\n".join(lines)
    t = re.sub(r",\s*,", ",", t)
    t = re.sub(r",\s*([.;:!?)])", r"\1", t)
    return t


def fix_card(js):
    if not js:
        return js
    c = json.loads(js)
    for k in ("headline", "subline", "formula"):
        if c.get(k):
            c[k] = fix_text(c[k], card=True)
    for b in c.get("blocks", []):
        b["label"] = fix_text(b["label"], card=True)
        b["value"] = fix_text(b["value"], card=True)
    new = json.dumps(c, ensure_ascii=False)
    return js if json.loads(js) == c else new
