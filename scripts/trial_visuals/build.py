"""Render the trial-mock explanation diagrams and write the DB update for them.

usage: python3 scripts/trial_visuals/build.py [module ...] [--only id,id] [--sql out.sql]
Images go to public/<url>; the record of every visual goes to data/trial-mock/trial-visuals.json.
"""
import argparse
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from kit import REPO, render, svg  # noqa: E402

MODULES = ["fp"]
RECORD = REPO / "data/trial-mock/trial-visuals.json"


def q(s):
    return "null" if s is None else "'" + str(s).replace("'", "''") + "'"


def load(mods):
    items = []
    for m in mods:
        if (HERE / f"{m}.py").exists():
            items += importlib.import_module(m).R.items
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("modules", nargs="*", default=MODULES)
    ap.add_argument("--only", default="")
    ap.add_argument("--sql")
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args()
    items = load(a.modules)
    if a.only:
        keep = {int(x) for x in a.only.split(",")}
        items = [i for i in items if i["id"] in keep]
    if not a.no_render:
        render([(svg(i["draw"](), i["w"], i["h"]), i["url"]) for i in items])
        print(f"rendered {len(items)}")
    if not a.only:
        record = {str(i["id"]): {k: i[k] for k in ("subject", "url", "title", "template")} for i in items}
        old = json.loads(RECORD.read_text()) if RECORD.exists() else {}
        old.update(record)
        RECORD.write_text(json.dumps(dict(sorted(old.items(), key=lambda kv: int(kv[0]))), indent=1, ensure_ascii=False) + "\n")
    if a.sql:
        lines = [f"update questions set explanation_image_url = {q(i['url'])}, explanation_image_title = {q(i['title'])}, "
                 f"explanation_image_caption = null, explanation_visual_template = {q(i['template'])} where id = {i['id']};"
                 for i in items]
        Path(a.sql).write_text("\n".join(lines) + "\n")
        print(a.sql)


if __name__ == "__main__":
    main()
