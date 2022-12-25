import requests
import random
import time
from PIL import Image
from io import BytesIO

# Constants for API endpoints and image folder
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"
POKEMON_ENDPOINT = "pokemon/{id}"
SPRITES_ENDPOINT = 'pokemon/{id}/'
IMAGE_FOLDER = "pokemon-images"

POKEMON_TYPE_CHART = {
    "normal": {
        "super_effective": ["rock"],
        "not_very_effective": ["steel"],
        "ineffective": []
        },
    "fire": {
        "super_effective": ["grass", "ice", "bug", "steel"],
        "not_very_effective": ["rock", "fire", "water", "dragon"],
        "ineffective": []
    },
    "water": {
        "super_effective": ["fire", "ground", "rock"],
        "not_very_effective": ["water", "grass", "dragon"],
        "ineffective": []
        },
    "electric": {
        "super_effective": ["water", "flying"],
        "not_very_effective": ["electric", "grass", "dragon"],
        "ineffective": ["ground"]
        },
    "grass": {
        "super_effective": ["water", "ground", "rock"],
        "not_very_effective": ["fire", "grass", "poison", "flying", "bug", "dragon", "steel"],
        "ineffective": []
        },
    "ice": {
        "super_effective": ["grass", "ground", "flying", "dragon"],
        "not_very_effective": ["steel", "fire", "water", "ice"],
        "ineffective": []
        },
    "fighting": {
        "super_effective": ["normal", "rock", "steel", "ice"],
        "not_very_effective": ["flying", "poison", "bug", "psychic", "fairy"],
        "ineffective": ["ghost"]
        }, 
    "poison": {
        "super_effective": ["grass"],
        "not_very_effective": ["poison", "rock", "ghost", "steel"],
        "ineffective": ["ground", "psychic"]
        },
    "ground": {
        "super_effective": ["fire", "electric", "poison", "rock", "steel"],
        "not_very_effective": ["grass", "bug"],
        "ineffective": ["flying"]
        },
    "flying": {
        "super_effective": ["fighting", "bug", "grass"],
        "not_very_effective": ["rock", "steel"],
        "ineffective": ["electric"]
        },
    "psychic": {
        "super_effective": ["fighting", "poison"],
        "not_very_effective": ["steel", "psychic"],
        "ineffective": ["dark"]
        },
    "bug": {
        "super_effective": ["grass", "psychic", "dark"],
        "not_very_effective": ["fighting", "flying", "poison", "ghost", "steel", "fire", "fairy"],
        "ineffective": []
        },
    "rock": {
        "super_effective": ["fire", "ice", "flying", "bug"],
        "not_very_effective": ["fighting", "ground", "steel"],
        "ineffective": []
        },
    "ghost": {
        "super_effective": ["psychic", "ghost"],
        "not_very_effective": ["dark"],
        "ineffective": ["normal"]
        }, 
    "dragon": {
        "super_effective": ["dragon"],
        "not_very_effective": ["steel"],
        "ineffective": ["fairy"]
        },
    "dark": {
        "super_effective": ["psychic", "ghost"],
        "not_very_effective": ["dark", "fighting", "fairy"],
        "ineffective": []
        },
    "steel": {
        "super_effective": ["rock", "ice", "fairy"],
        "not_very_effective": ["steel", "fire", "water", "electric"],
        "ineffective": []
        },
    "fairy": {
        "super_effective": ["fighting", "dragon", "dark"],
        "not_very_effective": ["poison", "steel"],
        "ineffective": []
        },
    }

class Pokemon:
    def __init__(self, name, stats, sprite_path, move_set, number, types):
        self.name = name.capitalize()
        self.stats = stats
        self.sprite_path = sprite_path
        self.move_set = move_set
        self.number = number
        self.types = types
        self.pp_cost = 1
        self.fainted = False
        self.health = int(stats['hp'])
        self.max_health = int(stats['hp'])
        self.level = 1
        
    def __str__(self):
        stat_str = "\n".join([f"  {k}: {v}" for k, v in self.stats.items()])
        
        move_set_str = "\n".join([f"  {move['name']} ({move['pp']}): Type: {move['type']}, Damage: {move['damage']}, Effect: {move['effect']}" for move in self.move_set])
        
        return f"Name: {self.name}\nNumber: {self.number}\nTypes: {self.types}\nStats:\n{stat_str}\nMove Set:\n{move_set_str}\n"
    
    def basic_show(self):
        image = Image.open(self.sprite_path)
        image.show()
        return ''
    
    def apply_damage(self, dmg):
        self.health = self.health - dmg
    
    def consume_pp(self,move_id):
        if self.move_set[move_id] != 0:
            self.move_set[move_id]['pp'] -= 1
        else:
            raise "Inssuficent PP"
        
    def is_alive(self):
        if self.health < 0:
            self.fainted = True
            print(self.name, "fainted!")

