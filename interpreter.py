import re

#The interpreter class parses the board model and simulates a game
class Interpreter:
    #initialize board object
    def __init__(self, model):
        self.board = model
        self.players = model.players
        self.tiles = {tile.position: tile for tile in model.tiles}
        self.die = model.die[0]
        self.cards = model.cards
        self.chance_deck, self.chest_deck = self._split_cards()
        self.turn = 0

    # Set up the chance and community chest decks
    def _split_cards(self):
        chance = [c for c in self.cards if 'chance' in c.name]
        chest = [c for c in self.cards if 'community_chest' in c.name]
        return chance, chest
    
    # Roll the dice and return the total value
    def roll_dice(self):
        import random
        return sum(random.choice(self.die.sideValues) for _ in range(self.die.amount))

    # Move the player based on the roll value
    def move_player(self, player, roll):
        old_pos = player.position
        new_pos = (old_pos + roll - 1) % self.board.size + 1
        player.position = new_pos
        print(f"{player.name} rolls {roll} and moves from {old_pos} to {new_pos}")
        self.handle_tile(player, self.tiles[new_pos])

    #function to handle the tile the player lands on
    #takes the player and the tile as arguments and applies the tile's actions
    def handle_tile(self, player, tile):
        print(f"{player.name} lands on tile: {tile.text}")
        if hasattr(tile.type, 'actions'):
            for action in tile.type.actions:
                if "draw_card" in action.name:
                    if "Community_Chest" in tile.name:
                        self.draw_card(player, self.chest_deck)
                    elif "Chance" in tile.name:
                        self.draw_card(player, self.chance_deck)
                elif "pay_tax" in action.name:
                    amount = self.parse_money(action.description)
                    player.score -= amount
                    print(f"{player.name} pays ${amount} in tax")
                elif "go_to_jail" in action.name:
                    player.position = 11  # Jail tile
                    print(f"{player.name} is sent to jail!")
        
        if hasattr(tile.type, 'attributes'):
            property_name = tile.name
            rent = 0
            cost = 0
            for attr in tile.type.attributes:
                if attr.name == "rent":
                    rent = int(attr.value)
                elif attr.name == "cost":
                    cost = int(attr.value)

            # Check if property is already owned
            owner = self.find_property_owner(property_name)
            if owner is None:
                # Buy property
                if cost > 0:
                    player.score -= cost
                    if not hasattr(player, 'inventory') or player.inventory == "null":
                        player.inventory = []
                    player.inventory.append(property_name)
                    print(f"{player.name} buys {property_name} for ${cost}")
            elif owner.name != player.name:
                # Pay rent to the owner
                player.score -= rent
                owner.score += rent
                print(f"{player.name} pays ${rent} rent to {owner.name}")
            
    #function to draw a card from the deck
    #takes the player and the deck as arguments and draws from appropriate deck
    def draw_card(self, player, deck):
        from random import shuffle
        shuffle(deck)
        card = deck.pop(0)
        deck.append(card)
        print(f"{player.name} draws a card: {card.type.effect}")
        self.apply_card_effect(player, card)

    #function to apply the card effect
    #takes the player and the card as arguments and applies the card's effect
    #card effect can be collecting money, paying money, going to jail, going back, or advancing to go
    def apply_card_effect(self, player, card):
        text = card.type.effect
        if "Collect" in text:
            amt = self.parse_money(text)
            player.score += amt
            print(f"{player.name} collects ${amt}")
        elif "Pay" in text:
            amt = self.parse_money(text)
            player.score -= amt
            print(f"{player.name} pays ${amt}")
        elif "Go to Jail" in text:
            player.position = 11
            print(f"{player.name} is sent to Jail.")
        elif "Advance to Go" in text:
            player.position = 1
            player.score += 200
            print(f"{player.name} advances to Go and collects $200.")
        elif "Go Back" in text:
            steps = self.parse_number(text)
            player.position = (player.position - steps - 1) % self.board.size + 1
            print(f"{player.name} moves back {steps} spaces to {player.position}")

    def parse_money(self, text):
        match = re.search(r"\$([0-9]+)", text)
        return int(match.group(1)) if match else 0

    def parse_number(self, text):
        match = re.search(r"(\d+)", text)
        return int(match.group(1)) if match else 0
    
    def find_property_owner(self, property_name):
        for p in self.players:
            if hasattr(p, 'inventory') and p.inventory and property_name in p.inventory:
                return p
        return None
    
    def run(self, rounds=20):
        for _ in range(rounds):
            current_player = self.players[self.turn % len(self.players)]
            print(f"{current_player.name}'s turn")
            print(f"{current_player.name} has ${current_player.score}")
            roll = self.roll_dice()
            self.move_player(current_player, roll)
            print(f"Score: {current_player.name} has ${current_player.score}\n")
            self.turn += 1t_player.score}\n")
            self.turn += 1

