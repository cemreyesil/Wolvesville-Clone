import random

class Player:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.is_alive = True
        self.votes_taken = 0 # The # of votes that the player got
        self.vote_given = False # If player is already voted or not

    def vote(self):
        vote_given = True
    
    def get_vote(self):
        votes_taken =+ 1

class Game:
    def __init__(self):
        self.players = []
        self.day_count = 1
        self.current_day = False # False == Night, True == Daytime

    def init_players(self):
        roles = ["Werewolf"] * 4 + ["Villager"] * 12
        random.shuffle(roles)
        self.players = [Player(f"Player {i+1}", role) for i, role in enumerate(roles)]
        # Print out player details for debugging purposes
        for player in self.players:
            print(player.name, player.role, player.is_alive)

    def get_players(self):
        return self.players.name, self.players.role, self.players.is_alive
    
    def get_votes(self, voting_player_index, voted_player_index):
        if self.players[voting_player_index].vote_given == False:
            if self.players[voting_player_index].role == "Werewolf" and self.players[voted_player_index].role == "Werewolf":
                return False # Werewolf can't vote for another werewolf
            self.players[voting_player_index].vote()
            self.players[voted_player_index].get_vote()
            print(self.players[voting_player_index].vote_given, self.players[voted_player_index].votes_taken)
            return True
        else:
            return False
        

# Initial setup to test game logic
if __name__ == "__main__":
    game = Game()
