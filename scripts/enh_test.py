# 改善案のルールに従って記述

import tradee_value_calculation, genetest, copy, pprint, json
from genetest import players, teams, adeq_list, calculate_position_adequacy, adeq_list_before
from tradee_value_calculation import tradee_value_dict
tradee_value_dict = tradee_value_calculation.tradee_value_dict

destination = {chr(i): {} for i in range(ord('a'), ord('m'))}
adeq_list_after = {}   # 各球団のポジション充実度を格納する辞書
tradee_temp = {chr(i): {} for i in range(ord('a'), ord('m'))}

# tradee_value_dictには各球団の、候補選手に対する評価順に並んだ配列が格納されており、そこから一番最初の選手のIDを取得する関数
def generate_preferred_dict(tradee_value_dict):
    preferred_dict = {}
    for key in teams:  # チーム 'a' から 'l' まで処理
        if key in tradee_value_dict:
            inner_keys = list(tradee_value_dict[key].keys())
            preferred_dict[key] = inner_keys
    return preferred_dict

# ITTCを用いてサイクルを見つける関数
def find_cycles(tentative_picks):
    cycles = []
    visited = set()
    for team in tentative_picks.keys():
        if team not in visited:
            cycle = []
            current_team = team
            while current_team not in visited and current_team in tentative_picks:
                visited.add(current_team)
                cycle.append(current_team)
                current_team = get_team_of_player(tentative_picks[current_team])
                
                if current_team in cycle:
                    cycle_start = cycle.index(current_team)
                    cycles.append(cycle[cycle_start:])
                    break
    return cycles

# 指名した選手の所属球団を返す関数
def get_team_of_player(player_id):
    # player_idを'_'で区切って後ろの部分を取得
    part_after_underscore = player_id.split('_')[-1]
    # 後ろの部分の1文字目を取得
    team = part_after_underscore[0]
    return team

# 獲得された選手を各球団のpreferred_dict配列から取り除く関数
def remove_player_from_preferred_dict(preferred_dict, player_id):
    for team, preferred in preferred_dict.items():   #.items()で辞書型を('b', ['p_c1', 'p_a1']),のようにする
        if player_id in preferred:
            preferred.remove(player_id)

# できたサイクルを元に実際に選手の移籍を行う関数
def draft_players(tradee_value_dict, players):
    preferred_dict = generate_preferred_dict(tradee_value_dict)
    while True:
        tentative_picks = {}
        for team, preferred in preferred_dict.items():
            if preferred:
                tentative_picks[team] = preferred[0]   #現在の球団の最も好みの選手の選手ID
        # print(tentative_picks)
        
        cycles = find_cycles(tentative_picks)
        # print(cycles)
        
        if not cycles:
            break
        
        for cycle in cycles:
            for team in cycle:
                player_id = tentative_picks[team]
                if team in tradee_value_dict and player_id in tradee_value_dict[team]:
                    player_info = tradee_value_dict[team][player_id][:2]
                    tradee_temp[team][player_id] = player_info
                remove_player_from_preferred_dict(preferred_dict, player_id)

        # 仮指名をリセットして次のサイクルのチェック
        for team in list(tentative_picks.keys()):
            if team in preferred_dict and preferred_dict[team]:
                tentative_picks[team] = preferred_dict[team][0]
            else:
                tentative_picks.pop(team, None)
    
    return players


position_order = {
    '捕手': 1,
    '内野手': 2,
    '外野手': 3,
    '投手': 4
}

# ここから新たなルールを追加
# 関数を呼び出して結果を取得
updated_players = draft_players(tradee_value_dict, players)
tradee_value_dict = {}
team_tradee_values = {chr(i): {} for i in range(ord('a'), ord('m'))}
for team in teams:
    
    total_before = 0
    for position in adeq_list[team].keys():
        total_before += adeq_list_before[team][position]
    for cal_team, infos in tradee_temp.items():
        # position = player_info[1]  # 選手のポジションを取得
        # 各選手のplayer_idとその情報をループで回す
        for player_id, player_info in infos.items():
            # players[team] に player_id をキーとして追加
            players[team][player_id] = player_info

        sorted_players = dict(sorted(players[team].items(), key=lambda item: (position_order[item[1][1]], -item[1][0])))
        for player_id, player_info in infos.items():
            del players[team][player_id]
        
        adeq_list = {}   # 各球団のポジション充実度を格納する辞書
        adeq_list = calculate_position_adequacy(team, sorted_players)
        total = 0
        for posi in adeq_list[team].keys():
            total += adeq_list[team][posi]
        value = total - total_before

        # 選手IDをキーとしてリストを辞書に追加
        team_tradee_values[team][cal_team] = value
    # 計算した値で降順にソート

    # 内側の辞書を数値の降順でソートする
