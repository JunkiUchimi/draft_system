# 改善案のルールに従って記述

from genetest import players, teams, tradee
from tradee_value_calculation import tradee_value_dict

def generate_preferred_dict(tradee_value_dict):
    preferred_dict = {}
    for key in teams:  # チーム 'a' から 'l' まで処理
        if key in tradee_value_dict:
            inner_keys = list(tradee_value_dict[key].keys())
            preferred_dict[key] = inner_keys
    return preferred_dict

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
                current_team = get_team_of_player(tentative_picks[current_team], tentative_picks)
                if current_team in cycle:
                    cycle_start = cycle.index(current_team)
                    cycles.append(cycle[cycle_start:])
                    break
    return cycles

def get_team_of_player(player_id, tentative_picks):
    for team, pick in tentative_picks.items():
        if pick == player_id:
            return team
    return None

def remove_player_from_preferred_dict(preferred_dict, player_id):
    for team, preferred in preferred_dict.items():
        if player_id in preferred:
            preferred.remove(player_id)

def draft_players(tradee_value_dict, players):
    preferred_dict = generate_preferred_dict(tradee_value_dict)
    while True:
        tentative_picks = {}
        for team, preferred in preferred_dict.items():
            if preferred:
                tentative_picks[team] = preferred[0]
        
        cycles = find_cycles(tentative_picks)
        
        if not cycles:
            break
        
        for cycle in cycles:
            for team in cycle:
                player_id = tentative_picks[team]
                if team in tradee_value_dict and player_id in tradee_value_dict[team]:
                    player_info = tradee_value_dict[team][player_id][:2]
                    players[team][player_id] = player_info
                remove_player_from_preferred_dict(preferred_dict, player_id)

        # 仮指名をリセットして次のサイクルのチェック
        for team in tentative_picks.keys():
            if team in preferred_dict and preferred_dict[team]:
                tentative_picks[team] = preferred_dict[team][0]
            else:
                tentative_picks.pop(team, None)
    
    return players

# 使用例
tradee_value_dict = {
    'a': {'p_b1': [11.5, '捕手'], 'p_c1': [11.7, '投手']},
    'b': {'p_c1': [11.7, '投手'], 'p_a1': [11.5, '捕手']},
    'c': {'p_a1': [11.7, '外野手'], 'p_b1': [11.1, '外野手']}
}

players = {team: {} for team in 'abc'}

# 関数を呼び出して結果を取得
updated_players = draft_players(tradee_value_dict, players)

# players 辞書をキーごとに改行して出力
for team, players_list in updated_players.items():
    print(f"Team: {team} ({len(players_list)} players)")
    for player_id, player_info in players_list.items():
        print(f"    {player_id}: {player_info}")