def get_pokemon_data(pokemon_id):
    """Fetches data for the specified pokemon from the PokeAPI"""
    # Construct the full URL for the pokemon endpoint
    pokemon_url = POKEAPI_BASE_URL + POKEMON_ENDPOINT.format(id=pokemon_id)
    # Send a GET request to the pokemon endpoint
    response = requests.get(pokemon_url)
    # Return the API response as a dictionary
    return response.json()

def get_random_pokemon_id():
    pokemonListLen = list(range(1, 1001))
    return random.choice(pokemonListLen)

def get_pokemon_image(pokemon_id):
  # Construct the full URL for the sprites endpoint
  sprites_url = POKEAPI_BASE_URL + SPRITES_ENDPOINT.format(id=pokemon_id)
  
  # Send a GET request to the sprites endpoint
  response = requests.get(sprites_url)
  # Get the sprite URL from the response
  sprite_url = response.json()['sprites']['front_default']
  
  # Send a GET request to the sprite URL
  response = requests.get(sprite_url)
  # Return the image data
  return Image.open(BytesIO(response.content))

def save_pokemon_image(pokemon_id, image_folder):
    """Saves the image for the specified pokemon to the specified folder"""
    # Fetch the pokemon image
    image = get_pokemon_image(pokemon_id)
    # Save the image to the specified folder
    image.save(f"{image_folder}/{pokemon_id}.png")

def create_pokemon(pokemon_id):
    """Displays the image and stats for the specified pokemon"""
    # Fetch the pokemon data
    pokemon_data = get_pokemon_data(pokemon_id)
    # Extract the pokemon name, stats, move set, and number from the data
    name = pokemon_data["name"]
    stats = pokemon_data['stats']
    types = pokemon_data['types']
    types_list = [item['type']['name'] for item in types]
    stats_dict = {stat['stat']['name']: stat['base_stat'] for stat in stats}
    move_set = pokemon_data["moves"]
    # Choose the first 4 moves from the move set
    moves = []
    i = 0
    for move in move_set[:4]:
        # Get the move data from the API
        move_data = requests.get(move["move"]["url"]).json()
        # Extract the move name, type, and effect
        move_name = move_data["name"]
        move_type = move_data["type"]["name"]
        move_damage = move_data["power"] if move_data["power"] else "N/A"
        move_effect = move_data["effect_entries"][0]["short_effect"]
        move_effect_chance = move_data["effect_chance"]
        move_hit_chance = move_data["accuracy"]
        move_pp = move_data["pp"]
        # Create a move dict with the extracted data
        move_dict = {"name": move_name, "type": move_type, "damage": move_damage, "effect": move_effect, "effect_chance" : move_effect_chance, "accuracy" : move_hit_chance ,"pp" : move_pp, "move" : i }
        # Append the move dict to the moves list
        moves.append(move_dict)
        i = 1+1
    number = pokemon_data["id"]
    # Create a Pokemon object
    pokemon = Pokemon(name, stats_dict, f"{IMAGE_FOLDER}/{pokemon_id}.png", moves, number, types_list)
    # Return the Pokemon object
    save_pokemon_image(pokemon_id, IMAGE_FOLDER)
        
    return pokemon


