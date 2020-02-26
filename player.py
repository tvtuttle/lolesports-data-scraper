# contains classes for use in other files
# before, players (fantasy and real) were represented by lists; by using defined objects instead, will be more
# readable and agile

class LolPlayer:

    def __init__(self, name, k, d, a, cs, pos):
        self.name = name
        self.k = k
        self.d = d
        self.a = a
        self.cs = cs
        self.pos = pos

    def get_score(self):
        score = 2*self.k - 0.5*self.d + 1.5*self.a + 0.01*self.cs
        return round(score, 2)


class LolTeam:

    def __init__(self, name, wins, towers, barons, dragons, heralds, fastwins):
        self.name = name
        self.wins = wins
        self.towers = towers
        self.barons = barons
        self.dragons = dragons
        self.heralds = heralds
        self.fastwins = fastwins

    def get_score(self):
        score = 2*self.wins + self.towers + 2*self.barons + self.dragons + 2*self.heralds + 2*self.fastwins
        return round(score, 2)


class FanTeam:
    def __init__(self, name, color, team=None):
        self.name = name
        self.color = color
        self.team = team
        self.players = list()
        self.starters = dict()
        self.subs = list()

    def add_player(self, player):
        self.players.append(player)

    def manage_roster(self):
        # sort players into starters and subs
        for player in self.players:
            # print(player.name)
            # print(player.pos)
            if player.pos not in self.starters and player.pos > -1:
                self.starters[player.pos] = player
            elif player.pos in self.starters and player.get_score() > self.starters[player.pos].get_score():
                self.subs.append(self.starters[player.pos])
                self.starters[player.pos] = player
            else:
                self.subs.append(player)

    def get_score(self):
        # requires manage_roster to have been called earlier, for subs and starters to be filled correctly
        score = self.team.get_score()
        for p in self.starters:
            score += self.starters[p].get_score()
        return score


