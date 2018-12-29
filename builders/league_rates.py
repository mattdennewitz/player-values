"""
Calculates league rates for all components
"""

import collections
import statistics

import const
import statbuilders


def calculate_league_rates(context, pool_type):
    """Calculates league averages, deviations, and expected rates
    """

    stats = collections.defaultdict(list)  # collect stats for avgs, devs
    totals = collections.Counter()  # for summation
    avgs = {}
    devs = {}

    components = context[pool_type]['components']
    rate_stats = context[pool_type]['rates']

    # player pool is limited to only drafted players
    player_pool = context[pool_type]['players']
    player_pool = player_pool[:context[pool_type]['n_draftable']]

    for player in player_pool:
        for stat in components:
            value = player['components'][stat]
            stats[stat].append(value)
            totals[stat] += value

    for stat in stats:
        avgs[stat] = statistics.mean(stats[stat])
        devs[stat] = statistics.stdev(stats[stat])

    avgs.update({
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
    })

    # iterate again through player pool to calculate "over-average" stats
    # for all rate stat categories (era, whip, avg, ...)
    for player in player_pool:
        rate_weight = (
            player['components']['b_ab']  # determine weight for rate stats
            if pool_type == 'b' else player['components']['p_ip'])

        for stat in rate_stats:
            # calculate over-average numbers for rate stats
            oa_key = f'{stat}_oa'
            if stat in const.BAD_STATS:
                value = avgs[stat] - player['components'][stat]
            else:
                value = player['components'][stat] - avgs[stat]
            value *= rate_weight  # weighted over-average value
            stats[oa_key].append(value)
            player['components'][oa_key] = value

    for stat in rate_stats:
        oa_key = f'{stat}_oa'
        avgs[oa_key] = statistics.mean(stats[oa_key])
        devs[oa_key] = statistics.stdev(stats[oa_key])

    context['rates'] = {
        'avgs': avgs,
        'devs': devs,
        'totals': totals,
    }

    return context
