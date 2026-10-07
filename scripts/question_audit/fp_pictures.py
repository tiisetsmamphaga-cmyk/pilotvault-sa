"""Which picture each Flight Planning question shows (none = KEY FACT card only).

Batch 1 (2026-10-07): questions that reuse the Navigation and Meteorology pictures, and the card-only questions
(table and chart readings, fuel sums, weight definitions). Later batches add the new flight-planning pictures.
"""
NAV = "/explanation-images/navigation/refined-batch-2/"
MET_DA = "/explanation-images/meteorology/refined-batch-2/density-altitude-v3.webp"

REUSED = {
    NAV + "climb-descent-v1.webp": ("Climb and Descent Planning",
                                    [2239, 2296, 2348, 2257, 2260, 2271, 2279, 2305, 2312, 2329, 2398]),
    NAV + "pressure-altitude-v1.webp": ("Pressure Altitude", [2283, 2371]),
    MET_DA: ("Density Altitude", [2240, 2374, 2375]),
}

CARD_ONLY = [
    # atmosphere: ISA sums
    2327, 2372, 2373,
    # airspeed calibration and stall speeds (Figures 1-1, 1-2, 1-19, 1-21)
    2242, 2249, 2290, 2291, 2292, 2323, 2334, 2335, 2343, 2347, 2351, 2354, 2357, 2403,
    # cruise, range and endurance (Figures 1-9 to 1-13, 1-23)
    2252, 2261, 2272, 2280, 2284, 2294, 2302, 2322, 2324, 2337, 2338, 2345, 2359, 2376, 2377, 2378, 2379, 2386,
    2387, 2388, 2399, 2400, 2414,
    # fuel planning
    2243, 2256, 2262, 2265, 2268, 2286, 2310, 2318, 2332, 2341, 2353, 2404, 2405, 2408, 2416,
    # mass and balance: weights, floor loading, Figures 2-2 and 2-3
    2244, 2246, 2270, 2275, 2282, 2289, 2308, 2309, 2311, 2316, 2325, 2346, 2370, 2392, 2406, 2407, 2410, 2415,
    # V-speeds with nothing to draw
    2321, 2344,
]

PICTURE, PICTURE_TITLE = {}, {}
for url, (title, ids) in REUSED.items():
    for q in ids:
        PICTURE[q], PICTURE_TITLE[q] = url, title

assert not set(PICTURE) & set(CARD_ONLY)
