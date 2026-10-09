"""Which explanation picture each Navigation question uses (docs/EXPLANATION_ILLUSTRATION_STANDARD.md).

The 23 old generic drawings are replaced by the phone-first pictures in scripts/trial_visuals/nav_phone.py
(navigation/refined-batch-2). Questions already on textbook figures (refined-batch-1) keep them. Questions that
need no picture get a KEY FACT card only (CARD_ONLY). Every question also gets its own card (nav_cards.py).
"""
B2 = "/explanation-images/navigation/refined-batch-2/"
B1 = "/explanation-images/navigation/refined-batch-1/"
MET_DA = "/explanation-images/meteorology/refined-batch-2/density-altitude-v3.webp"
TAS_FIG = B1 + "nav-tas-increase-with-altitude-v1.webp"

TITLES = {
    "variation-deviation-v1": "Variation and Deviation", "wind-drift-v1": "Heading, Track and Drift",
    "one-in-sixty-v1": "The 1 in 60 Rule", "qdm-qdr-v1": "QDM and QDR", "relative-bearing-v1": "Relative Bearing",
    "vor-radial-v1": "VOR Radials", "dme-slant-range-v1": "DME Slant Range",
    "ndb-night-effect-v1": "NDB Ground Wave and Night Effect",
    "compass-acceleration-v1": "Compass Errors (Southern Hemisphere)",
    "runway-wind-components-v1": "Runway Wind Components", "groundspeed-fuel-v1": "Groundspeed, Time and Fuel",
    "climb-descent-v1": "Climb and Descent Planning", "pressure-altitude-v1": "Pressure Altitude",
    "official-day-night-v1": "Official Day and Night", "longitude-time-v1": "Longitude and Time",
    "chart-scale-v1": "Chart Scale", "lambert-conic-v1": "Lambert Conformal Conic Chart",
    "great-circle-rhumb-v1": "Great Circles and Rhumb Lines", "latitude-longitude-v1": "Latitude and Longitude",
    "compass-points-v1": "Cardinal and Quadrantal Points", "measure-track-v1": "Measuring a Track on the Chart",
}

_IDS = {
    "variation-deviation-v1": [1550, 1593, 1594, 1595, 1596, 1597, 1598, 1599, 1600, 1601, 1602, 1611, 1629, 1686,
                               1702, 1705, 1706, 1722, 1760, 1764, 1768, 1793, 1801, 1810, 1811, 1821, 1829, 1831],
    "compass-acceleration-v1": [1604, 1606, 1615, 1616, 1620, 1622, 1623, 1624, 1626, 1631, 1632, 1834, 1923, 1928,
                                1931, 1938, 1941, 1947],
    "wind-drift-v1": [1633, 1634, 1637, 1638, 1639, 1642, 1643, 1644, 1647, 1648, 1649, 1652, 1653, 1654, 1656, 1657,
                      1659, 1662, 1666, 1695, 1709, 1716, 1720, 1820, 1827, 1828, 1830, 1839, 1843, 1848, 1849, 1851,
                      1852, 1853, 1862, 1864, 1866, 1868, 1869, 1870, 1871, 1872, 1873, 1877, 1880, 1887, 1890, 1898,
                      1899, 1900, 1903, 1904, 1906, 1908, 1909, 1910, 1911, 1912, 1694],
    "runway-wind-components-v1": [1670, 1671, 1676, 1685, 1687],
    "one-in-sixty-v1": [1672, 1678, 1711, 1769, 1786, 1794, 1799, 1807, 1823, 1825, 1832, 1913, 1916, 1926, 1930,
                        1933, 1935],
    "groundspeed-fuel-v1": [1663, 1667, 1673, 1675, 1679, 1682, 1689, 1696, 1715, 1717, 1728, 1761, 1815, 1822,
                            1879, 1883, 1895, 1902, 1907, 1922, 1937, 1939, 1942, 1943, 1944, 1946],
    "climb-descent-v1": [1664, 1677, 1688, 1819, 1824, 1826, 1842, 1881, 1886],
    "pressure-altitude-v1": [1645, 1646, 1651, 1658, 1660, 1661, 1767, 1837, 1917, 1936],
    "qdm-qdr-v1": [1731, 1734, 1736, 1740, 1743, 1751, 1753, 1850, 1854, 1855, 1860, 1865, 1878, 1893],
    "relative-bearing-v1": [1697, 1699, 1708, 1718, 1719, 1721, 1726, 1748, 1752, 1884, 1888, 1889, 1896],
    "vor-radial-v1": [1693, 1704, 1707, 1710, 1713, 1714, 1723, 1725, 1730, 1742, 1746, 1750, 1756, 1757, 1892,
                      1894],
    "dme-slant-range-v1": [1741, 1744, 1758],
    "ndb-night-effect-v1": [1733, 1735, 1738, 1747],
    "official-day-night-v1": [1603, 1605, 1607, 1610, 1612, 1613, 1618, 1619, 1621, 1625, 1627, 1630, 1772, 1773,
                              1789, 1802, 1817, 1919, 1921, 1934, 1945],
    "longitude-time-v1": [1558, 1559, 1560, 1700, 1701, 1703, 1712, 1779, 1787, 1788, 1790, 1797],
    "chart-scale-v1": [1669, 1680, 1683, 1690, 1759, 1771, 1798, 1803, 1806, 1914, 1915, 1918, 1920, 1924, 1925,
                       1929, 1940],
    "lambert-conic-v1": [1571, 1572, 1573, 1574, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583, 1584, 1585,
                         1586, 1587, 1588, 1589, 1590, 1766, 1778, 1791, 1792, 1808, 1863, 1875],
    "great-circle-rhumb-v1": [1563, 1564, 1567, 1568, 1684, 1692, 1770, 1774, 1777, 1782, 1783, 1796, 1809, 1818],
    "latitude-longitude-v1": [1561, 1562, 1565, 1566, 1569, 1570, 1668, 1674, 1765, 1776, 1780, 1781, 1795, 1813,
                              1814],
    "compass-points-v1": [1554, 1555, 1556, 1557, 1800, 1804],
    "measure-track-v1": [1698, 1724, 1727, 1816, 1856, 1857, 1858, 1859, 1861, 1867, 1874, 1876],
}
OTHER = {**{q: MET_DA for q in (1636, 1641, 1655, 1838, 1927, 1932)},
         **{q: TAS_FIG for q in (1665, 1681, 1833, 1844)}}
CARD_ONLY = [1543, 1544, 1545, 1546, 1547, 1548, 1549, 1551, 1552, 1553, 1609, 1614, 1617, 1729, 1732, 1737,
             1739, 1745, 1749, 1754, 1755]

PICTURE = {q: B2 + slug + ".webp" for slug, ids in _IDS.items() for q in ids}
PICTURE.update(OTHER)
PICTURE_TITLE = {q: TITLES[slug] for slug, ids in _IDS.items() for q in ids}
PICTURE_TITLE.update({q: "Density Altitude" for q in OTHER if OTHER[q] == MET_DA})
PICTURE_TITLE.update({q: "TAS Increases with Altitude" for q in OTHER if OTHER[q] == TAS_FIG})
assert not set(PICTURE) & set(CARD_ONLY)
assert len(PICTURE) == sum(len(v) for v in _IDS.values()) + len(OTHER)
