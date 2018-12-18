"""
z-score buildout and application
"""

import const


def apply_z_scores(player_pool, lg_avgs, lg_devs, lg_rates):
    """Applies z-scores for each category
    """

    for player in player_pool:
        components = (const.BATTING_COMPONENTS if player['player_type'] == 'b'
                      else const.PITCHING_COMPONENTS)
        rates = (const.BATTING_RATES
                 if player['player_type'] == 'b' else const.PITCHING_RATES)

        # set *component* z-scores
        for component in components:
            if lg_devs[component] == 0:
                continue

            weight = 1.0 if component not in const.BAD_STATS else -1.0
            player['z_' + component] = (
                (player['components'][component] - lg_avgs[component]) /
                lg_devs[component]) * weight

        # determine weight for rate stats
        rate_weight = (player['components']['b_ab']
                       if player['player_type'] == 'b' else
                       player['components']['p_ip'])

        # set rate z-scores
        for rate in rates:
            key = 'z_' + rate

            if rate in const.BAD_STATS:
                value = lg_rates[rate] - player['components'][rate]
            else:
                value = player['components'][rate] - lg_rates[rate]

            player[key] = value * rate_weight

        lg_components = (const.BATTING_STATS if player['player_type'] == 'b'
                         else const.PITCHING_STATS)
        lg_keys = ['z_' + c for c in lg_components]
        player['z_value'] = sum([player[key] for key in lg_keys])

    return player_pool
