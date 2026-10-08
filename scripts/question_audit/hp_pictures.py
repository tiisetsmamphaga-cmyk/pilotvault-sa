"""Which picture each Human Performance question shows (none = KEY FACT card only).

The textbook figures already on the questions stay. New: the approach-illusion pictures in
scripts/trial_visuals/hp_phone.py, built on the manual's own Figures 8.25, 8.28a, 8.29a and 8.30; and 2207 moves
from a corrupt file to the Principles of Flight bank-angle chart.
"""
HP = "/explanation-images/human-performance/refined-batch-11/"
NEW = {
    HP + "runway-slope-illusion-v2.webp": ("Runway Slope Illusion", [2108, 2159]),
    HP + "black-hole-approach-v2.webp": ("Black Hole Approach", [2216, 2795]),
    HP + "false-horizon-v1.webp": ("False Horizon", [2214]),
    "/explanation-images/principles-of-flight/refined-batch-1/pof-bank-load-factor-v1.webp":
        ("Bank Angle and Load Factor", [2207]),
}
# The manual has no runway-width figure: these show their KEY FACT card only.
CARD_ONLY = [2072, 2158, 2797]
BROKEN = {"/explanation-images/human-performance/load-factor-bank-v7.webp"}

PICTURE, PICTURE_TITLE = {}, {}
for url, (title, ids) in NEW.items():
    for q in ids:
        PICTURE[q], PICTURE_TITLE[q] = url, title
