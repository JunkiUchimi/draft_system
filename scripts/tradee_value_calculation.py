# トレード候補選手をそのチームの評価値順に並べる。計算は（WAR/ポジション充実度）

import pickle

# genetest.pyの内容をインポートして実行
import genetest

# genetest.pyから必要な変数を取得
adeq_list = genetest.adeq_list  # 各球団のポジション充実度を表す辞書
tradee = genetest.tradee        # トレード対象の選手リスト (選手の値, ポジション)

# 各球団ごとにtradeeの値をポジション充実度で割ったものを格納する
tradee_value_dict = {}
for team in adeq_list.keys():
    team_tradee_values = {}
    for player_id, player_info in tradee.items():
        position = player_info[1]  # 選手のポジションを取得
        # 選手の値を球団のポジション充実度で割る
        value = round(player_info[0] / adeq_list[team][position], 2)
        # 選手IDをキーとしてリストを辞書に追加
        team_tradee_values[player_id] = [player_info[0], position, value]
    # 計算した値で降順にソート
    sorted_team_tradee_values = dict(sorted(team_tradee_values.items(), key=lambda item: item[1][2], reverse=True))
    # ソートした辞書を球団名をキーとして辞書に格納
    tradee_value_dict[team] = sorted_team_tradee_values

print(adeq_list)
# for key, value in tradee_value_dict.items():
#     print(f"\n{key}: {value}")

# 新しいファイルにtradee_value_dictを保存
# with open('/mnt/data/tradee_value_dict.pkl', 'wb') as f:
#     pickle.dump(tradee_value_dict, f)  # tradee_value_dictをpickle形式で保存

#tradee_value_dictは以下の形式になる。{'a': {'p_k26': [12.2, '外野手', 1.7509169191516503], ...