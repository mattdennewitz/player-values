"""
Calculates league rates for all components
"""

import collections
import statistics

import const
import statbuilders


def calculate_league_rates(player_pool, batting_stats, pitching_stats):
    """Calculates league averages, deviations, and expected rates
    """

    stats = collections.defaultdict(list)  # collect stats for avgs, devs
    totals = collections.Counter()  # for summation
    avgs = {}
    devs = {}

    for player in player_pool:
        components = (const.BATTING_COMPONENTS if player['player_type'] == 'b'
                      else const.PITCHING_COMPONENTS)

        for stat in components:
            value = player['components'][stat]
            stats[stat].append(value)
            totals[stat] += value

    for stat in stats:
        avgs[stat] = statistics.mean(stats[stat])
        devs[stat] = statistics.stdev(stats[stat])

    rates = {
        'b_avg':
        statbuilders.build_avg(totals['b_h'], totals['b_ab']),
        'b_obp':
        statbuilders.build_obp(totals['b_h'], totals['b_bb'], totals['b_hbp'],
                               totals['b_sf'], totals['b_ab']),
        'b_slg':
        statbuilders.build_slg(totals['b_1b'], totals['b_2b'], totals['b_3b'],
                               totals['b_hr'], totals['b_ab']),
        'b_tb':
        statbuilders.build_tb(totals['b_1b'], totals['b_2b'], totals['b_3b'],
                              totals['b_hr']),
        'p_era':
        statbuilders.build_era(totals['p_ip'], totals['p_er']),
        'p_whip':
        statbuilders.build_whip(totals['p_ip'], totals['p_bb'], totals['p_h']),
    }

    return (avgs, devs, rates)
