"""Which picture each Human Performance question shows (none = KEY FACT card only).

The textbook figures already on the questions stay (KEEP = their live picture). New: the approach-illusion
pictures drawn in scripts/trial_visuals/hp_phone.py, and 2207 moves from a corrupt file to the Principles of
Flight bank-angle chart.
"""
HP = "/explanation-images/human-performance/refined-batch-11/"
NEW = {
    HP + "runway-slope-illusion-v1.webp": ("Runway Slope Illusion", [2108, 2159]),
    HP + "runway-width-illusion-v1.webp": ("Runway Width Illusion", [2072, 2158, 2797]),
    HP + "black-hole-approach-v1.webp": ("Black Hole Approach", [2216, 2795]),
    "/explanation-images/principles-of-flight/refined-batch-1/pof-bank-load-factor-v1.webp":
        ("Bank Angle and Load Factor", [2207]),
}
BROKEN = {"/explanation-images/human-performance/load-factor-bank-v7.webp"}

PICTURE, PICTURE_TITLE = {}, {}
for url, (title, ids) in NEW.items():
    for q in ids:
        PICTURE[q], PICTURE_TITLE[q] = url, title
