"""Navigation trial set (the fixed 25-question trial mock), 2026-10-08.

The user is picking the trial pictures so that none repeats. 1592 (RAS/CAS, pitot-static scan) gives way to
1664 (rate of climb, the climb and descent planning picture), and 1591 (TAS, TAS-with-altitude scan) to 1604
(compass acceleration error), and 1816 (measuring a track, protractor) to 1663 (TAS from groundspeed and
headwind); all three stay in the bank with their pictures. 1552 (lighted obstacle chart symbol, picture in the
question) replaces 1885 (track from drift), which shared the triangle of velocities with 1841 and 1882.
1609 (140 km in NM) is a card-only question: its KEY FACT card is the explanation.
"""
TRIAL = [1552, 1574, 1604, 1608, 1609, 1621, 1628, 1663, 1664, 1691, 1694, 1730, 1741, 1762, 1765, 1772, 1775, 1785,
         1790, 1804, 1841, 1882, 1913, 1914, 1933]

# id -> (picture url, title); only questions whose picture changes
PICTURE = {}

# id -> card; only questions whose card changes
CARDS = {}
