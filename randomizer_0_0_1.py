def read_seed_file(run_year, region):
    # reads the file with the seed information (tab delimited as seed#    team_name)
    # and produces a list of teams
    # open the file
    directory = "F:/Github/marchmadness_randomizer/"
    file_path = directory + runyear + '_' + region + '_' + 'teams.txt'
    f = open(file_path)

    # initialize the Region class
    reg = Region(region)

    # there are always 16 teams in a single region
    for i in range(16):
        line_output = f.readline()
        seed, team = line_output.strip().split("\t")
        reg.append_team(Team(team, seed, reg.name))

    reg.print_teams()

    # create matchups...
    # matchup = {}
    # while teams:
    #     print(str(teams[min(teams)]), "(" + str(min(teams)) + ")", 'Vs.', str(teams[max(teams)]),
    #           "(" + str(max(teams)) + ")")
    #     matchup[min(teams)] = max(teams)
    #     del teams[min(teams)]
    #     del teams[max(teams)]
    # print(matchup)
    # return teams


def get_win_odds(seed1, seed2, round_num):
    # return odds of winning for seed 1, given seed 1 and 2

    # round_num can be: 64, 32, 16, 8, 4, 2

    # hardcoded odds for RO64#
    # matchup    seed    % chance win    seed    % chance win
    # 1v16       1       99.50%          16      0.50%
    # 2v15       2       98.00%          15      2.00%
    # 3v14       3       93.00%          14      7.00%
    # 4v13       4       85.00%          13      15.00%
    # 5v12       5       70.59%          12      29.41%
    # 6v11       6       64.71%          11      35.29%
    # 7v10       7       58.82%          10      41.18%
    # 8v9        8       53.00%          9       47.00%

    if round_num == 64:
        # use hardcoded odds
        if seed1 == 1:
            return 0.995
        elif seed1 == 2:
            return 0.98
        elif seed1 == 3:
            return 0.93
        elif seed1 == 4:
            return 0.85
        elif seed1 == 5:
            return 12 / 17
        elif seed1 == 6:
            return 11 / 17
        elif seed1 == 7:
            return 10 / 17
        elif seed1 == 8:
            return 9 / 17
        else:
            return bool(0)
    else:
        return seed2 / (seed1 + seed2)


class Team:
    def __init__(self, name, seed, region):
        self.name = name
        self.seed = int(seed)
        self.region = region


class Region:
    # this is the class that represents a region which contains the 16 teams that make up the region
    def __init__(self, name):
        self.teams = [] # array of teams
        self.name = name # name of the region (eg. Midwest)

    def append_team(self, team_cl):
        self.teams.append(team_cl)

    def print_teams(self):
        print(self.name)
        print("------------------------------------------------------------")
        for team in self.teams:
            if team.seed < 10: # prettier formatting
                print("(" + str(team.seed) + ")  " + team.name)
            else:
                print("(" + str(team.seed) + ") " + team.name)
        print("------------------------------------------------------------")
        print("")


def winner_print(rand_outcome, team_1, team_2, win_odds):
    if rand_outcome <= win_odds:
        winner = team_1
    else:
        winner = team_2
    print("---------------------------------------------")
    print("Matchup is between", team_1, "and", team_2 + ".")
    print(team_1, "has a", str(round(win_odds * 100, 2)) + "% chance of winning.")
    print(winner, "advances. (", round(rand_outcome, 3), ")")
    print("---------------------------------------------")
    print("")

# process
# read team list
# prepare matchups for round of 64
# calculate odds for each matchup
# generate random results for each matchup based on odds
# prepare matchups for round of 32
# calculate odds for each matchup
# generate random results for each matchup based on odds

# prepare matchups for sweet 16
# calculate odds for each matchup
# generate random results for each matchup based on odds

# prepare matchups for elite 8
# calculate odds for each matchup
# generate random results for each matchup based on odds

# first time teams are crossing regions
# prepare matchups for final 4
# calculate odds for each matchup
# generate random results for each matchup based on odds

# prepare matchups for championship
# calculate odds for matchup
# calculate possible scores for matchup
# generate random results for each matchup based on odds

if __name__ == '__main__':
    # initialization of process..
    print('Beginning of the process...')
    runyear = input("Enter year to run the program on: ")
    print("")
    print(str(runyear))

    # read the seed files to build the teams
    # assume that the format of the file name is like "YYYY_[region]_teams.txt"
    region_list = ("east", "midwest", "south", "west")
    for region_name in region_list:
        read_seed_file(runyear, region_name)
