"""
z-score buildout and application
"""

from pydash import pick

import const


def apply_z_scores(context, pool_type):
    """Applies z-scores for each category
    """

    lg_devs = context['rates']['devs']
    lg_avgs = context['rates']['avgs']
    rates = context[pool_type]['rates']
    player_pool = context[pool_type]['players']
    scoring_components = context[pool_type]['scoring']

    # create z-scores only for scoring components
    for player in player_pool:
        player['z_value'] = 0.

        for component in scoring_components:
            component_key = component if component not in rates else f'{component}_oa'

            if lg_devs[component_key] == 0.:
                continue

            value = (
                (player['components'][component_key] - lg_avgs[component_key])
                / lg_devs[component_key])
            player['z_' + component_key] = value  # mark component z-score
            player['z_value'] += value  # add to total z-value

    return context