tradee_value_pair_dict = {
    team: dict(sorted(values.items(), key=lambda item: item[1], reverse=True))
    for team, values in team_tradee_values.items()
}
for team, players_to_remove in tradee_value_pair_dict.items():
    for player_key in players_to_remove:
        if player_key in players[team]:
            del players[team][player_key]
# tradee_value_pair_dict = {'a': {'c': 2.625, 'i': 0.7614583333333371, 'g': 0.40625, 'a': 0.125, 'h': 0.08125000000001137, 'b': -0.078125, 'l': -0.2291666666666572, 'k': -1.84375, 'j': -2.3999999999999773, 'd': -2.619791666666657, 'e': -2.6531249999999886, 'f': -2.7750000000000057}, 'b': {'c': 12.418749999999989, 'g': 6.696874999999977, 'b': 5.712499999999977, 'h': 4.712499999999977, 'i': 0.5729166666666288, 'a': 0.078125, 'l': -0.05208333333337123, 'k': -0.7489583333333485, 'e': -0.7750000000000341, 'j': -1.1437500000000114, 'f': -1.196875000000034, 'd': -1.25}, 'c': {'c': 1.424999999999983, 'h': -0.06874999999999432, 'g': -0.4906249999999943, 'b': -1.125, 'i': -3.731250000000017, 'j': -3.950000000000017, 'l': -4.200000000000017, 'e': -4.40625, 'a': -4.426041666666691, 'f': -4.715625000000017, 'k': -4.853125000000006, 'd': -5.337500000000006}, 'd': {'c': 8.64270833333336, 'g': 5.567708333333343, 'h': 5.3552083333333655, 'i': 4.831250000000011, 'l': 4.578125, 'b': 4.508333333333354, 'a': 3.9447916666666742, 'j': 1.3239583333333371, 'k': 0.9510416666666401, 'd': 0.0, 'f': -0.038541666666645824, 'e': -0.28229166666667993}, 'e': {'c': 9.587499999999977, 'g': 6.559375000000017, 'h': 5.725000000000023, 'b': 5.525000000000006, 'i': 2.3020833333333144, 'l': 1.8604166666667084, 'a': 1.440624999999983, 'j': 0.8562499999999886, 'k': 0.31354166666667993, 'e': 0.04374999999998863, 'f': 0.015625, 'd': -0.2874999999999943}, 'f': {'c': 6.59375, 'i': 4.259375000000034, 'l': 3.7687500000000114, 'g': 3.6875, 'a': 3.42291666666668, 'b': 2.6781249999999943, 'h': 2.5875000000000057, 'j': 1.081249999999983, 'k': 0.7125000000000057, 'f': 0.0, 'd': -0.1885416666666515, 'e': -0.2718749999999943}, 'g': {'c': 1.1781250000000227, 'h': 0.6468750000000227, 'g': 0.0, 'i': -0.053124999999965894, 'b': -0.484375, 'a': -0.689583333333303, 'l': -0.7218750000000114, 'j': -1.8781249999999545, 'k': -2.433333333333337, 'f': -2.6875, 'e': -2.8093749999999886, 'd': -2.8843749999999773}, 'h': {'c': 2.575000000000017, 'i': 0.27916666666666856, 'g': 0.21562499999998863, 'h': 0.0, 'b': -0.3687500000000057, 'a': -0.5072916666666742, 'l': -0.6020833333333258, 'k': -2.0677083333333144, 'j': -2.143749999999983, 'e': -2.706249999999983, 'f': -2.8656249999999943, 'd': -2.9187499999999886}, 'i': {'c': 2.0125000000000455, 'i': 0.32916666666670835, 'h': 0.2812500000000284, 'g': 0.078125, 'a': -0.30729166666662877, 'l': -0.38333333333329733, 'b': -0.40625, 'j': -2.349999999999966, 'k': -2.609374999999943, 'f': -3.146874999999966, 'e': -3.2968749999999716, 'd': -3.3854166666666288}, 'j': {'c': 5.701041666666669, 'i': 3.1937499999999943, 'g': 2.8885416666666686, 'l': 2.7906250000000057, 'h': 2.75104166666668, 'a': 2.557291666666657, 'b': 1.9041666666666686, 'j': 0.6572916666666799, 'k': -0.078125, 'f': -0.5677083333333428, 'e': -0.6395833333333201, 'd': -0.7291666666666572}, 'k': {'c': 6.278125000000017, 'i': 3.796875, 'g': 3.525000000000034, 'l': 3.44062500000004, 'a': 3.160416666666663, 'h': 2.78437500000004, 'b': 2.559375000000017, 'k': 0.591666666666697, 'j': 0.4531250000000284, 'd': -0.16562499999997726, 'f': -0.703125, 'e': -1.0781249999999716}, 'l': {'i': 0.7562499999999943, 'c': 0.3395833333333371, 'a': 0.11979166666665719, 'l': 0.0, 'g': -0.6697916666666686, 'h': -1.0229166666666742, 'j': -1.1791666666666742, 'k': -1.5156249999999716, 'b': -1.5541666666666458, 'f': -1.7010416666666686, 'e': -1.7541666666666345, 'd': -2.041666666666657}}
# print(tradee_temp)
# print(tradee_value_pair_dict)
# 最初のキーを取得して新しい辞書を作成
tradee_pair_temp = {chr(i): {} for i in range(ord('a'), ord('m'))}
def generate_first_key_team(tradee_value_pair_dict):
    first_keys_team = {}
    for outer_key, inner_dict in tradee_value_pair_dict.items():
        if inner_dict:  # inner_dictが空でない場合のみ処理を行う
            first_keys_team[outer_key] = list(inner_dict.keys())[0]
    return first_keys_team

