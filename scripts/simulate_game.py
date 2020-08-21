import os
import json
from os import path
from random import randrange
from numpy.random import choice
import numpy as np
import time
from calculate_avg_hits import get_avg_hits

def get_pitch(pitcher, balls, strikes, batter):
    if 'L' in batter['hand']:
        against_array = pitcher['against_left']
    else:
        against_array = pitcher['against_right']
    count_dict = against_array[balls][strikes]
    if 'N/A' in count_dict:
        total = count_dict['total'] - count_dict['N/A']
    else:
        total = count_dict['total']
    pitch_list = []
    probability_list = []
    for item in count_dict:
        if 'total' not in item and 'N/A' not in item:
            pitch_list.append(item)
            probability_list.append(count_dict[item]/total)
    if not pitch_list:
        if balls > 0:
            return get_pitch(pitcher, balls - 1, strikes, batter)
        elif strikes > 0:
            return get_pitch(pitcher, balls, strikes - 1, batter)
        else:
            return 'Four-Seam Fastball', 5
    draw_pitch = choice(pitch_list, 1, p=probability_list)
    draw = draw_pitch[0]
    pitch_json = pitcher['pitch_types'][draw]
    zone_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    zone_prob = [0] * 15
    sum2 = 0
    for x in range (0,15):
        zone_prob[x] = pitch_json['zone'][x]/pitch_json['total']
        sum2 = sum2 + pitch_json['zone'][x]
    sum = 0
    for thing in zone_prob:
        sum = sum + thing
    zone_draw_2 = choice(zone_list, 1, p=zone_prob)
    zone_draw = zone_draw_2[0]
    #print(pitcher['name'] + " threw a " + draw + " in zone " + str(zone_draw) + " to batter " + batter['name'])
    return draw, zone_draw

def get_result(pitch, zone, batter):
    if pitch not in batter['pitches']:
        return 'S'
    batter_on_pitch = batter['pitches'][pitch]
    zone_list = batter_on_pitch[zone]
    result_draw = choice(zone_list)
    return result_draw

def analyze_result(outs, balls, strikes, result):
    new_batter = False
    if 'N/A' in result:
        result_str = "No Pitch"
        return outs, balls, strikes, result_str, new_batter
    elif 'C' in result or 'S' in result or 'L' in result or 'W' in result or 'T' in result or 'M' in result:
        #Strike
        strikes = strikes + 1
        result_str = 'Called Strike'
    elif 'F' in result:
        result_str = 'Foul Ball'
        if strikes < 2:
            strikes = strikes + 1
    elif 'B' in result:
        result_str = 'Called Ball'
        balls = balls + 1
    elif 'X' in result:
        result_str = 'Out in Play'
        outs = outs + 1
        strikes = 0
        balls = 0
        new_batter = True
    elif 'H' in result:
        result_str = 'Hit by Pitch'
        strikes = 0
        balls = 0
        new_batter = True
    elif 'D' in result or 'E' in result:
        result_str = 'Hit'
        strikes = 0
        balls = 0
        new_batter = True
    elif 'P' in result or 'I' in result:
        result_str = "No decision"
    else:
        print(result)
        result_str = "No decision"
    if strikes == 3:
        result_str = result_str + ": Strikeout"
        outs = outs + 1
        strikes = 0
        balls = 0
        new_batter = True
    if balls == 4:
        strikes = 0
        balls = 0
        new_batter = True
        result_str = result_str + ": Walk"
    return outs, balls, strikes, result_str, new_batter

