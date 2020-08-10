
with open("history.txt", "r") as myfile:
    lines = myfile.readlines()
    right_count = 0
    wrong_count = 0
    big_diff_right = 0
    big_diff_wrong = 0
    for line in lines:
        split = line.split(":")
        if len(split) > 2 and 'PPD' not in split[2]:
            teams = split[0].split(" at ")
            away = teams[0]
            home = teams[1]
            hits = split[1].strip().split(", ")
            if 'N/A' not in hits[0]:
                away_hits = float(hits[0])
                home_hits = float(hits[1])
                diff = away_hits - home_hits
                winning_team = split[2].strip()
                if winning_team in home and diff < 0:
                    right_count = right_count + 1
                elif winning_team in away and diff > 0:
                    right_count = right_count + 1
                else:
                    wrong_count = wrong_count + 1
    print("right count: ", right_count)
    print("wrong count: ", wrong_count)
    print("correct %: ", str(right_count/(right_count + wrong_count)))
