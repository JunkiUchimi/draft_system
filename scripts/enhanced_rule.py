# enhanced_rule.py

from genetest import players
from tradee_value_calculation import tradee_value_dict

def provisional_draft():
    provisional_selections = {}
    for team in players.keys():
        if tradee_value_dict[team]:
            preferred_player = tradee_value_dict[team][0]  # 最も好ましい選手は一番前
            provisional_selections[team] = preferred_player
    return provisional_selections

def detect_cycles(provisional_selections):
    cycles = []
    visited = set()
    for team, player in provisional_selections.items():
        if team in visited:
            continue
        cycle = []
        current_team = team
        while current_team not in visited and current_team in provisional_selections:
            visited.add(current_team)
            cycle.append(current_team)
            next_team = provisional_selections[current_team]['team']
            if next_team == team:
                cycles.append(cycle)
                break
            current_team = next_team
    return cycles

def finalize_drafts(provisional_selections, cycles):
    for cycle in cycles:
        for team in cycle:
            player = provisional_selections[team]
            players[team].append(player)
            tradee_value_dict[team].remove(player)
    
    for team, player in provisional_selections.items():
        if player in tradee_value_dict[team]:
            players[team].append(player)
            tradee_value_dict[team].remove(player)

def execute_draft():
    while any(tradee_value_dict.values()):
        provisional_selections = provisional_draft()
        cycles = detect_cycles(provisional_selections)
        finalize_drafts(provisional_selections, cycles)

if __name__ == "__main__":
    execute_draft()
