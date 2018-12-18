import collections

TEAMS = 12  # teams per league
TEAM_BUDGET = 260.0
LEAGUE_BUDGET = TEAM_BUDGET * TEAMS  # 3120
LEAGUE_BATTING_BUDGET = LEAGUE_BUDGET * .7  # 2090.4
LEAGUE_PITCHING_BUDGET = LEAGUE_BUDGET * .3  # 1029.6

BAD_STATS = frozenset([  # lower == better
    'b_so',
    'p_era',
    'p_whip',
    'p_hra',
])

BATTING_COMPONENTS = frozenset([
    'b_pa',
    'b_ab',
    'b_r',
    'b_rbi',
    'b_hr',
    'b_bb',
    'b_so',
    'b_hbp',
    'b_sf',
    'b_sh',
    'b_sb',
    'b_cs',
    'b_g',
    'b_h',
    'b_1b',
    'b_2b',
    'b_3b',
])

BATTING_RATES = frozenset([
    'b_avg',
    'b_obp',
    'b_slg',
])

PITCHING_COMPONENTS = frozenset([
    'p_ip',
    'p_g',
    'p_gs',
    'p_w',
    'p_l',
    'p_qs',
    'p_sv',
    'p_bs',
    'p_hld',
    'p_so',
    'p_h',
    'p_bb',
    'p_ibb',
    'p_er',
    'p_hbp',
    'p_cg',
    'p_sho',
    'p_tbf',
    'p_ra',
    'p_r',
    'p_wp',
    'p_bk',
    'p_hra',
])

PITCHING_RATES = frozenset([
    'p_era',
    'p_whip',
])

BATTING_STATS = frozenset([
    'b_avg',
    'b_obp',
    'b_slg',
    'b_hr',
    'b_rbi',
    'b_so',
    'b_r',
    'b_sb',
])

PITCHING_STATS = frozenset([
    'p_era',
    'p_whip',
    'p_so',
    'p_w',
    'p_qs',
    'p_sv',
    'p_hld',
    'p_hra',
])

# positions used by a certain league
POSITIONS = {
    'c': 1,
    'b1': 1,
    'b2': 1,
    'ss': 1,
    'b3': 1,
    'lf': 0,
    'cf': 0,
    'rf': 0,
    'of': 3,
    'dh': 1,
    'sp': 5,
    'rp': 5,
    'mi': 0,
    'ci': 0,
    'if_': 0,
    'p': 0,
}

# a league's positional eligibility requirements
POS_ELIGIBILITY = {
    'c': 10,
    'b1': 10,
    'b2': 10,
    'ss': 10,
    'b3': 10,
    'lf': 10,
    'cf': 10,
    'rf': 10,
    'of': 10,
    'mi': 10,
    'ci': 10,
    'if_': 10,
    'sp': 5,
    'rp': 5,
    'p': 0,
    'dh': 0,
}

# league players per batting position
BATTING_POS = collections.OrderedDict((
    ('c', 1 * TEAMS),
    ('ss', 1 * TEAMS),
    ('b2', 1 * TEAMS),
    ('b3', 1 * TEAMS),
    ('cf', 0 * TEAMS),
    ('lf', 0 * TEAMS),
    ('rf', 0 * TEAMS),
    ('of', 3 * TEAMS),
    ('b1', 1 * TEAMS),
    ('mi', 0 * TEAMS),
    ('ci', 0 * TEAMS),
    ('if_', 0 * TEAMS),
    ('dh', 1 * TEAMS),
))

# league players per pitching position
PITCHING_POS = collections.OrderedDict((
    ('sp', 5 * TEAMS),
    ('rp', 6 * TEAMS),
    ('P', 0 * TEAMS),
))

# position scarcity
POS_PRIORITY = {
    # core positions
    'c': 1,
    'ss': 2,
    'b2': 3,
    'b3': 4,
    'cf': 4,
    'lf': 5,
    'rf': 6,
    'of': 7,
    'b1': 8,
    'sp': 9,
    'rp': 10,

    # flex spots
    'mi': 11,
    'ci': 12,
    'if_': 13,
    'dh': 14,
    'p': 15,
}

DRAFTABLE_PLAYERS = sum(BATTING_POS.values()) + sum(
    PITCHING_POS.values())  # total number of players drafted

PLAYERS_PER_TEAM = DRAFTABLE_PLAYERS / TEAMS
