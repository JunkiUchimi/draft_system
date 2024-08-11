# 現役ドラフト制度を実行するファイル
from genetest import calculate_position_adequacy, teams, players, tradee, adeq_list, adeq_list_before
from tradee_value_calculation import position_order, tradee_value_dict
import copy, pprint, json


# for key, positions in adeq_list_before.items():
#     print(f"Team {key}:")
#     for position, value in positions.items():
#         print(f"  {position}: {value}")

adeq_list_after = {}   # 各球団のポジション充実度を格納する辞書


# 各球団の票を記録する辞書
votes = {team: 0 for team in teams}


# 各チームの tradee_value_dict を処理する
for team, player_values in tradee_value_dict.items():
    player_ids = list(player_values.keys())
    for idx, player_id in enumerate(player_ids[:3]):  # 最初の3選手のみ確認
        # 選手IDの 'P_' の次の文字を取得
        player_team = player_id.split('_')[1][0]
        if player_team != team:  # 自分の球団以外の場合
            if player_team in votes:
                votes[player_team] += 1
            break

# 投票数が最も多い球団を決定
top_team = max(votes, key=votes.get)

# トップの球団から選手を獲得する関数
def acquire_players(team, target_team=None):
    # 最も好みの選手リストを取得
    if target_team:
        top_players_list = [player_id for player_id in tradee_value_dict[team] if player_id.split('_')[1][0] == target_team]
    else:
        top_players_list = tradee_value_dict[team]

    for player_id in top_players_list:
        # 最も好みの選手を取得
        top_player = player_id

        # 選手IDのプレフィックスから球団名を取得
        player_team = top_player.split('_')[1][0]

        # 選手が自球団の選手でない場合は獲得
        if player_team != team:
            # 選手がまだ tradee に存在するか確認
            if top_player in tradee:
                # 選手情報を自球団の選手リストに追加
                if team not in players:
                    players[team] = {}
                players[team][top_player] = tradee[top_player]
                # 獲得した選手を出力
                # print(f"球団 {team} が選手 {top_player} を獲得しました。")
                # 獲得した選手を tradee から削除
                del tradee[top_player]
                # 獲得された選手が所属していた球団の他の選手も tradee から削除
                for other_player in list(tradee.keys()):
                    if other_player.split('_')[1][0] == player_team:
                        if player_team not in players:
                            players[player_team] = {}
                        players[player_team][other_player] = tradee[other_player]
                        del tradee[other_player]
                players[team] = dict(sorted(players[team].items(), key=lambda item: (position_order[item[1][1]], -item[1][0])))
                return player_team  # 獲得した選手の元の球団を返す

    return None  # 獲得できる選手がいない場合

# 獲得した球団を記録するセット
acquired_teams = set()

# トップの球団から選手を獲得
current_team = top_team

# 結果を表示
# print("各球団の票数:")
# for team, count in votes.items():
#     print(f"球団{team}: {count}票")

# print(tradee)

last_acquired_team = None

while len(acquired_teams) < len(teams) - 2:
    if current_team not in acquired_teams:
        next_team = acquire_players(current_team)
        if next_team:
            last_acquired_team = current_team
            acquired_teams.add(current_team)
        current_team = next_team
    else:
        remaining_teams = {team: votes[team] for team in teams if team not in acquired_teams}
        if remaining_teams:
            current_team = max(remaining_teams, key=remaining_teams.get)
        else:
            break

# remaining_teamsをvotesの票数順にソート
remaining_teams = sorted([team for team in teams if team not in acquired_teams], key=lambda team: votes[team])

# 10球団目が獲得した選手の所属球団Xを取得
if last_acquired_team:
    last_acquired_player_team = None
    for player_id in tradee_value_dict[last_acquired_team]:
        player_team = player_id.split('_')[1][0]
        if player_id in players[last_acquired_team]:
            last_acquired_player_team = player_team
            break

# 11球団目の獲得処理
if len(remaining_teams) == 2:
    if last_acquired_player_team and last_acquired_player_team not in acquired_teams:
        eleventh_team = last_acquired_player_team
    else:
        eleventh_team = remaining_teams[0]  # 票数が最も少ない球団を11球団目として選択
    remaining_teams.remove(eleventh_team)  # eleventh_teamをremaining_teamsから削除
    last_team = remaining_teams[0]  # 票数が2番目に少ない球団を12球団目として選択
    # print(f"球団 {eleventh_team} がまだ獲得していない球団 {last_team} の選手を獲得します。")
    acquire_players(eleventh_team, target_team=last_team)
 

# 最後に残った球団が他の球団から選手を獲得する
if len(remaining_teams) == 1:
    last_team = remaining_teams[0]
    # print(f"球団 {last_team} が最後に残った球団から選手を獲得します。")
    acquire_players(last_team)


for prefix in teams:
    team_name = prefix  # チーム名を取得
    sorted_players = players[team_name]
    adeq_list_after = calculate_position_adequacy(team_name, sorted_players)

# 獲得後の結果を表示

    # print(f"\n球団 {team} の選手リスト:")
    # for player_id, player_info in players[team].items():
    #     print(f"選手ID: {player_id}, 選手情報: {player_info}")
        
# for key, positions in adeq_list_before.items():
#     print(f"Team {key}:")
#     for position, value in positions.items():
#         print(f"  {position}: {value}")

# for key, positions in adeq_list_after.items():
#     print(f"Team {key}:")
#     for position, value in positions.items():
#         print(f"  {position}: {value}")

# adeq_list_difを計算
adeq_list_dif = {}
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

# 結果の確認


# print(adeq_list_dif['合計']['合計'])
json_data = json.dumps(adeq_list_dif, ensure_ascii=False)
print(json_data)

# total_sum = sum(sum(positions.values()) for positions in adeq_list_dif.values())  

# print(total_sum)

