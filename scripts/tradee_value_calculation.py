# トレード候補選手をそのチームの評価値順に並べる。計算は（WAR/ポジション充実度）

import pickle, pprint

# genetest.pyの内容をインポートして実行
import genetest

# genetest.pyから必要な変数を取得
adeq_list = genetest.adeq_list  # 各球団のポジション充実度を表す辞書
tradee = genetest.tradee        # トレード対象の選手リスト (選手の値, ポジション)
position_order = {
    '捕手': 1,
    '内野手': 2,
    '外野手': 3,
    '投手': 4
}

# 各球団ごとにtradeeの値をポジション充実度で割ったものを格納する
tradee_value_dict = {}

# トレード候補選手をそのチームの評価値順に並べる。計算は（WAR/ポジション充実度）

import pickle, copy

# genetest.pyの内容をインポートして実行
from genetest import adeq_list, tradee, teams, players, adeq_list, calculate_position_adequacy
# print(players["a"])
adeq_list_before = copy.deepcopy(adeq_list)
total_before = 0
for key in adeq_list:
    for category in adeq_list[key]:
        total_before += adeq_list[key][category]

# 各球団ごとにtradeeの値をポジション充実度で割ったものを格納する
position_order = {
    '捕手': 0,
    '内野手': 1,
    '外野手': 2,
    '投手': 3
}

tradee_value_dict = {}

for team in teams:
    team_tradee_values = {}
    total_before = 0
    for position in adeq_list[team].keys():
        total_before += adeq_list_before[team][position]
    for player_id, player_info in tradee.items():
        position = player_info[1]  # 選手のポジションを取得
        players[team][player_id] = player_info

        sorted_players = dict(sorted(players[team].items(), key=lambda item: (position_order[item[1][1]], -item[1][0])))

        del players[team][player_id]
        adeq_list = {}   # 各球団のポジション充実度を格納する辞書
        adeq_list = calculate_position_adequacy(team, sorted_players)
        total = 0
        for posi in adeq_list[team].keys():
            total += adeq_list[team][posi]
        value = total - total_before
      

        # 選手IDをキーとしてリストを辞書に追加
        team_tradee_values[player_id] = [player_info[0], position, value]
    # 計算した値で降順にソート
    sorted_team_tradee_values = dict(sorted(team_tradee_values.items(), key=lambda item: item[1][2], reverse=True))
    # ソートした辞書を球団名をキーとして辞書に格納
    tradee_value_dict[team] = sorted_team_tradee_values
