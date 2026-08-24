import os
import struct

# 1. Define your base project root (Up one level from the script)
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up to the parent folder
project_root = os.path.dirname(script_dir)

ROM_INPUT = None

# 3. Use os.walk to search downward through the directories
###. Search downward using a case-insensitive check
for root, dirs, files in os.walk(project_root):
    for f in files:
        if f.lower() == 'baserom.z64':
            ROM_INPUT = os.path.join(root, f)
            break
    if ROM_INPUT:
        break  # Stop searching once found

# 4. Define the folder path variable you want to ensure exists
target_dir = os.path.join(project_root, 'Helpers')

# 5. Create the folder safely if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

os.chdir(target_dir)
        

OUTPUT_MAP_FILE = "pokemon_master_id_map.txt"

# Definitive Master Table Coordinates
START_OFFSET = 0x98F20
STRIDE_SIZE = 22
TOTAL_POKEMON = 251

# Clean, sequential 1-251 National Pokedex Order List
NATIONAL_POKEDEX_ORDER = [
    "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard",
    "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree",
    "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata",
    "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu",
    "Sandshrew", "Sandslash", "Nidoran Female", "Nidorina", "Nidoqueen", "Nidoran Male",
    "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales",
    "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume",
    "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth",
    "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine",
    "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop",
    "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool",
    "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke",
    "Slowbro", "Magnemite", "Magneton", "Farfetch'd", "Doduo", "Dodrio", "Seel",
    "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter",
    "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb",
    "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee",
    "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey",
    "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu",
    "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir",
    "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon",
    "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops",
    "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair",
    "Dragonite", "Mewtwo", "Mew", "Chikorita", "Bayleef", "Meganium", "Cyndaquil",
    "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret",
    "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados",
    "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi",
    "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom",
    "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff",
    "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon",
    "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig",
    "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull",
    "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring",
    "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery",
    "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy",
    "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum",
    "Elekid", "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune",
    "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-Oh", "Celebi"
]

def build_pure_id_map():
    if not os.path.exists(ROM_INPUT):
        print(f"Error: ROM file '{ROM_INPUT}' not found.")
        return

    output_lines = []
    print("Extracting raw table IDs into sequential National Pokedex ordered sheet...")

    with open(ROM_INPUT, "rb") as f:
        for idx in range(TOTAL_POKEMON):
            # Calculate linear absolute step address boundary location
            target_addr = START_OFFSET + (idx * STRIDE_SIZE)
            f.seek(target_addr)
            
            # Read only byte +00 (rr) to retrieve the raw assigned value
            raw_id_byte = f.read(1)
            if not raw_id_byte:
                break
                
            internal_id_int = int(raw_id_byte[0])
            
            # Align the current file record to our sequential pokedex name row
            pokedex_name = NATIONAL_POKEDEX_ORDER[idx]
            
            # Output format layout: Hex Offset -> Raw ID (Hex Format) -> Pokemon Name
            formatted_entry = f"{hex(target_addr).upper()}: 0x{internal_id_int:02X} - {pokedex_name}"
            output_lines.append(formatted_entry)

    # Output text profile configuration to file
    with open(OUTPUT_MAP_FILE, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(output_lines) + "\n")

    print(f"[Success] Raw mapping blueprint exported cleanly to: {OUTPUT_MAP_FILE}")

if __name__ == "__main__":
    build_pokedex_map_fixed = build_pure_id_map
    build_pokedex_map_fixed()