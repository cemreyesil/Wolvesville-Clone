import random

class Player:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.is_alive = True

    def vote(self):
        # Will be done later
        pass

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

# Initial setup to test game logic
if __name__ == "__main__":
    game = Game()
