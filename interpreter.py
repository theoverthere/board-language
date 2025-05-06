class Interpreter:
    def __init__(self, model):
        self.board = model
        self.players = model.players
        self.tiles = {tile.position: tile for tile in model.tiles}
        self.die = model.die[0]
        self.cards = model.cards
        self.chance_deck, self.chest_deck = self._split_cards()
        self.turn = 0

    def _split_cards(self):
        chance = [c for c in self.cards if 'chance' in c.name]
        chest = [c for c in self.cards if 'community_chest' in c.name]
        return chance, chest
    
    def roll_dice(self):
        import random
        return sum(random.choice(self.die.sideValues) for _ in range(self.die.amount))

    def move_player(self, player, roll):
        old_pos = player.position
        new_pos = (old_pos + roll - 1) % self.board.size + 1
        player.position = new_pos
        print(f"{player.name} rolls {roll} and moves from {old_pos} to {new_pos}")
        self.handle_tile(player, self.tiles[new_pos])

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

    def draw_card(self, player, deck):
        from random import shuffle
        shuffle(deck)
        card = deck.pop(0)
        deck.append(card)
        print(f"{player.name} draws a card: {card.type.effect}")
        self.apply_card_effect(player, card)

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
        import re
        match = re.search(r"\$([0-9]+)", text)
        return int(match.group(1)) if match else 0

    def parse_number(self, text):
        import re
        match = re.search(r"(\d+)", text)
        return int(match.group(1)) if match else 0
    
    def run(self, rounds=20):
        for _ in range(rounds):
            current_player = self.players[self.turn % len(self.players)]
            roll = self.roll_dice()
            self.move_player(current_player, roll)
            print(f"Score: {current_player.name} has ${current_player.score}\n")
            self.turn += 1

