import logging
import random
from enum import Enum

# Configure main logging to write messages to a file
logging.basicConfig(filename='game_log.txt', level=logging.INFO)

# Separate logger for important actions
action_logger = logging.getLogger('ActionLogger')
action_file_handler = logging.FileHandler('player_actions.txt')
action_logger.addHandler(action_file_handler)
action_logger.setLevel(logging.INFO)

# Enum for game states
class GameState(Enum):
    LOCKED = 0
    KEY_FOUND = 1
    ESCAPED = 2

# Nested dictionaries to represent two layers of actions
layer_actions = {
    "1": {
        "description": "Look at the desk",
        "subactions": {
            "1": "Look under the desk => You found a key!",
            "2": "Look inside the desk drawers => You found an apple!",
            "3": "Check desk compartments => Nothing special here.",
            "0": "Go back"
        }
    },
    "2": {
        "description": "Look at the bookshelf",
        "subactions": {
            "1": "Check behind the bookshelf => Just spiderwebs.",
            "2": "Check above the bookshelf => Nothing but dust.",
            "3": "Rummage through the books => A random note, but it's unreadable.",
            "0": "Go back"
        }
    },
    "3": {
        "description": "Inspect the window",
        "subactions": {
            "1": "Try to open the window => It's locked from the outside.",
            "2": "Wipe the window => You can see a garden outside, but no help.",
            "3": "Tap on the glass => Only a dull thud echoes.",
            "0": "Go back"
        }
    },
    "4": {
        "description": "Open the door (need key to escape)",
        "subactions": {}  
    }
}

# Track game state, inventory, subaction usage counts, and player health
current_state = GameState.LOCKED
inventory = {}
subaction_count = {}
player_health = 100

print("Welcome to the Text Adventure Game!")
print("You must find the hidden key and unlock the door to escape.\n")

while current_state != GameState.ESCAPED:
    # If the player's health reaches 0 or less, end the game
    if player_health <= 0:
        print("Your health dropped to zero. You can’t continue.")
        break

    print("Main Actions:")
    for action_key, action_info in layer_actions.items():
        print(f"{action_key} - {action_info['description']}")
    print("0 - Quit the game")

    user_input = input("Choose an option: ")
    try:
        choice = user_input[:1]

        if choice == "0":
            print("You chose to quit. Goodbye!")
            break

        if choice not in layer_actions.keys():
            raise KeyError("Invalid main action.")

        # If the chosen action is the door
        if choice == "4":
            if inventory.get("key") is True:
                print("You used the key to unlock the door. You've escaped!")
                current_state = GameState.ESCAPED
                break
            else:
                print("The door is locked. You need a key.")
                continue

        sub_dict = layer_actions[choice]["subactions"]

        while True:
            # If we're looking at the desk and we have the key, we can add/enable a secret compartment
            if layer_actions[choice]['description'] == "Look at the desk" and inventory.get("key", False) and "4" not in sub_dict:
                sub_dict["4"] = "Open the secret compartment => You find a hidden message!"

            print(f"\n{layer_actions[choice]['description']} - Subactions:")
            for sub_key, sub_desc in sub_dict.items():
                print(f"{sub_key} - {sub_desc.split('=>')[0]}")
            print("Choose a subaction (0 to go back):")

            sub_input = input()
            sub_choice = sub_input[:1]

            if sub_choice == "0":
                break

            if sub_choice not in sub_dict.keys():
                raise KeyError("Invalid subaction.")

            # Increase usage count for the chosen subaction
            subaction_count[sub_choice] = subaction_count.get(sub_choice, 0) + 1

            # Subaction's outcome
            outcome = sub_dict[sub_choice]
            outcome_text = outcome.split("=>")[1].strip() if "=>" in outcome else outcome
            print(outcome_text)
            
            action_logger.info(f"Player performed subaction '{sub_choice}': {outcome_text}")
            print(f"You have performed this subaction {subaction_count[sub_choice]} times.")

            # Random chance (25%) of finding a worthless item
            chance = random.random()
            if chance < 0.25:
                print("You also stumble upon a strange pebble, but it seems worthless.")

            # Handle health adjustments or other conditional logic
            if "drawers" in outcome.lower() and "sharp" in outcome.lower():
                player_health -= 10
                print(f"Ouch! You cut yourself. Current health: {player_health}")

            if "key" in outcome.lower():
                inventory["key"] = True
                current_state = GameState.KEY_FOUND
                print("The key has been added to your inventory.")
                action_logger.info("Player found the key.")

            if "apple" in outcome.lower():
                inventory["apple"] = True
                player_health = min(player_health + 5, 100)
                print("The apple has been added to your inventory. It might be tasty later!")
                print(f"You feel a bit better. Current health: {player_health}")
                action_logger.info("Player picked up an apple.")

    except KeyError as e:
        logging.error(f"KeyError encountered: {e}")
        print("That choice doesn't seem possible. Try again.")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        print("An unexpected error occurred, but the game continues.")
    finally:
        logging.info("End of main loop iteration.\n")

print("Game over. Thank you for playing!")

print("Created/Modified files:", ["game_log.txt", "player_actions.txt"])