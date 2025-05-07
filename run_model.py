from textx import metamodel_from_file
from interpreter import Interpreter


def validate_board_length(m):
    if hasattr(m, 'tiles'):
        tile_count = len(m.tiles)
    else:
        tile_count = 0

    if m.size != tile_count:
        raise ValueError(
            f"Board '{m.name}' declared length {m.size}, "
            f"but {tile_count} tiles were defined."
        )

# Load the grammar
mm = metamodel_from_file('grammar.tx')

# Parse the model
model = mm.model_from_file('monopoly.board')

validate_board_length(model)

game = Interpreter(model)
game.run(rounds=30)


# print(f"Board: {model.name}")
# print(f"Length: {model.size}")

# print("\nPlayers:")
# for player in model.players:
#     print(f"Player: {player.name}")
#     print(f"  Color: {player.color}")
#     print(f"  Position: {player.position}")

# print("\nDice:")
# for die in model.die:
#     print(f"Die: {die.name}")
#     print(f"  Sides: {die.sides}")
#     print(f"  SideValues: {die.sideValues}")
#     print(f"  Amount: {die.amount}")

# print("\nTiles:")
# for tile in model.tiles:
#     print(f"  - {tile.name}")
#     print(f"    Type: {tile.type.__class__.__name__} ({tile.type.name})")
#     print(f"    Position: {tile.position}")
#     print(f"    Color: {tile.color}")
#     print(f"    Text: {tile.text}")

#     if hasattr(tile.type, 'attributes') and tile.type.attributes:
#         print(f"    Attributes:")
#         for attr in tile.type.attributes:
#             print(f"      {attr.name} = {attr.value}")
#     if hasattr(tile.type, 'actions') and tile.type.actions:
#         print(f"    Actions:")
#         for action in tile.type.actions:
#             print(f"      Action: {action.name}")
#             if hasattr(action, 'description') and action.description:
#                 print(f"        Description: {action.description}")
#             if hasattr(action, 'effect') and action.effect:
#                 print(f"        Effect: {action.effect}")

# print("\nCards:")
# for card in model.cards:
#     print(f"Card: {card.name}")
#     print(f"  Name: {card.type.name}")
#     print(f"  Effect: {card.type.effect}")
#     print(f"  Description: {card.type.description}")