class Engine:
    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.turn = 0

    def calculate_hit_chance(self, move):
        """Calculates the hit chance of the given move based on the accuracy and evasion stats of the attacking and defending pokemon"""
        # Get the accuracy and evasion stats of the attacking and defending pokemon
        accuracy = move['accuracy'] if move['accuracy'] is not None and not 0 else 100
        return (accuracy * 100) >= random.randint(1, 100)
        
    def choose_move(self, pokemon):
        """Prompts the player to choose a move to use"""
        # Print the available moves
        print("Available moves:")
        for i, move in enumerate(pokemon.move_set):
            print(f"{i+1}. {move['name']}")
            # Get the move index from the player
        move_index = int(input("Enter the number of the move to use: "))-1
        # Return the move at the specified index
        return {"id": move_index, "move": pokemon.move_set[move_index]['name'], "dmg" : pokemon.move_set[move_index]['damage'], "accuracy" : pokemon.move_set[move_index]['accuracy']}
    
    def choose_move_ia(self, pokemon):
        """Prompts the player to choose a move to use"""
        move_index = random.randint(0,3)
        # Return the move at the specified index
        return {"id": move_index, "move": pokemon.move_set[move_index]['name'], "dmg" : pokemon.move_set[move_index]['damage'], "accuracy" : pokemon.move_set[move_index]['accuracy'], "type" : pokemon.move_set[move_index]["type"]}
        
    def calculate_damage_old(self, pokemon, move, enemy):
        movedmg = int(move["dmg"]) if move["dmg"] != "N/A" else 0
        dmg = int((int(pokemon.stats['attack']) - int(enemy.stats['defense']) + movedmg)/10)
        pokemon.apply_damage(dmg)
        print(f"Move {move['move']} inflicted {dmg} damage!")
        pokemon.is_alive()
        return dmg
         
         
    def move_lands_critical_hit(self):
        """Determines if a move lands a critical hit based on its critical hit chance"""
        # Generate a random number between 0 and 1
        random_number = random.uniform(0, 1)
        # If the random number is less than the critical hit chance, the move lands a critical hit
        return random_number < 0.15
         
    def get_type_modifier(self, move_type, pokemon_type):
        for type in pokemon_type:
            if move_type in POKEMON_TYPE_CHART[type]["super_effective"]:
                return 2
            elif move_type in POKEMON_TYPE_CHART[type]["not_very_effective"]:
                return 0.5
            elif move_type in POKEMON_TYPE_CHART[type]["ineffective"]:
                return 0
        return 1 

         
    def calculate_damage(self, attacking_pokemon, move, defending_pokemon):
        movedmg = float(move["dmg"]) if move["dmg"] != "N/A" else 0
        # Get the type modifier for the attack
        type_modifier = self.get_type_modifier(move["type"], defending_pokemon.types)
        # Check if the move lands a critical hit
        critical_hit = self.move_lands_critical_hit()
        # Calculate the damage
        damage = (((((2 * attacking_pokemon.level) / 5) + 2) * movedmg * float(attacking_pokemon.stats["attack"]) / float(defending_pokemon.stats["defense"])) / 50) + 2
        # Apply the type modifier
        damage = damage * type_modifier
        # Apply the critical hit multiplier if applicable
            
        defending_pokemon.apply_damage(damage)
        print(f"Move {move['move']} inflicted {int(damage)} damage!")
        defending_pokemon.is_alive()     
    
    def display_health(self, pokemon):
        BLOCK_LENGTH = 30
        # Calculate the percentage of the pokemon's health remaining
        health_percentage = pokemon.health / pokemon.max_health
        # Calculate the number of full blocks to display
        full_blocks = int(health_percentage * BLOCK_LENGTH)
        # Calculate the number of half blocks to display
        half_blocks = BLOCK_LENGTH - full_blocks
        # Create the health bar string
        health_bar = "█" * full_blocks + "░" * half_blocks
        # Print the health bar and the pokemon's name
        print(f"{pokemon.name} has {int(pokemon.health)} HP: [{health_bar}]")
        
        
    def battle(self, pokemon1, pokemon2):
        # Set the turn order
        turn_order = [pokemon1, pokemon2]
        # Initialize the battle loop
        while not pokemon1.fainted or  not pokemon2.fainted:
            self.display_health(pokemon1)
            self.display_health(pokemon2)
            print('\n')
            self.turn += 1
            print(f"\n--- Turn {self.turn} ---")
            # Iterate through the turn order
            for pokemon in turn_order:
                if pokemon == pokemon1:
                    enemy = pokemon2
                else:
                    enemy = pokemon1
                
                
                #move = self.choose_move(pokemon)
                move = self.choose_move_ia(pokemon)
                pokemon.consume_pp(move["id"])
                print(f"{pokemon.name} used {[move['move']]}!")
                hit = self.calculate_hit_chance(move)
                # Check if the move hit
                if hit:
                    # Calculate the damage dealt
                    damage = self.calculate_damage(pokemon, move, enemy)
                    #print(f"{move['move']} dealt {damage} damage to {enemy.name}!")
                    time.sleep(1)
                # If the move missed, print a message
                else:
                    print(f"{pokemon.name}'s attack missed!")
                
                if pokemon.fainted:
                    print(f"Battle ended. {enemy.name} was the winner!")
                    return
        
        
        
def main():
    # Select and display the first pokemon
    pokemon1_id = get_random_pokemon_id()
    PkMon1 = create_pokemon(pokemon1_id)
    print(PkMon1)
    #print(PkMon1.basic_show())
    # Select and display the second pokemon
    pokemon2_id = get_random_pokemon_id()
    PkMon2 = create_pokemon(pokemon2_id)
    print(PkMon2)
    #print(PkMon2.basic_show())
    
    engine = Engine(PkMon1,PkMon2) 
    engine.battle(engine.pokemon1, engine.pokemon2)

if __name__ == "__main__":
    main()