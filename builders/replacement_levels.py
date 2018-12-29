"""
Builds and applies replacement levels
"""


def player_eligible_at_pos(player, pos):
    """Determines if a player is eligible at a position
    """

    if player['above_repl'] is True:
        return False

    return pos in player['pos_all']


def calculate_replacement_levels(context: dict, pool_type: str):
    """Calculates replacement levels for each position
    """

    replacement_levels = {}

    player_pool = context[pool_type]['players']
    lg_positions = context['lineup']
    n_teams = context['teams']

    threshold = {
        'b': {
            'key': 'b_ab',
            'min': 400,
        },
        'p': {
            'key': 'p_ip',
            'min': 50,
        }
    }

    for player in player_pool:
        player['above_repl'] = False

    for pos in context[pool_type]['positions']:
        if lg_positions[pos] < 1:
            continue

        players_found = 0
        max_per = lg_positions[pos] * n_teams
        subpositions = []

        for player in player_pool:
            # pos_mv = player['pos_mv']
            # t_key = threshold[pool_type]['key']

            # if pos_mv == 'c' and player['components'][t_key] < 350:
            #     continue
            # elif pos_mv == 'rp' and player['components'][t_key] < 50:
            #     continue
            # elif pos_mv == 'sp' and player['components'][t_key] < 80:
            #     continue
            # elif pos_mv == 'p' and player['components'][t_key] < 50:
            #     continue
            # elif pos_mv == 'dh' and player['components'][t_key] < 150:
            #     print(player['name'], player['components'][t_key])
            #     continue

            if player_eligible_at_pos(player, pos):
                players_found += 1
                player['above_repl'] = True
                replacement_levels[pos] = player['z_value']
                subpositions.append(player['pos_mv'])

            if players_found == max_per:
                print(pos, players_found, player['name'], player['z_value'])

                # for subpos in subpositions:
                #     if pos != subpos:
                #         print(f'setting {subpos} repl to {pos}')
                #         replacement_levels[subpos] = replacement_levels[pos]

                break

    print('-')

    context['replacement_levels'] = replacement_levels
    return context


def apply_replacement_levels(context: dict, pool_type: str):
    """Sets replacement level for player based on most valuable position
    """

    player_pool = context[pool_type]['players']
    replacement_levels = context['replacement_levels']

    for player in player_pool:
        player['fvarz'] = (
            player['z_value'] - replacement_levels[player['pos_mv']])
        player['repl'] = replacement_levels[player['pos_mv']]
        player['above_repl'] = False

    return context
