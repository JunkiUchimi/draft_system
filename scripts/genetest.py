import random
import json

# 設定ファイルを読み込む
with open('config/config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

# Initialize the global variables
tradee = {}      # トレード対象の選手を格納する辞書
adeq_list = {}   # 各球団のポジション充実度を格納する辞書
players = {}     # 各球団の選手情報を格納する辞書
teams = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']    # 12球団のリスト

# Define the generate_player function
def generate_player(position_prefix, num_players):
    positions = ["捕手"] * 8 + ["内野手"] * 16 + ["外野手"] * 12 + ["投手"] * 32
    team_players = {}

    # 各ポジションごとに選手を生成
    for i in range(1, num_players + 1):
        random_number = round(random.uniform(0, 14), 1)  # 0から14の間のランダムな数値を生成
        position = positions[i - 1]  # 生成する選手のポジションを決定
        key = f"{position_prefix}{i}"  # 選手のキーを生成
        if position not in team_players:
            team_players[position] = []  # ポジションがまだ存在しない場合、新たにリストを作成
        team_players[position].append((key, random_number))  # 選手情報をリストに追加

    # 各ポジションごとに選手を数値で降順にソート
    sorted_players = {}
    for position, player_list in team_players.items():
        sorted_players.update({player[0]: [player[1], position] for player in sorted(player_list, key=lambda x: x[1], reverse=True)})
    return sorted_players

# ポジション充実度を計算する関数
def calculate_position_adequacy(team_name, sorted_players):
    catchers = []
    infielders = []
    outfielders = []
    pitchers = []

    cat_players = {key: value for key, value in sorted_players.items() if value[1] == '捕手'}
    inf_players = {key: value for key, value in sorted_players.items() if value[1] == '内野手'}
    out_players = {key: value for key, value in sorted_players.items() if value[1] == '外野手'}
    pit_players = {key: value for key, value in sorted_players.items() if value[1] == '投手'}

        # 捕手の数値に係数をかけてリストに格納
    for idx, key in enumerate(cat_players):
        if 0 <= idx < 2:
            catchers.append(cat_players[key][0] * config['multiplier_1'])
        elif 2 <= idx < 4:
            catchers.append(cat_players[key][0] * config['multiplier_2'])
        elif 4 <= idx < 6:
            catchers.append(cat_players[key][0] * config['multiplier_3'])
        elif 6 <= idx < 8:
            catchers.append(cat_players[key][0] * config['multiplier_4'])



    # 内野手も同様に計算
    for idx, key in enumerate(inf_players):
        if 0 <= idx < 4:
            infielders.append(inf_players[key][0] * config['multiplier_1'])
        elif 4 <= idx < 8:
            infielders.append(inf_players[key][0] * config['multiplier_2'])
        elif 8 <= idx < 12:
            infielders.append(inf_players[key][0] * config['multiplier_3'])
        elif 12 <= idx < 16:
            infielders.append(inf_players[key][0] * config['multiplier_4'])



    # 外野手も同様に計算
    for idx, key in enumerate(out_players):
        if 0 <= idx < 3:
            outfielders.append(out_players[key][0] * config['multiplier_1'])
        elif 3 <= idx < 6:
            outfielders.append(out_players[key][0] * config['multiplier_2'])
        elif 6 <= idx < 9:
            outfielders.append(out_players[key][0] * config['multiplier_3'])
        elif 9 <= idx < 12:
            outfielders.append(out_players[key][0] * config['multiplier_4'])




    # 投手も同様に計算
    for idx, key in enumerate(pit_players):
        if 0 <= idx < 8:
            pitchers.append(pit_players[key][0] * config['multiplier_1'])
        elif 8 <= idx < 16:
            pitchers.append(pit_players[key][0] * config['multiplier_2'])
        elif 16 <= idx < 24:
            pitchers.append(pit_players[key][0] * config['multiplier_3'])
        elif 24 <= idx < 32:
            pitchers.append(pit_players[key][0] * config['multiplier_4'])

    adeq_cat = sum(catchers) / 8  # 捕手の充実度を計算
    adeq_inf = sum(infielders) / 16  # 内野手の充実度を計算
    adeq_out = sum(outfielders) / 12  # 外野手の充実度を計算
    adeq_pit = sum(pitchers) / 32  # 投手の充実度を計算

    # adeq_listに新しいエントリーを追加
    if team_name not in adeq_list:
        adeq_list[team_name] = {}
    adeq_list[team_name]["捕手"] = adeq_cat
    adeq_list[team_name]["内野手"] = adeq_inf
    adeq_list[team_name]["外野手"] = adeq_out
    adeq_list[team_name]["投手"] = adeq_pit
    
    return adeq_cat, adeq_inf, adeq_out, adeq_pit

    
def choose_tradees(adeq_cat, adeq_inf, adeq_out, adeq_pit, sorted_players, team_name):
    # 上位2つの数値を見つける
    adeq_values = [("捕手", adeq_cat, 2), ("内野手", adeq_inf, 12), ("外野手", adeq_out, 27), ("投手", adeq_pit, 44)]
    top_two = sorted(adeq_values, key=lambda x: x[1], reverse=True)[:2]
    # added_player_keysを生成
    added_player_keys = [key for idx, key in enumerate(sorted_players) if idx in {top_two[0][2], top_two[1][2]}]

    # tradeeに追加
    for key in added_player_keys:
        tradee[key] = sorted_players[key]

    # 追加した選手をsorted_playersから削除
    for key in added_player_keys:
        del sorted_players[key]

    players[team_name] = sorted_players  # 球団の選手情報をplayers辞書に格納

# 球団ごとに選手を生成し、ポジション充実度を計算
for prefix in teams:
    sorted_players = generate_player(f'p_{prefix}', 68)  # 各球団のプレイヤーを生成
    team_name = prefix  # チーム名を取得
    calculate_position_adequacy(team_name, sorted_players)
    adeq_cat, adeq_inf, adeq_out, adeq_pit = calculate_position_adequacy(team_name, sorted_players)
    choose_tradees(adeq_out, adeq_pit, adeq_cat, adeq_inf, sorted_players, team_name)

# tradeeはp_j61': [13.2, '投手'], の形
# playersは{'a': {'p_a3': [9.4, '捕手'], 'p_a5': [5.4, '捕手'], の形
# adeq_listは{'a': {'捕手': 8.606666666666667, '内野手': 8.223333333333334, '外野手': 9.373333333333335, '投手': 10.647499999999999}, 
