import random


def read_seed_file(run_year, region):
    # reads the file with the seed information (tab delimited as seed#    team_name)
    # and produces a list of teams

    # open the file
    directory = "F:/Github/marchmadness_randomizer/"
    file_path = directory + run_year + '_' + region + '_' + 'teams.txt'
    f = open(file_path)

    # initialize the Region class
    return_region = Region(region)

    # there are always 16 teams in a single region
    for i in range(16):
        line_output = f.readline()
        seed, team = line_output.strip().split("\t")
        return_region.append_team(Team(team, seed, return_region.name))

    # reg.print_teams()

    return return_region


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

class Team:
    def __init__(self, name, seed, region):
        self.name = name
        self.seed = int(seed)
        self.region = region


class Region:
    # this is the class that represents a region which contains the 16 teams that make up the region
    def __init__(self, name):
        self.teams = []  # array of teams
        self.name = name  # name of the region (eg. Midwest)

    def append_team(self, team_cl):
        self.teams.append(team_cl)

    def print_teams(self):
        print(self.name)
        print("------------------------------------------------------------")
        for team in self.teams:
            if team.seed < 10:  # prettier formatting
                print("(" + str(team.seed) + ")  " + team.name)
            else:
                print("(" + str(team.seed) + ") " + team.name)
        print("------------------------------------------------------------")
        print("")


class Matchup:
    # this is the class that represents a matchup, which gets placed into an array within the region class
    def __init__(self, team1, team2, reg_round, matchup_index):
        self.top_team = team1  # the team on the top of the bracket
        self.bottom_team = team2  # the team on the bottom of the bracket
        self.winner = self.compute_winner()  # produce a winning Team
        self.round_num = reg_round  # the round the matchup is located at (64 = round of 64, .., 4 = Final Four, etc.)
        self.index = matchup_index

    def compute_winner(self):
        return self.top_team

    def get_odds_basic(self):
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

        if self.round_num == 64:
            # use hardcoded odds
            if self.top_team.seed == 1:
                return 0.995
            elif self.top_team.seed == 2:
                return 0.98
            elif self.top_team.seed == 3:
                return 0.93
            elif self.top_team.seed == 4:
                return 0.85
            elif self.top_team.seed == 5:
                return 12 / 17
            elif self.top_team.seed == 6:
                return 11 / 17
            elif self.top_team.seed == 7:
                return 10 / 17
            elif self.top_team.seed == 8:
                return 9 / 17
            else:
                return bool(0)
        else:
            return self.bottom_team.seed / (self.top_team.seed + self.bottom_team.seed)

    def winner_print(self):
        # produce a winning team for the matchup and assign to winner Team object
        rand_outcome = random.random()  # random variable to produce the outcome
        top_odds = self.get_odds_basic()  # retrieve odds from the get odds function

        if rand_outcome <= top_odds:
            winner = self.top_team
        else:
            winner = self.bottom_team

        print("---------------------------------------------")
        print("Matchup is between", self.top_team.name, "and", self.bottom_team.name + ".")
        print(self.top_team.name, "has a", str(round(top_odds * 100, 2)) + "% chance of winning.")
        print(winner.name, "advances. (", round(rand_outcome, 3), ")")
        print("---------------------------------------------")
        print("")

        return winner


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
    region_name_list = ("east", "midwest", "south", "west")
    region_list = []

    for region_name in region_name_list:
        region_list.append(read_seed_file(runyear, region_name))

    for reg in region_list:
        reg.print_teams()
