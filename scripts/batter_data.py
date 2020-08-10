import os
import json
from os import path

def handle_pitch(batter, zone, pitch, result):
    if pitch in batter['pitches']:
        batter['pitches'][pitch][zone].append(result)
    else:
        batter['pitches'][pitch] = [[]] * 15
        batter['pitches'][pitch][zone].append(result)
    return batter

def create_jsons(filename):
    file = "players/" + filename
    f = open(file)
    total = 0
    for line in f:
        pitch = line.split("|")
        batter = pitch[2].strip('.')
        batter_file = "players/batter-jsons/" + batter.replace(" ", "_") + ".json"
        pitch_type = pitch[6]
        zone = int(pitch[11])
        result = pitch[5]
        hand = pitch[3]
        if path.exists(batter_file):
            batter_json = json.loads(open(batter_file).read())
            result_json = handle_pitch(batter_json, zone, pitch_type, result)
        else:
            batter_json = json.loads(open('players/batter_json.json').read())
            batter_json['name'] = batter
            batter_json['hand'] = hand
            result_json = handle_pitch(batter_json, zone, pitch_type, result)
        with open(batter_file, 'w') as outfile:
            json.dump(result_json, outfile)


def run_all():
    for filename in os.listdir("/home/nick/Desktop/players"):
        if filename.endswith(".txt"):
            create_jsons(filename)

if __name__ == "__main__":
    run_all()
