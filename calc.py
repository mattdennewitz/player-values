"""
Percent Valuation
"""

import collections
import itertools
import functools
import json
import operator
import random
import statistics

from pprint import pprint

from pydash import pick, sorted_index_by

import builders
import const
from models import Config


def sort_positions(positions):
    sorted_positions = []
    for pos in positions:
        idx = sorted_index_by(sorted_positions, pos,
                              lambda pos: const.POS_PRIORITY[pos])
        sorted_positions.insert(idx, pos)
    return sorted_positions


def main():
    cfg_data = json.load(open('league_config.json'))
    cfg = Config().load(cfg_data)

    player_pool = json.load(open('player-pool.json'))
    random.shuffle(player_pool)

    # mark player's positional eligibility
    player_pool = builders.mark_positional_eligibility(
        player_pool, cfg['lg_pos'], cfg['eligibility'])

    context = {
        'b': {
            'players':
            list(filter(lambda p: p['player_type'] == 'b', player_pool)),
            'components':
            const.BATTING_COMPONENTS,
            'rates':
            const.BATTING_RATES,
            'scoring':
            cfg['batting_stats'],
            'n_draftable':
            cfg['draftable_b'],
            'positions':
            sort_positions(cfg['batting_pos']),
            'budget':
            cfg['batting_budget'],
            'split':
            cfg['split']['b'],
        },
        'p': {
            'players':
            list(filter(lambda p: p['player_type'] == 'p', player_pool)),
            'components':
            const.PITCHING_COMPONENTS,
            'rates':
            const.PITCHING_RATES,
            'scoring':
            cfg['pitching_stats'],
            'n_draftable':
            cfg['draftable_p'],
            'positions':
            sort_positions(cfg['pitching_pos']),
            'budget':
            cfg['pitching_budget'],
            'split':
            cfg['split']['p'],
        },
        'teams': cfg['teams'],
        'eligibility': cfg['eligibility'],
        'lineup': cfg['positions'],
        'budget': cfg['budget'],
        'total_draftable': cfg['total_draftable'],
    }

    results = {
        'batting': optimize(context, 'b'),
        'pitching': optimize(context, 'p'),
    }

    return results


def optimize(context: dict, pool_type: str):
    """Optimize a player pool

    Args:
        player_pool (list[dict]): Players to evaluate
        pool_type (str (b|p)): (b)atting or (p)itching?
    """

    outcomes = []  # how we watch for convergence
    completed = False

    print(f'Optimizing {pool_type}')

    while not completed:
        # for _ in range(20):
        # calculate league averages for all stats
        # for draftable pool of players
        context = builders.calculate_league_rates(context, pool_type)

        # set over-average scores for all players
        context = builders.apply_oa_values(context, pool_type)

        # apply z-scores for components and rates
        context = builders.apply_z_scores(context, pool_type)

        # sort by z-value
        context[pool_type]['players'] = sorted(
            context[pool_type]['players'],
            key=operator.itemgetter('z_value'),
            reverse=True)

        # calculate replacement levels for each position
        context = builders.calculate_replacement_levels(context, pool_type)

        # calculate player value above replacement, re-sort
        context = builders.apply_replacement_levels(context, pool_type)
        context[pool_type]['players'] = sorted(
            context[pool_type]['players'],
            key=operator.itemgetter('fvarz'),
            reverse=True)

        # add dollar values, re-sort
        context = builders.apply_dollar_values(context, pool_type)
        context[pool_type]['players'] = sorted(
            context[pool_type]['players'],
            key=operator.itemgetter('dollars'),
            reverse=True)

        # check for convergence
        for prior in outcomes:
            if prior == context['rates']['devs']:
                print(context[pool_type]['players'][0].keys())

                output = [
                    pick(player, 'name', 'pos_mv', 'pos_eligible', 'dollars',
                         'z_value', 'fvarz')
                    for player in context[pool_type]['players']
                ]

                print('repls')
                pprint(context['replacement_levels'])
                print('- averages')
                pprint(context['rates']['avgs'])

                json.dump(output, open(f'final-{pool_type}.json', 'w'))
                completed = True  # done

        outcomes.append(context['rates']['devs'])


if __name__ == '__main__':
    main()
