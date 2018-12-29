"""
Calculates and applies over-average values for given players
"""

import const


def apply_oa_values(context: dict, pool_type: str):
    """OA value application
    """

    rate_stats = context[pool_type]['rates']
    player_pool = context[pool_type]['players']
    avgs = context['rates']['avgs']

    for player in player_pool:
        rate_weight = (
            player['components']['b_ab']  # determine weight for rate stats
            if pool_type == 'b' else player['components']['p_ip'])

        for stat in rate_stats:
            oa_key = f'{stat}_oa'

            if oa_key in player['components']:
                continue  # ignore above repl players

            # calculate over-average numbers for rate stats
            if stat in const.BAD_STATS:
                value = avgs[stat] - player['components'][stat]
            else:
                value = player['components'][stat] - avgs[stat]
            value *= rate_weight  # weighted over-average value
            player['components'][oa_key] = value

    return context
