import collections

TEAMS = 12  # teams per league
TEAM_BUDGET = 260.0
LEAGUE_BUDGET = TEAM_BUDGET * TEAMS  # 3120
LEAGUE_BATTING_BUDGET = LEAGUE_BUDGET * .7  # 2090.4
LEAGUE_PITCHING_BUDGET = LEAGUE_BUDGET * .3  # 1029.6

# stats that count *against* a player
BAD_STATS = frozenset([  # lower == better
    'b_so',
    'b_cs',
    'p_era',
    'p_whip',
    'p_hra',
])

# all recognized batting components
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

# all recognized batting rate stats
BATTING_RATES = frozenset([
    'b_avg',
    'b_obp',
    'b_slg',
])

# all recognized pitching components
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

# all recognized pitching rate stats
PITCHING_RATES = frozenset([
    'p_era',
    'p_whip',
])

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

POS_CORE = ('c', 'ss', 'b2', 'b3', 'b1', 'sp', 'rp')
POS_OF = ('cf', 'lf', 'rf', 'of')
POS_FLEX = ('mi', 'ci', 'if_', 'p', 'dh')
POS_P = ('sp', 'rp', 'p')
