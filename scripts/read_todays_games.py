import requests
from bs4 import BeautifulSoup
from simulate_game import simulate_games
import time
from datetime import date, datetime, timedelta
import json

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
    game_day_dict = {'631529': {'status': 'processed', 'id': '631529', 'home_team': 'Rockies', 'away_team': 'Giants', 'date': '3:10 PM', 'home_pitcher': 'Kyle Freeland', 'away_pitcher': 'Logan Webb', 'home_lineup': ['Raimel Tapia', 'Trevor Story', 'Nolan Arenado', 'Charlie Blackmon', 'Kevin Pillar', 'Garrett Hampson', 'Sam Hilliard', 'Josh Fuentes', 'Tony Wolters'], 'away_lineup': ['Donovan Solano', 'Mike Yastrzemski', 'Evan Longoria', 'Wilmer Flores', 'Darin Ruf', 'Alex Dickerson', 'Joey Bart', 'Daniel Robertson', 'Mauricio Dubon'], 'home_hits': '13.619', 'away_hits': '15.055'}, '631673': {'status': 'processed', 'id': '631673', 'home_team': 'Orioles', 'away_team': 'Mets', 'date': '4:05 PM', 'home_pitcher': 'John Means', 'away_pitcher': 'Michael Wacha', 'home_lineup': ['Cedric Mullins', 'Anthony Santander', 'Jose Iglesias', 'Renato Nunez', 'Pedro Severino', 'Ryan Mountcastle', 'Rio Ruiz', 'Pat Valaika', 'Andrew Velazquez'], 'away_lineup': ['Jeff McNeil', 'J.D. Davis', 'Michael Conforto', 'Todd Frazier', 'Robinson Cano', 'Pete Alonso', 'Wilson Ramos', 'Jake Marisnick', 'Amed Rosario'], 'home_hits': '9.87', 'away_hits': '15.371'}, '631587': {'status': 'processed', 'id': '631587', 'home_team': 'Reds', 'away_team': 'Cardinals', 'date': 'warmup\n                                                                                \n                                                                                                •', 'home_pitcher': 'Tyler Mahle', 'away_pitcher': 'Johan Oviedo', 'home_lineup': ['Joey Votto', 'Nick Castellanos', 'Jesse Winker', 'Eugenio Suarez', 'Mike Moustakas', 'Brian Goodwin', 'Jose Garcia', 'Shogo Akiyama', 'Tucker Barnhart'], 'away_lineup': ['Kolten Wong', 'Tommy Edman', 'Paul Goldschmidt', 'Brad Miller', 'Paul DeJong', 'Yadier Molina', 'Matt Carpenter', "Tyler O'Neill", 'Lane Thomas']}, '631308': {'status': 'processed', 'id': '631308', 'home_team': 'Marlins', 'away_team': 'Blue Jays', 'date': 'warmup\n                                                                                \n                                                                                                •', 'home_pitcher': 'Sixto Sanchez', 'away_pitcher': 'Hyun Jin Ryu', 'home_lineup': ['Jon Berti', 'Starling Marte', 'Garrett Cooper', 'Jesus Aguilar', 'Brian Anderson', 'Corey Dickerson', 'Lewis Brinson', 'Jorge Alfaro', 'Jazz Chisholm'], 'away_lineup': ['Cavan Biggio', 'Randal Grichuk', 'Jonathan Villar', 'Teoscar Hernandez', 'Rowdy Tellez', 'Lourdes Gurriel Jr.', 'Travis Shaw', 'Santiago Espinal', 'Danny Jansen']}, '631111': {'status': 'processed', 'id': '631111', 'home_team': 'Pirates', 'away_team': 'Cubs', 'date': '7:05 PM', 'home_pitcher': 'Joe Musgrove', 'away_pitcher': 'Kyle Hendricks', 'home_lineup': ['Cole Tucker', 'Adam Frazier', 'Kevin Newman', 'Josh Bell', 'Colin Moran', "Ke'Bryan Hayes", 'Gregory Polanco', 'Anthony Alford', 'Jacob Stallings'], 'away_lineup': ['Ian Happ', 'Willson Contreras', 'Anthony Rizzo', 'Javier Baez', 'Steven Souza Jr.', 'Jose Martinez', 'Cameron Maybin', 'David Bote', 'Nico Hoerner'], 'home_hits': '18.112', 'away_hits': '12.777'}, '631145': {'status': 'processed', 'id': '631145', 'home_team': 'Phillies', 'away_team': 'Nationals', 'date': '7:05 PM', 'home_pitcher': 'Zack Wheeler', 'away_pitcher': 'Max Scherzer', 'home_lineup': ['Andrew McCutchen', 'Didi Gregorius', 'Bryce Harper', 'J.T. Realmuto', 'Jay Bruce', 'Jean Segura', 'Alec Bohm', 'Neil Walker', 'Adam Haseley'], 'away_lineup': ['Trea Turner', 'Juan Soto', 'Howie Kendrick', 'Asdrubal Cabrera', 'Adam Eaton', 'Kurt Suzuki', 'Brock Holt', 'Luis Garcia', 'Victor Robles'], 'home_hits': '13.419', 'away_hits': '12.62'}, '631194': {'status': 'processed', 'id': '631194', 'home_team': 'Yankees', 'away_team': 'Rays', 'date': '7:05 PM', 'home_pitcher': 'Jordan Montgomery', 'away_pitcher': 'Charlie Morton', 'home_lineup': ['DJ LeMahieu', 'Luke Voit', 'Aaron Hicks', 'Clint Frazier', 'Gio Urshela', 'Mike Tauchman', 'Gary Sanchez', 'Brett Gardner', 'Tyler Wade'], 'away_lineup': ['Manuel Margot', 'Randy Arozarena', 'Austin Meadows', 'Mike Brosseau', 'Willy Adames', 'Joey Wendle', 'Hunter Renfroe', 'Kevan Smith', 'Nate Lowe'], 'home_hits': '15.181', 'away_hits': '17.078'}, '631624': {'status': 'processed', 'id': '631624', 'home_team': 'Red Sox', 'away_team': 'Braves', 'date': '7:30 PM', 'home_pitcher': 'Robinson Leyer', 'away_pitcher': 'Robbie Erlin', 'home_lineup': ['Alex Verdugo', 'Rafael Devers', 'Xander Bogaerts', 'J.D. Martinez', 'Kevin Plawecki', 'Michael Chavis', 'Jackie Bradley Jr.', 'Bobby Dalbec', 'Jose Peraza'], 'away_lineup': ['Dansby Swanson', 'Freddie Freeman', 'Marcell Ozuna', 'Nick Markakis', "Travis d'Arnaud", 'Austin Riley', 'Adam Duvall', 'Johan Camargo', 'Ender Inciarte']}, '631283': {'status': 'processed', 'id': '631283', 'home_team': 'Brewers', 'away_team': 'Tigers', 'date': '7:40 PM', 'home_pitcher': 'Adrian Houser', 'away_pitcher': 'Spencer Turnbull', 'home_lineup': ['Ben Gamel', 'Christian Yelich', 'Keston Hiura', 'Justin Smoak', 'Avisail Garcia', 'Omar Narvaez', 'Luis Urias', 'Eric Sogard', 'Orlando Arcia'], 'away_lineup': ['Victor Reyes', 'Jonathan Schoop', 'Miguel Cabrera', 'Jeimer Candelario', 'Willi Castro', 'Christin Stewart', 'Jorge Bonifacio', 'Austin Romine', 'Isaac Paredes'], 'home_hits': '15.217', 'away_hits': '13.972'}, '631404': {'status': 'processed', 'id': '631404', 'home_team': 'Royals', 'away_team': 'Indians', 'date': '8:05 PM', 'home_pitcher': 'Jakob Junis', 'away_pitcher': 'Triston McKenzie', 'home_lineup': ['Whit Merrifield', 'Hunter Dozier', 'Jorge Soler', 'Maikel Franco', 'Ryan McBroom', 'Alex Gordon', 'Adalberto Mondesi', 'Nicky Lopez', 'Cam Gallagher'], 'away_lineup': ['Cesar Hernandez', 'Jose Ramirez', 'Francisco Lindor', 'Carlos Santana', 'Franmil Reyes', 'Tyler Naquin', 'Josh Naylor', 'Roberto Perez', 'Delino DeShields']}, '631431': {'status': 'processed', 'id': '631431', 'home_team': 'Astros', 'away_team': 'Rangers', 'date': '8:10 PM', 'home_pitcher': 'Cristian Javier', 'away_pitcher': 'Kolby Allard', 'home_lineup': ['George Springer', 'Jose Altuve', 'Michael Brantley', 'Yuli Gurriel', 'Kyle Tucker', 'Carlos Correa', 'Josh Reddick', 'Aledmys Diaz', 'Martin Maldonado'], 'away_lineup': ['Leody Taveras', 'Isiah Kiner-Falefa', 'Shin-Soo Choo', 'Nick Solak', 'Joey Gallo', 'Elvis Andrus', 'Derek Dietrich', 'Anderson Tejeda', 'Jeff Mathis']}, '631253': {'status': 'processed', 'id': '631253', 'home_team': 'Twins', 'away_team': 'White Sox', 'date': '8:10 PM', 'home_pitcher': 'Jose Berrios', 'away_pitcher': 'Reynaldo Lopez', 'home_lineup': ['Max Kepler', 'Josh Donaldson', 'Jorge Polanco', 'Nelson Cruz', 'Eddie Rosario', 'Miguel Sano', 'Luis Arraez', 'Jake Cave', 'Ryan Jeffers'], 'away_lineup': ['Tim Anderson', 'Yoan Moncada', 'Yasmani Grandal', 'Jose Abreu', 'Eloy Jimenez', 'Edwin Encarnacion', 'Luis Robert', 'Nomar Mazara', 'Nick Madrigal'], 'home_hits': '14.293', 'away_hits': '14.268'}, '631356': {'status': 'processed', 'id': '631356', 'home_team': 'Dodgers', 'away_team': 'D-backs', 'date': '9:40 PM', 'home_pitcher': 'Walker Buehler', 'away_pitcher': 'Zac Gallen', 'home_lineup': ['Mookie Betts', 'Corey Seager', 'AJ Pollock', 'Max Muncy', 'Chris Taylor', 'Joc Pederson', 'Will Smith', 'Edwin Rios', 'Gavin Lux'], 'away_lineup': ['Kole Calhoun', 'Ketel Marte', 'Christian Walker', 'David Peralta', 'Eduardo Escobar', 'Josh Rojas', 'Nick Ahmed', 'Daulton Varsho', 'Carson Kelly'], 'home_hits': '15.935', 'away_hits': '14.22'}, '631379': {'status': 'waiting for lineups', 'id': '631379', 'home_team': 'Angels', 'away_team': 'Padres', 'date': '9:40 PM', 'home_pitcher': 'Julio Teheran', 'away_pitcher': 'Dinelson Lamet', 'home_lineup': [], 'away_lineup': []}, '631054': {'status': 'processed', 'id': '631054', 'home_team': 'Mariners', 'away_team': 'Athletics', 'date': 'PPD', 'home_pitcher': 'Yusei Kikuchi', 'away_pitcher': 'TBD', 'home_lineup': [], 'away_lineup': []}}
    still_running = True
    with open("../logs/history.txt", "a") as myfile:
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
    outfile_path = "../DateFiles/" + str(today) + ".json"
    with open(outfile_path, 'w', encoding='utf-8') as f:
        json.dump(game_day_dict, f, ensure_ascii=False, indent=4)
    print("************FINISHED************")
