# 改善案のルールに従って記述

from genetest import players, teams
from tradee_value_calculation import tradee_value_dict



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
        print(cycles)
        
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
        for team in list(tentative_picks.keys()):
            if team in preferred_dict and preferred_dict[team]:
                tentative_picks[team] = preferred_dict[team][0]
            else:
                tentative_picks.pop(team, None)
    
    return players





# 関数を呼び出して結果を取得
updated_players = draft_players(tradee_value_dict, players)

# players 辞書をキーごとに改行して出力
for team, players_list in updated_players.items():
    print(f"Team: {team} ({len(players_list)} players)")
    for player_id, player_info in players_list.items():
        print(f"    {player_id}: {player_info}")

