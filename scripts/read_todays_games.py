import requests
from bs4 import BeautifulSoup
from simulate_game import simulate_games
import time
from datetime import date, datetime, timedelta

def read_games(game_day_dict):
    URL = 'https://www.mlb.com/starting-lineups'
    #URL = 'https://www.mlb.com/starting-lineups/2020-07-26'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id='starting-lineups_index')

    #print(results.prettify())

    job_elems = results.find_all('div', class_='starting-lineups__matchup')

    for job_elem in job_elems:
        game_identifier = job_elem['data-gamepk']
        if game_identifier in game_day_dict.keys():
            game_dict = game_day_dict[game_identifier]
        else:
            game_dict = {}
        if 'status' not in game_dict.keys():
            game_dict['status'] = 'game created'
        game_time = job_elem.find('div', class_='starting-lineups__game-date-time').text.strip()
        home_team = job_elem.find('span', class_='starting-lineups__team-name starting-lineups__team-name--home').text.strip()
        away_team = job_elem.find('span', class_='starting-lineups__team-name starting-lineups__team-name--away').text.strip()
        game_dict['id'] = game_identifier
        game_dict['home_team'] = home_team
        game_dict['away_team'] = away_team
        game_dict['date'] = game_time
        pitchers = job_elem.find_all('div', class_='starting-lineups__pitcher-name')
        ind = 0
        for pitcher in pitchers:
            if ind == 0:
                away_pitcher = pitcher.text.strip()
                ind = ind + 1
            else:
                home_pitcher = pitcher.text.strip()
        game_dict['home_pitcher'] = home_pitcher
        game_dict['away_pitcher'] = away_pitcher
        away_lineup = []
        home_lineup = []
        lineups = job_elem.find('div', class_='starting-lineups__teams starting-lineups__teams--sm starting-lineups__teams--xl')
        players = lineups.find_all('li', class_='starting-lineups__player')
        count = 0
        for player in players:
            player_stripped = player.text.strip()
            name = player_stripped.split(" ")
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
        game_dict['home_lineup'] = home_lineup
        game_dict['away_lineup'] = away_lineup

        if away_lineup and home_lineup and game_dict['status'] not in 'processed':
            simulate_games(away_pitcher, home_pitcher, away_team, home_team, away_lineup, home_lineup, game_dict)
            game_dict['status'] = 'processed'
        elif 'PPD' in game_time:
            game_dict['date'] = 'PPD'
            game_dict['status'] = 'processed'
        elif not away_lineup or not home_lineup:
            game_dict['status'] = 'waiting for lineups'

        game_day_dict[game_identifier] = game_dict
    return game_day_dict

if __name__ == "__main__":
    starttime = time.time()
    today = date.today()
    game_day_dict = {}
    still_running = True
    with open("history.txt", "a") as myfile:
        myfile.write("\n" + str(today) + "\n")
    while still_running:
        game_day_dict = read_games(game_day_dict)
        print(game_day_dict)
        still_running = False
        for item in game_day_dict.keys():
            if game_day_dict[item]['status'] not in 'processed':
                still_running = True
        if still_running:
            print("sleeping")
            timer = datetime.now() + timedelta(minutes=30)
            time_str = timer.strftime('%H:%M')
            print("next run at ", time_str)
            time.sleep(1800)
            print("done sleeping")
        #time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    outfile_path = "DateFiles/" + str(today) + ".json"
    with open(outfile_path, 'w') as outfile:
        json.dump(game_day_dict, outfile, indent=4, sort_keys=True)
    print("************FINISHED************")
