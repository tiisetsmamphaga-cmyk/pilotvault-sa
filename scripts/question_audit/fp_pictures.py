"""Which picture each Flight Planning question shows (none = KEY FACT card only).

Batch 1 (2026-10-07): questions that reuse the Navigation and Meteorology pictures, and the card-only questions
(table and chart readings, fuel sums, weight definitions). Batch 2 (2026-10-08): the new flight-planning pictures
drawn in scripts/trial_visuals/fp_phone.py.
"""
NAV = "/explanation-images/navigation/refined-batch-2/"
MET_DA = "/explanation-images/meteorology/refined-batch-2/density-altitude-v3.webp"

REUSED = {
    NAV + "climb-descent-v1.webp": ("Climb and Descent Planning",
                                    [2239, 2296, 2348, 2257, 2260, 2271, 2279, 2312, 2329, 2398]),
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

FP = "/explanation-images/flight-planning/refined-batch-1/"
NEW = {
    FP + "takeoff-distance-v1.webp": ("Take-off Distance",
                                      [2247, 2317, 2320, 2330, 2358, 2381, 2382, 2383, 2384, 2385, 2248, 2393, 2394, 2395,
                                       2288, 2293, 2269, 2306, 2336, 2339, 2326, 2352, 2396, 2397]),
    FP + "landing-distance-v1.webp": ("Landing Distance", [2266, 2281, 2313, 2389, 2315, 2380, 2301, 2356]),
    FP + "glide-range-v1.webp": ("Glide Range", [2250, 2253, 2274, 2304, 2360]),
    FP + "climb-rate-fig-1-7-v1.webp": ("Figure 1-7: Rate of Climb", [2305]),
    FP + "cg-moment-v1.webp": ("Moment and Centre of Gravity",
                               [2263, 2295, 2299, 2303, 2331, 2340, 2355, 2368, 2369, 2401, 2402, 2411, 2417]),
    FP + "displaced-threshold-v1.webp": ("Displaced Threshold",
                                         [2245, 2251, 2366, 2267, 2273, 2278, 2333, 2350, 2314, 2412]),
    FP + "declared-distances-v1.webp": ("Declared Distances", [2297, 2298, 2391]),
    FP + "runway-slope-v1.webp": ("Runway Slope", [2255, 2277, 2319, 2409, 2413]),
    FP + "aquaplaning-v1.webp": ("Aquaplaning", [2276, 2285, 2300, 2367]),
    FP + "windshear-v1.webp": ("Wind Shear", [2241, 2264, 2259, 2307, 2328, 2361]),
    FP + "wake-turbulence-v1.webp": ("Wake Turbulence", [2287, 2362, 2363, 2364]),
    FP + "asi-arcs-v1.webp": ("Airspeed Indicator Markings", [2254, 2258, 2365]),
    FP + "vx-vy-v1.webp": ("VX and VY", [2342, 2349, 2390]),
}

PICTURE, PICTURE_TITLE = {}, {}
for url, (title, ids) in {**REUSED, **NEW}.items():
    for q in ids:
        PICTURE[q], PICTURE_TITLE[q] = url, title

assert not set(PICTURE) & set(CARD_ONLY)
assert sum(len(ids) for _, ids in {**REUSED, **NEW}.values()) == len(PICTURE)
