import os
import json

def create_count_spread(pitch, player_json):
    against_json = None
    if pitch[3] == "R":
        against_json = player_json["against_right"]
    else:
        against_json = player_json["against_left"]
    if int(pitch[8]) < 4 and int(pitch[9]) < 3:
        count_json = against_json[int(pitch[8])][int(pitch[9])]
        count_json["total"] = count_json["total"] + 1
        if pitch[6] not in count_json:
            count_json[pitch[6]] = 1
        else:
            count_json[pitch[6]] = count_json[pitch[6]] + 1

def analyze_pitch_type(pitch_type_dict):
    pitch_type_json = {"avg_speed": 0, "top_speed": 0, "percent_left": 0, "percent_right": 0, "zone": [], "total": 0, "name": ""}
    final_array = []
    total = 0
    left = 0
    right = 0
    top_speed = 0
    speed_sum = 0
    zone = [0] * 15
    name = ""
    for pitch in pitch_type_dict:
        if total == 0:
            name = pitch[6]
        pitch[12].strip()
        total = total + 1
        if pitch[3] == "R":
            right = right + 1
        else:
            left = left + 1
        zone[int(pitch[11])] = zone[int(pitch[11])] + 1
        speed_sum = speed_sum + int(pitch[12])
        if int(pitch[12]) > top_speed:
            top_speed = int(pitch[12])
    avg_speed = speed_sum / total
    final_pitch_json = pitch_type_json
    final_pitch_json["name"] = name
    final_pitch_json["avg_speed"] = avg_speed
    final_pitch_json["top_speed"] = top_speed
    final_pitch_json["percent_left"] = (left/total) * 100
    final_pitch_json["percent_right"] = (right/total) * 100
    final_pitch_json["zone"] = zone
    final_pitch_json["total"] = total

    return final_pitch_json

def create_json(filename):
    f = open(filename)
    player_json = json.loads(open('json_template.json').read())
    total_pitch_types = {}
    #player_json = json.loads(json_template)
    total = 0
    for line in f:
        pitch = line.split("|")
        if total == 0:
            player_json["name"] = filename.replace("_", " ")[:-4]
            player_json["hand"] = pitch[1]
        total = total + 1
        create_count_spread(pitch, player_json)

        if pitch[6] not in total_pitch_types:
            total_pitch_types[pitch[6]] = []
        total_pitch_types[pitch[6]].append(pitch)

    for pitch_type in total_pitch_types:
        player_json["pitch_types"][pitch_type] = analyze_pitch_type(total_pitch_types[pitch_type])
    player_json["total_pitches"] = total
    return player_json

def run_all():
    for filename in os.listdir("/home/nick/Desktop/players"):
        if filename.endswith(".txt"):
            temp_json = create_json(filename)
            player_name = filename[:-4]
            json_file = "jsons/" + player_name + ".json"
            with open(json_file, 'w') as outfile:
                json.dump(temp_json, outfile)

if __name__ == "__main__":
    run_all()
