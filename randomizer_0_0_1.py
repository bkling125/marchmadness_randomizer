import random


def read_seed_file(run_year, region):
    # reads the file with the seed information (tab delimited as seed#    team_name)
    # and produces a list of teams

    # open the file

    # two directories depending on what machine i'm working on
    # directory = "F:/Github/marchmadness_randomizer/"
    directory = "C:/Users/bkling/Documents/GitHub/marchmadness_randomizer/"
    file_path = directory + run_year + '_' + region + '_' + 'teams.txt'
    f = open(file_path)

    # initialize the Region class
    return_region = Region(region)

    # there are always 16 teams in a single region
    for i in range(16):
        line_output = f.readline()
        seed, team = line_output.strip().split("\t")
        return_region.append_team(Team(team, seed, return_region.name))

    return_region.compute_region_results()

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
        self.region_winner = None  # Team variable
        self.teams = []  # array of teams
        self.name = name  # name of the region (eg. Midwest)
        self.ro64_matchups = []  # Array of Teams
        self.ro32_matchups = []  # Array of Teams
        self.ro16_matchups = []  # Array of Teams
        self.ro8_matchups = []  # Array of Teams

    def compute_region_results(self):
        self.matchup_builder(64)
        self.matchup_builder(32)
        self.matchup_builder(16)
        self.matchup_builder(8)
        self.region_winner = self.ro8_matchups[0].winner  # Team variable

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

    def print_region_outcome(self, round_number):
        print(self.name, "matchups: Round of", round_number)
        print("-------------------------------- ")

        if round_number == 64:
            for matchup in self.ro64_matchups:
                # "Outcome: 0.xxx: (1) Team1 advances to the Round of 32"
                print("Outcome: " + str(round(matchup.rand_outcome, 3)) + ": (" + str(matchup.winner.seed) + ") " +
                      matchup.winner.name + " advances to the Round of 32")

        if round_number == 32:
            for matchup in self.ro32_matchups:
                # "Outcome: 0.xxx: (1) Team1 advances to the Sweet Sixteen"
                print("Outcome: " + str(round(matchup.rand_outcome, 3)) + ": (" + str(matchup.winner.seed) + ") " +
                      matchup.winner.name + " advances to the Sweet Sixteen")

        if round_number == 16:
            for matchup in self.ro16_matchups:
                # "Outcome: 0.xxx: (1) Team1 advances to the Elite Eight"
                print("Outcome: " + str(round(matchup.rand_outcome, 3)) + ": (" + str(matchup.winner.seed) + ") " +
                      matchup.winner.name + " advances to the Elite Eight")

        if round_number == 8:
            for matchup in self.ro8_matchups:
                # "Outcome: 0.xxx: (1) Team1 advances to the Final Four"
                print("Outcome: " + str(round(matchup.rand_outcome, 3)) + ": (" + str(matchup.winner.seed) + ") " +
                      matchup.winner.name + " advances to the Final Four")

        print("")

    def matchup_builder(self, round_number):
        # handling for Round of 64
        if round_number == 64:
            # here we have 8 total Matchups to create, with fixed seeds making up each Matchup
            for i in range(8):
                if i == 0:
                    t1_seed = 1
                    t2_seed = 16
                elif i == 1:
                    t1_seed = 8
                    t2_seed = 9
                elif i == 2:
                    t1_seed = 5
                    t2_seed = 12
                elif i == 3:
                    t1_seed = 4
                    t2_seed = 13
                elif i == 4:
                    t1_seed = 6
                    t2_seed = 11
                elif i == 5:
                    t1_seed = 3
                    t2_seed = 14
                elif i == 6:
                    t1_seed = 7
                    t2_seed = 10
                else:
                    t1_seed = 2
                    t2_seed = 15
                self.ro64_matchups.append(
                    Matchup(self.teams[t1_seed - 1], self.teams[t2_seed - 1], round_number, i))

        # handling for Round of 32
        elif round_number == 32:
            # here we have 4 total Matchups to create, building off of the winners from the Round of 64
            for i in range(4):
                # i = 0 want 64[0] and 64[1]
                # i = 1 want 64[2] and 64[3]
                # i = 2 want 64[4] and 64[5]
                # i = 3 want 64[6] and 64[7]
                # GENERAL: Given i, want 64[i*2] and 64[i*2+1]
                self.ro32_matchups.append(
                    Matchup(self.ro64_matchups[i * 2].winner, self.ro64_matchups[i * 2 + 1].winner, round_number,
                            i))

        # handling for Sweet 16
        elif round_number == 16:
            # here we have 2 total Matchups to create, building off of the winners from the Round of 32
            for i in range(2):
                self.ro16_matchups.append(
                    Matchup(self.ro32_matchups[i * 2].winner, self.ro32_matchups[i * 2 + 1].winner, round_number,
                            i - 1))

        # handling for Elite 8
        elif round_number == 8:
            # here we have 1 total Matchup to create, building off of the winners from the Sweet 16
            self.ro8_matchups.append(
                Matchup(self.ro16_matchups[0].winner, self.ro16_matchups[1].winner, round_number, 0))


class Matchup:
    # this is the class that represents a matchup, which gets placed into an array within the region class
    def __init__(self, team1, team2, reg_round, matchup_index):
        self.top_team = team1  # the team on the top of the bracket
        self.bottom_team = team2  # the team on the bottom of the bracket
        self.round_num = reg_round  # the round the matchup is located at (64 = round of 64, .., 4 = Final Four, etc.)
        self.index = matchup_index
        self.rand_outcome = random.random()  # random variable to produce the outcome
        self.winner = self.winner_print()  # produce a winning Team

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
        top_odds = self.get_odds_basic()  # retrieve odds from the get odds function

        if self.rand_outcome <= top_odds:
            winner = self.top_team
        else:
            winner = self.bottom_team

        print("---------------------------------------------")
        print("Matchup is between", self.top_team.name, "and", self.bottom_team.name + ".")
        print(self.top_team.name, "has a", str(round(top_odds * 100, 2)) + "% chance of winning.")
        print(winner.name, "advances. (", round(self.rand_outcome, 3), ")")
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
        # reg.print_teams()
        reg.print_region_outcome(64)
        reg.print_region_outcome(32)
        reg.print_region_outcome(16)
        reg.print_region_outcome(8)
