"""KEY FACT cards for Meteorology questions whose card was wrong (#50, the 39,000 ft tropopause) or did not answer
the question (a generic card shared with other questions). Each headline states the answer to its own question.

usage: python3 scripts/question_audit/met_key_cards.py <before.json> <out.sql>
before.json: the rows as they are live (id, explanation_visual_template). Writes the change record to
data/content-fixes/met-key-cards-2026-10-07.json and the UPDATE to <out.sql>.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def card(headline, subline, blocks, kicker="KEY FACT"):
    return {"kicker": kicker, "headline": headline, "subline": subline,
            "blocks": [{"label": a, "value": b} for a, b in blocks]}


TROPOSPHERE = card(
    "MOST WEATHER HAPPENS IN THE TROPOSPHERE, THE LOWEST LAYER",
    "IT HOLDS NEARLY ALL THE ATMOSPHERE'S WATER VAPOUR, AND TEMPERATURE FALLS WITH HEIGHT",
    [("Troposphere", "From the surface to the tropopause, about 11 km (36,000 ft) on average; almost all cloud and weather"),
     ("Tropopause", "The boundary with the stratosphere: about 8 km over the poles, up to about 18 km over the equator"),
     ("Stratosphere", "Above the tropopause; very little water vapour; contains the ozone layer"),
     ("Mesosphere and thermosphere", "Higher layers, far above where aircraft operate")])

TROPO_HEIGHT = card(
    "THE TROPOSPHERE IS ABOUT 11 KM (36,000 FT) DEEP ON AVERAGE",
    "DEEPEST OVER THE EQUATOR, SHALLOWEST OVER THE POLES",
    [("ISA tropopause", "11 km (36,090 ft), where the temperature stops falling at −56.5°C"),
     ("Over the equator", "About 16–18 km"),
     ("Over the poles", "About 8 km"),
     ("Why it varies", "Warm air columns are deeper than cold ones")])

TROPOPAUSE = card(
    "THE TROPOPAUSE SEPARATES THE TROPOSPHERE FROM THE STRATOSPHERE",
    "IT IS WHERE THE TEMPERATURE STOPS FALLING WITH HEIGHT",
    [("Height", "About 11 km (36,000 ft) on average; higher over the equator, lower over the poles"),
     ("Temperature", "About −56.5°C in the ISA"),
     ("Other boundaries", "Stratopause: stratosphere to mesosphere. Mesopause: mesosphere to thermosphere")])

OZONE = card(
    "THE OZONE LAYER ABSORBS HARMFUL ULTRAVIOLET RADIATION",
    "IT LIES IN THE STRATOSPHERE, ABOVE THE WEATHER",
    [("Where", "In the stratosphere, roughly 15–35 km up"),
     ("What it does", "Absorbs most of the sun's UV radiation before it reaches the surface"),
     ("Side effect", "Absorbing UV warms the stratosphere, so temperature rises with height there"),
     ("Not weather", "Ozone does not make cloud or rain; weather happens in the troposphere below")])

CARDS = {
    7: TROPOSPHERE, 618: TROPOSPHERE, 1484: TROPOSPHERE,
    8: TROPO_HEIGHT, 636: TROPO_HEIGHT,
    10: TROPOPAUSE, 617: TROPOPAUSE, 1474: TROPOPAUSE,
    11: OZONE, 628: OZONE,
    50: card(
        "FLYING FROM LOW TO HIGH PRESSURE WITHOUT RESETTING MAKES THE ALTIMETER UNDER-READ",
        "THE AIRCRAFT IS ACTUALLY HIGHER THAN INDICATED",
        [("Low to high pressure", "The altimeter under-reads: true altitude is higher than indicated"),
         ("High to low pressure", "The altimeter over-reads: true altitude is lower — \"high to low, look out below\""),
         ("Size of the error", "About 30 ft for every 1 hPa of difference"),
         ("The fix", "Set the new QNH on the subscale")]),
    54: card(
        "THUNDERSTORMS COME FROM CUMULONIMBUS CLOUD",
        "A CUMULONIMBUS GROWS THROUGH THREE STAGES: CUMULUS, MATURE, DISSIPATING",
        [("Cumulonimbus", "Towering cloud, often with an anvil top: lightning, heavy rain, hail and severe turbulence"),
         ("Cumulus stage", "Updraughts only; the cloud is still building"),
         ("Mature stage", "Updraughts and downdraughts side by side — the most dangerous stage"),
         ("Dissipating stage", "Downdraughts take over as the storm rains itself out")]),
    56: card(
        "DRIZZLE COMES FROM STRATUS OR STRATOCUMULUS",
        "THIN, LOW LAYER CLOUD HAS TINY DROPLETS AND WEAK UPCURRENTS, SO IT DRIZZLES RATHER THAN RAINS",
        [("Drizzle", "Very small drops (under 0.5 mm) falling close together"),
         ("Stratus and stratocumulus", "Low layer cloud: drizzle, poor visibility and low cloud bases"),
         ("Nimbostratus", "Deep layer cloud: steady, continuous rain"),
         ("Cumulonimbus", "Heavy showers, hail and thunderstorms")]),
    59: card(
        "NIMBOSTRATUS IS TYPICAL OF A WARM FRONT",
        "WARM AIR SLIDES GENTLY UP OVER THE COLD AIR, FORMING THICK LAYER CLOUD AND STEADY RAIN",
        [("Warm front cloud", "Cirrus, cirrostratus, altostratus, then nimbostratus near the front"),
         ("Nimbostratus", "Thick, dark layer cloud with continuous rain or snow"),
         ("Cold front (contrast)", "Cumulus and cumulonimbus, with showers and thunderstorms")]),
    722: card(
        "STEADY, CONTINUOUS RAIN COMES FROM NIMBOSTRATUS",
        "A THICK LAYER CLOUD, OFTEN AHEAD OF A WARM FRONT",
        [("Nimbostratus", "Thick, grey layer cloud with a low base; rain for hours"),
         ("Cumulonimbus", "Showers: heavy but short"),
         ("Stratus", "Drizzle at most"),
         ("Cirrus and fair-weather cumulus", "No significant precipitation")]),
    1498: card(
        "CIRRUS IS THE CLOUD LEAST LIKELY TO GIVE PRECIPITATION",
        "IT IS THIN, HIGH CLOUD MADE OF ICE CRYSTALS",
        [("Cirrus", "High (6–12 km), thin and wispy; nothing reaches the ground"),
         ("Nimbostratus", "Steady rain"),
         ("Cumulonimbus", "Heavy showers, hail and thunder"),
         ("Stratus", "Drizzle")]),
    1540: card(
        "CUMULONIMBUS IS THE MOST HAZARDOUS CLOUD ON A VFR FLIGHT",
        "STAY WELL CLEAR — DO NOT FLY UNDER, THROUGH OR CLOSE TO IT",
        [("Turbulence", "Severe up- and downdraughts in and around the cloud"),
         ("Icing and hail", "Heavy icing, and hail even outside the cloud under the anvil"),
         ("Lightning and downbursts", "Lightning strikes and downbursts that can be stronger than an aircraft's climb"),
         ("Visibility", "Very heavy rain cuts visibility almost to nothing")]),
    75: card(
        "A WARM, DRY WIND DESCENDING A MOUNTAIN SLOPE IS A FÖHN WIND",
        "THE AIR WARMS AS IT IS COMPRESSED ON THE WAY DOWN THE LEE SIDE",
        [("Windward side", "Moist air rises, cools and drops its moisture as cloud and rain"),
         ("Lee side", "The drier air descends and warms at the dry rate, about 3°C per 1,000 ft"),
         ("Result", "A warm, dry, often gusty wind at the foot of the mountains"),
         ("In South Africa", "The berg wind is a similar warm, dry wind blowing down from the interior"),
         ("Katabatic (contrast)", "A cold wind draining downhill at night")]),
    1503: card(
        "IN THE SOUTHERN HEMISPHERE THE TRADE WINDS BLOW FROM THE SOUTH-EAST",
        "AIR FLOWS FROM THE SUBTROPICAL HIGHS TOWARDS THE EQUATOR AND IS TURNED LEFT BY THE CORIOLIS EFFECT",
        [("Source", "The subtropical high pressure belt, around 30°S"),
         ("Direction", "Towards the equator, deflected to the left in the Southern Hemisphere: south-easterly"),
         ("Northern Hemisphere", "Deflected to the right: north-easterly trade winds"),
         ("Where they meet", "The ITCZ, near the equator"),
         ("Local example", "The Cape Doctor is a south-easterly linked to this flow")]),
    1483: card(
        "FREEZING RAIN FORMS WHEN RAIN FALLS INTO A LAYER OF AIR BELOW 0°C",
        "THE DROPS BECOME SUPERCOOLED AND FREEZE ON IMPACT AS CLEAR ICE",
        [("Set-up", "A warm layer aloft (above 0°C) over a cold layer below"),
         ("The drops", "Rain from the warm layer falls into the sub-zero layer and supercools without freezing"),
         ("On contact", "Large supercooled drops spread and freeze into heavy clear ice"),
         ("Where", "Typically ahead of a warm front — very dangerous for aircraft")]),
    1537: card(
        "CLEAR ICE IS USUALLY THE MOST DANGEROUS",
        "IT IS HEAVY, HARD TO SEE, HARD TO REMOVE AND SPREADS BACK OVER THE WING",
        [("Clear ice", "Large supercooled drops freeze slowly, flowing back into a smooth, hard, transparent layer"),
         ("Rime ice", "Small drops freeze instantly: rough, milky and brittle — lighter and easier to remove"),
         ("Hoar frost", "Deposited directly from water vapour; thin, but can still spoil lift on take-off"),
         ("Why clear ice is worst", "It adds weight quickly and changes the shape of the wing")]),
    1499: card(
        "AIR IS SATURATED WHEN ITS RELATIVE HUMIDITY IS 100%",
        "IT THEN HOLDS ALL THE WATER VAPOUR IT CAN AT THAT TEMPERATURE",
        [("Relative humidity", "The water vapour present, as a percentage of what the air could hold at that temperature"),
         ("Dew point", "The temperature the air must cool to in order to become saturated"),
         ("At saturation", "Temperature equals dew point; further cooling makes cloud or fog"),
         ("A rising parcel", "Cools at the DALR until saturated, then at the slower SALR")]),
    1494: card(
        "AN AIR MASS IS A LARGE BODY OF AIR WITH UNIFORM TEMPERATURE AND MOISTURE",
        "IT TAKES ITS PROPERTIES FROM THE SURFACE OF ITS SOURCE REGION",
        [("Size", "Hundreds to thousands of kilometres across"),
         ("Named by source", "Maritime (m, moist) or continental (c, dry); polar (P, cold) or tropical (T, warm)"),
         ("Over South Africa", "mP from the Southern Ocean, cT over the interior, mT from the Indian and Atlantic Oceans"),
         ("Fronts", "A front is where two different air masses meet")]),
    1510: card(
        "APPROACHING A WARM FRONT: CIRRUS, CIRROSTRATUS, ALTOSTRATUS, THEN NIMBOSTRATUS",
        "THE CLOUD LOWERS AND THICKENS AS THE SHALLOW FRONTAL SURFACE COMES DOWN TO MEET YOU",
        [("First", "Cirrus, often several hundred kilometres ahead of the front"),
         ("Then", "Cirrostratus (a halo round the sun), then altostratus"),
         ("Near the front", "Nimbostratus with steady rain and a lowering cloud base"),
         ("Cold front (contrast)", "Steep slope: cumulus and cumulonimbus, short heavy showers")]),
    1517: card(
        "A TROUGH IS AN AREA OF CONVERGENCE AND RISING AIR",
        "SO IT OFTEN BRINGS CLOUD, SHOWERS AND THUNDERSTORMS",
        [("Trough", "An elongated extension of low pressure: a V-shaped kink in the isobars"),
         ("Airflow", "Air converges at the surface and is forced to rise"),
         ("Weather", "Rising air cools, giving cloud and precipitation"),
         ("Ridge (contrast)", "Divergence and sinking air, usually fair weather")]),
    1481: card(
        "DESCENDING AIR WARMS, SO ITS RELATIVE HUMIDITY DECREASES",
        "THE WATER VAPOUR STAYS THE SAME, BUT WARMER AIR CAN HOLD MORE",
        [("Why it warms", "Sinking air is compressed and warms at about 3°C per 1,000 ft"),
         ("At 10°C", "100% relative humidity (saturated)"),
         ("Same air at 20°C", "52% relative humidity"),
         ("Same air at 30°C", "28% relative humidity"),
         ("In practice", "This is why sinking air in a high brings clear, dry weather")]),
}

WHY = {q: "wrong fact: tropopause averaged 39,000 ft (it is about 11 km / 36,000 ft)"
       for q in (7, 8, 10, 11, 617, 618, 628, 636, 1474, 1484)}
WHY[50] = "wrong fact: headline said high-to-low over-reads, but the question and answer are low-to-high under-reads"
for q in CARDS:
    WHY.setdefault(q, "generic card shared with other questions; headline did not answer this question")


def main():
    before = {r["id"]: r for r in json.loads(Path(sys.argv[1]).read_text())}
    assert set(before) == set(CARDS), set(CARDS) ^ set(before)
    rows = []
    for q in sorted(CARDS):
        new = json.dumps(CARDS[q], ensure_ascii=False)
        rows.append({"id": q, "question": before[q]["question"], "is_hidden": before[q]["is_hidden"], "why": WHY[q],
                     "before": {"explanation_visual_template": before[q]["explanation_visual_template"]},
                     "after": {"explanation_visual_template": new}})
    record = {"date": "2026-10-07", "subject": "meteorology",
              "change": "Corrected wrong KEY FACT cards and replaced generic ones with cards that answer each question.",
              "rows": rows}
    (REPO / "data/content-fixes/met-key-cards-2026-10-07.json").write_text(
        json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    payload = json.dumps([{"id": r["id"], "t": r["after"]["explanation_visual_template"]} for r in rows], ensure_ascii=False)
    import base64
    Path(sys.argv[2]).write_text(
        "update questions q set explanation_visual_template = r.t from jsonb_to_recordset(convert_from(decode('"
        + base64.b64encode(payload.encode()).decode()
        + "','base64'),'UTF8')::jsonb) as r(id bigint, t text) where q.id = r.id returning q.id;")
    print(len(rows), "cards")


if __name__ == "__main__":
    main()
