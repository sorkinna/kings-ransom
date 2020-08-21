import os
import json

def get_all_avg_hits():
    with open("../logs/history.txt", "r") as myfile:
        lines = myfile.readlines()
        teams_dict = {}
        for line in lines:
            split = line.split(":")
            if len(split) > 2 and 'PPD' not in split[2] and 'N/A' not in split[2]:
                teams = split[0].split(" at ")
                away = teams[0]
                home = teams[1]
                if home in teams_dict.keys():
                    home_hits_list = teams_dict[home]
                else:
                    teams_dict[home] = []
                    home_hits_list = teams_dict[home]
                if away in teams_dict.keys():
                    away_hits_list = teams_dict[away]
                else:
                    teams_dict[away] = []
                    away_hits_list = teams_dict[away]
                hits = split[1].strip().split(", ")
                if 'N/A' not in hits[0]:
                    away_hits = float(hits[0])
                    home_hits = float(hits[1])
                    home_hits_list.append(home_hits)
                    away_hits_list.append(away_hits)
        final_dict = {}
        for key in teams_dict.keys():
            final_dict[key] = rount(sum(teams_dict[key])/len(teams_dict[key]), 3)
            print(key + " average hits: " + str(sum(teams_dict[key])/len(teams_dict[key])))
        return final_dict

def get_avg_hits(team):
    with open("../logs/history.txt", "r") as myfile:
        lines = myfile.readlines()
        hits_list = []
        for line in lines:
            split = line.split(":")
            if len(split) > 2 and 'PPD' not in split[2] and 'N/A' not in split[2]:
                teams = split[0].split(" at ")
                away = teams[0]
                home = teams[1]
                hits = split[1].strip().split(", ")
                if 'N/A' not in hits[0]:
                    away_hits = float(hits[0])
                    home_hits = float(hits[1])
                    if away in team:
                        hits_list.append(away_hits)
                    elif home in team:
                        hits_list.append(home_hits)
                    else:
                        continue
        print(hits_list)
        return round(sum(hits_list)/len(hits_list), 3)

if __name__ == "__main__":
    print(get_avg_hits("Blue Jays"))