def remove_player_from_first_keys_team(tradee_value_pair_dict, selected_team):
    for base_team, preferred in tradee_value_pair_dict.items():
        if selected_team in preferred:
            preferred.pop(selected_team)
    return
# print()

# print(first_keys_team)
# first_keys_team = {'a': 'b', 'b': 'c', 'c': 'g', 'd': 'j', 'e': 'j', 'f': 'j', 'g': 'a', 'h': 'j', 'i': 'j', 'j': 'j', 'k': 'c', 'l': 'j'}
def find_pair_cycles(first_keys_team):
    pair_cycles = []
    visited = set()
    for team in teams:
        if team not in visited:
            cycle = []
            current_team = team
            while current_team not in visited and current_team in first_keys_team:
                visited.add(current_team)
                cycle.append(current_team)
                current_team = first_keys_team[current_team]
                
                if current_team in cycle:
                    cycle_start = cycle.index(current_team)
                    pair_cycles.append(cycle[cycle_start:])
                    break
    return pair_cycles

# print(tradee_value_pair_dict)
def draft_pair_players(tradee_value_pair_dict, players):
    first_keys_team = generate_first_key_team(tradee_value_pair_dict)
    
    while True:
        pair_cycles = find_pair_cycles(first_keys_team)
        
        if not pair_cycles:
            break
        
        for cycle in pair_cycles:
            for team in cycle:
                # サイクルに含まれるチームの選手をplayersに追加
                if team in tradee_value_pair_dict:
                    # 選手を追加
                    for player_id, player_info in tradee_temp[team].items():
                        players[team][player_id] = player_info
                
                # 次のチームに対する処理
                next_team = first_keys_team[team]
                if team in tradee_value_pair_dict and next_team in tradee_value_pair_dict[team]:
                    team_info = tradee_value_pair_dict[team][next_team]
                    tradee_temp[team][next_team] = team_info

                remove_player_from_first_keys_team(tradee_value_pair_dict, next_team)

        # サイクルを処理した後、再度first_keys_teamを更新
        first_keys_team = generate_first_key_team(tradee_value_pair_dict)
    
    return players

draft_pair_players(tradee_value_pair_dict, players)
# print('aaaaaaaaa')
# print(players)
for prefix in teams:
    players[prefix] = dict(sorted(players[prefix].items(), key=lambda item: (position_order[item[1][1]], -item[1][0])))
    team_name = prefix  # チーム名を取得
    sorted_players = players[team_name]

    adeq_list_after = calculate_position_adequacy(team_name, sorted_players)


# adeq_list_difを計算
adeq_list_dif = {}
adeq_list_dif_sum = {}
for team in teams:
    adeq_list_dif[team] = {}
    for position in adeq_list[team]:
        adeq_list_dif[team][position] = adeq_list_after[team][position] - adeq_list_before[team][position]
    total = sum(adeq_list_dif[team].values())
    adeq_list_dif[team]['合計'] = total


adeq_list_dif['合計'] = {'捕手': 0, '内野手': 0, '外野手': 0, '投手': 0, '合計': 0}
# 各ポジションの数値の合計値を計算して格納
for player in adeq_list_dif.values():
    if player is not adeq_list_dif['合計']:  # '合計' キーのエントリを無視
        for position in ['捕手', '内野手', '外野手', '投手', '合計']:
            adeq_list_dif['合計'][position] += player[position]


json_data = json.dumps(adeq_list_dif, ensure_ascii=False)

# print(json_data)

print(adeq_list_dif['合計']['合計'])