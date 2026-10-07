"""Restore the Meteorology questions hidden as duplicates: none of them is a word-for-word duplicate.

Before they come back, each one gets a picture and/or KEY FACT card that answers it, usually its visible twin's
(the question it was hidden in favour of). Generic cards shared by a hidden question and its twin are replaced on
both. #17 gets real wrong options in place of "Temperature decreases", "100%" and "Temperature increases".

usage: python3 scripts/question_audit/met_restore_hidden.py <hidden.json> <keeps.json> <out.sql>
hidden.json / keeps.json: the live rows (id, img, title, key, card, ...). Writes the change record to
data/content-fixes/met-hidden-restored-2026-10-07.json and the SQL to <out.sql>.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HIDDEN_RECORD = REPO / "data/content-fixes/met-duplicates-hidden-2026-10-07.json"


def card(headline, subline, blocks, kicker="KEY FACT"):
    return json.dumps({"kicker": kicker, "headline": headline, "subline": subline,
                       "blocks": [{"label": a, "value": b} for a, b in blocks]}, ensure_ascii=False)


COLD_FRONT = card("COLD AIR CUTTING UNDER WARM AIR IS A COLD FRONT",
                  "THE DENSE COLD AIR WEDGES UNDER THE WARM AIR AND LIFTS IT STEEPLY",
                  [("Cold front", "Cold air undercuts the warm air: steep slope, cumuliform cloud, heavy but short showers"),
                   ("Warm front", "Warm air slides up over the cold air: shallow slope, layered cloud, steady rain"),
                   ("Occlusion", "A cold front catches up with a warm front")])
CIRRUS = card("CIRRUS IS HIGH, THIN, WISPY CLOUD MADE OF ICE CRYSTALS",
              "THE HIGHEST CLOUD FAMILY, ABOVE THE MIDDLE-LEVEL CLOUDS",
              [("Looks like", "Thin white streaks or “mares' tails”"),
               ("Made of", "Ice crystals"),
               ("Watch", "Spreading cirrus can be the first sign of an approaching warm front")])
INVERSION_CAUSE = card("SURFACE INVERSIONS FORM BY TERRESTRIAL RADIATION ON CLEAR, CALM NIGHTS",
                       "THE GROUND LOSES HEAT AND COOLS THE AIR NEXT TO IT, LEAVING WARMER AIR ABOVE",
                       [("Clear sky", "Heat radiates away from the ground freely"),
                        ("Light or no wind", "Little mixing, so the coldest air stays at the surface"),
                        ("Inversion", "Temperature rises with height instead of falling"),
                        ("Effects", "Poor visibility, fog, smooth air, wind shear at the top")])
BLACK_SE = card("THE BLACK SOUTH EASTER BLOWS WHEN A STRONG HIGH LIES WEST OR SOUTH-WEST OF CAPE TOWN",
                "A STRONG PRESSURE GRADIENT AND A LONG SEA TRACK BRING CLOUD AND RAIN",
                [("Ordinary south easter", "Dry, with the “tablecloth” cloud over Table Mountain"),
                 ("Black south easter", "The long sea track picks up moisture: low cloud and rain"),
                 ("Pressure", "A well-developed high to the west or south-west of Cape Town")])

# hidden id -> what it gets from its twin: "all" = picture, title, visual key and card; "card" = card only
FROM_TWIN = {
    17: "all", 640: "all", 632: "all", 629: "all", 634: "all", 649: "all", 652: "all", 1526: "all",
    742: "all", 624: "all",
    654: "card", 666: "card", 670: "card", 683: "card", 687: "card", 688: "card", 691: "card", 701: "card",
    705: "card", 708: "card", 725: "card", 737: "card", 1497: "card", 1500: "card", 1514: "card", 1521: "card",
    60: "card", 693: "card", 669: "card", 727: "card", 1485: "card",
}
# id -> new card (replaces a generic one; twins listed too so the pair matches)
NEW_CARD = {63: COLD_FRONT, 1478: COLD_FRONT, 61: CIRRUS, 673: CIRRUS,
            41: INVERSION_CAUSE, 647: INVERSION_CAUSE, 1476: INVERSION_CAUSE, 77: BLACK_SE, 747: BLACK_SE}
OPTIONS_17 = {"option_a": "Humid air is denser than dry air", "option_b": "Adding water vapour has no effect on density",
              "option_c": "Humid air is less dense", "option_d": "Humid air is denser only at night"}
OLD_17 = {"option_a": "Temperature decreases", "option_b": "100%", "option_c": "Humid air is less dense",
          "option_d": "Temperature increases"}


def main():
    hidden = {r["id"]: r for r in json.loads(Path(sys.argv[1]).read_text())}
    keeps = {int(k): v for k, v in json.loads(Path(sys.argv[2]).read_text()).items()}
    twin = {h["id"]: g["keep"]["id"] for g in json.loads(HIDDEN_RECORD.read_text())["groups"] for h in g["hidden"]}
    assert set(hidden) <= set(twin), set(hidden) - set(twin)  # the 9 restored earlier are already visible
    rows, sets = [], []
    for q, how in FROM_TWIN.items():
        h, k = hidden[q], keeps[twin[q]]
        assert k["card"], q
        if how == "all":
            assert k["img"], q
            before = {"explanation_image_url": h["img"], "explanation_image_title": h["title"],
                      "explanation_visual_template": h["card"]}
            after = {"explanation_image_url": k["img"], "explanation_image_title": k["title"],
                     "explanation_visual_key": k["key"], "explanation_visual_template": k["card"]}
        else:
            before, after = {"explanation_visual_template": h["card"]}, {"explanation_visual_template": k["card"]}
        rows.append({"id": q, "change": f"picture and card from #{k['id']}" if how == "all" else f"card from #{k['id']}",
                     "before": before, "after": after})
        sets.append({"id": q, **after})
    for q, c in NEW_CARD.items():
        old = (hidden.get(q) or keeps.get(q))["card"]
        rows.append({"id": q, "change": "generic card replaced with one that answers the question",
                     "before": {"explanation_visual_template": old}, "after": {"explanation_visual_template": c}})
        sets.append({"id": q, "explanation_visual_template": c})
    rows.append({"id": 17, "change": "nonsense wrong options replaced", "before": OLD_17, "after": OPTIONS_17})
    rows.append({"ids": sorted(hidden), "change": "restored (is_hidden true -> false): no word-for-word duplicates",
                 "before": {"is_hidden": True}, "after": {"is_hidden": False}})
    record = {"date": "2026-10-07", "subject": "meteorology",
              "change": "Restored every Meteorology question hidden as a duplicate. None was a word-for-word duplicate; "
                        "questions asked a different way stay in the bank.",
              "rows": rows}
    (REPO / "data/content-fixes/met-hidden-restored-2026-10-07.json").write_text(
        json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    cols = ["explanation_image_url", "explanation_image_title", "explanation_visual_key", "explanation_visual_template"]
    payload = json.dumps(sets, ensure_ascii=False, separators=(",", ":"))
    assert "$j$" not in payload
    sql = ["begin;"]
    sql.append("update questions q set " + ", ".join(
        f"{c} = case when r ? '{c}' then r->>'{c}' else q.{c} end" for c in cols)
        + f" from jsonb_array_elements($j${payload}$j$::jsonb) r where q.id = (r->>'id')::bigint"
        + " and q.subject = 'meteorology';")
    sql.append("update questions set " + ", ".join(f"{k} = '{v}'" for k, v in OPTIONS_17.items())
               + " where id = 17 and option_b = '100%';")
    sql.append("update questions set is_hidden = false where subject = 'meteorology' and is_hidden and id in ("
               + ",".join(map(str, sorted(hidden))) + ");")
    sql.append("commit;")
    Path(sys.argv[3]).write_text("\n".join(sql) + "\n")
    print(len(sets), "picture/card updates;", len(hidden), "to restore")


if __name__ == "__main__":
    main()
