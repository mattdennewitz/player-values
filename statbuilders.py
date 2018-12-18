"""Rate stat builders
"""


def build_tb(b_1b, b_2b, b_3b, b_hr):
    """Total bases"""

    return b_1b + (2.0 * b_2b) + (3.0 * b_3b) + (4.0 * b_hr)


def build_avg(b_h, b_ab):
    """Batting average"""

    if b_ab == 0:
        return 0.

    value = b_h / b_ab
    return round(value, 3)


def build_obp(b_h, b_bb, b_hbp, b_sf, b_ab):
    """On-base percentage"""

    if not b_ab:
        return 0.

    value = (b_h + b_bb + b_hbp) / (b_ab + b_bb + b_hbp + b_sf)
    return round(value, 3)


def build_slg(b_1b, b_2b, b_3b, b_hr, b_ab):
    """Slugging percentage"""

    if not b_ab:
        return 0.

    value = build_tb(b_1b, b_2b, b_3b, b_hr) / b_ab
    return round(value, 3)


def build_era(p_ip, p_er):
    """Earned run average"""

    if not p_ip:
        return 0.

    value = (p_er / p_ip) * 9.
    return round(value, 3)


def build_whip(p_ip, p_bb, p_h):
    """Walks + Hits / IP"""

    if not p_ip:
        return 0.

    value = (p_bb + p_h) / p_ip
    return round(value, 3)