def simulate(home_pitch, away_pitch, home_lineup, away_lineup):
    home_hits = 0
    away_hits = 0
    home_at_bat = 0
    away_at_bat = 0
    top_inning = True
    bat_lineup = []
    at_bat = 0
    for x in range(0,18):
        #print("Inning: " + str(int(x/2)+1))
        if top_inning:
            pitch_file = "../players/jsons/" + home_pitch.replace(' ', '_') + ".json"
            if not path.exists(pitch_file):
                return -1, -1
            pitcher_json = json.loads(open(pitch_file).read())
            bat_lineup = away_lineup
            at_bat = away_at_bat
        else:
            pitch_file = "../players/jsons/" + away_pitch.replace(' ', '_') + ".json"
            if not path.exists(pitch_file):
                return -1, -1
            pitcher_json = json.loads(open(pitch_file).read())
            bat_lineup = home_lineup
            at_bat = home_at_bat
        outs = 0
        balls = 0
        strikes = 0
        new_batter = False
        while outs < 3:
            batter = bat_lineup[at_bat]
            batter_file = "../players/batter-jsons/" + batter.replace(' ', '_') + ".json"
            if path.exists(batter_file):
                batter_json = json.loads(open(batter_file).read())
                pitch_thrown, pitch_zone = get_pitch(pitcher_json, balls, strikes, batter_json)
                pitch_result = get_result(pitch_thrown, pitch_zone, batter_json)
                outs, balls, strikes, result, new_batter = analyze_result(outs, balls, strikes, pitch_result)
                #print(f"{outs}:{balls}:{strikes} {result}")
                if 'Walk' in result or 'Hit' in result:
                    #print(batter_json['name'] + " gets a hit")
                    if top_inning:
                        away_hits = away_hits + 1
                    else:
                        home_hits = home_hits + 1
                if new_batter:
                    #print(pitcher_json['name'] + " against " + batter_json['name'] + " resulted in a " + result)
                    at_bat = (at_bat + 1) % 9
                    new_batter = False
            else:
                #print(batter + " doesn't exist in our records yet")
                at_bat = (at_bat + 1) % 9
        if top_inning:
            away_at_bat = at_bat
        else:
            home_at_bat = at_bat
        top_inning = not top_inning
    #print(f"Home team had {home_hits} hits")
    #print(f"Away team had {away_hits} hits")
    return home_hits, away_hits

def read_lineups(lineup_file):
    # Using readlines()
    file = open(lineup_file, 'r')
    lines = file.readlines()

    count = 0
    # Strips the newline character
    away_lineup = []
    home_lineup = []
    for line in lines:
        name = line.split(" ")
        if count < 9:
            if len(name) == 5:
                away_lineup.append(name[0] + " " + name[1] + " " + name[2])
            else:
                away_lineup.append(name[0] + " " + name[1])
        else:
            if len(name) == 5:
                home_lineup.append(name[0] + " " + name[1] + " " + name[2])
            else:
                home_lineup.append(name[0] + " " + name[1])
        count = count + 1
    return home_lineup, away_lineup

def simulate_games(away_pitcher, home_pitcher, away_name, home_name, away_lineup, home_lineup, game_dict):
    home_array = []
    away_array = []
    for x in range(0, 1000):
        home, away = simulate(home_pitcher, away_pitcher, home_lineup, away_lineup)
        if home == -1 and away == -1:
            with open("../logs/history.txt", "a") as myfile:
                myfile.write(away_name + " at " + home_name + ": N/A\n")
            break
        else:
            home_array.append(home)
            away_array.append(away)
    if home != -1 and away != -1:
        np_home = np.array(home_array)
        np_away = np.array(away_array)
        away_expected = str(sum(away_array)/len(away_array))
        home_expected = str(sum(home_array)/len(home_array))
        game_dict['home_hits'] = home_expected
        game_dict['away_hits'] = away_expected
        with open("../logs/history.txt", "a") as myfile:
            myfile.write(away_name + " at " + home_name + ": " + away_expected + ", " + home_expected + ": (" + str(get_avg_hits(away_name)) + "),(" + str(get_avg_hits(home_name)) + ")\n")
        print("Average home team hits = " + str(sum(home_array)/len(home_array)) + " with standard deviation: " + str(np.std(np_home)))
        print("Average away team hits = " + str(sum(away_array)/len(away_array)) + " with standard deviation: " + str(np.std(np_away)))

if __name__ == "__main__":
    home_pitcher = "Derek Holland"
    away_pitcher = "Josh Lindblom"
    away_lineup = ['Lorenzo Cain', 'Keston Hiura', 'Christian Yelich', 'Ryan Braun', 'Jedd Gyorko', 'Avisail Garcia', 'Justin Smoak', 'Manny Pina', 'Orlando Arcia']
    home_lineup = ['Adam Frazier', 'Kevin Newman', 'Josh Bell', 'Colin Moran', 'Bryan Reynolds', 'Phillip Evans', 'Guillermo Heredia', 'Cole Tucker', 'John Ryan Murphy']
    hhits, ahits = simulate(home_pitcher, away_pitcher, home_lineup, away_lineup)
    print(hhits, " : ", ahits)
