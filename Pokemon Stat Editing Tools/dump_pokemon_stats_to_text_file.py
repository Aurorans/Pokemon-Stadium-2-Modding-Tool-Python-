import os
import re
import sys

# 1. Define your base project root (Up one level from the script)
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up to the parent folder
project_root = os.path.dirname(script_dir)

# Define tracking files based on your workspace setup

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

if not ROM_INPUT:
    print("Could not find 'baserom.z64' in the parent or its subfolders.")
    print("Please make sure the file exists and try again.")
    sys.exit(1)  # Stops the script safely right here

# 4. Set the variable ROM_OUTPUT to the directory pathname with baserom_modified.z64 (the output file)

# 5. Search downward for the file and save it to a variable
ID_MAP_FILE = None

# 6. Use os.walk to search downward through the directories
for root, dirs, files in os.walk(project_root):
    for f in files:
        if f.lower() == 'pokemon_master_id_map.txt':
            ID_MAP_FILE = os.path.join(root, f)
            break
    if ID_MAP_FILE:
        break  # Stop searching once found
		
# 7. Search downward for the file and save it to a variable
TYPES_FILE = None

# 8. Use os.walk to search downward through the directories
for root, dirs, files in os.walk(project_root):
    for f in files:
        if f.lower() == 'types_list.txt':
            TYPES_FILE = os.path.join(root, f)
            break
    if TYPES_FILE:
        break  # Stop searching once found

# 9. Define the folder path variable you want to ensure exists
target_dir = os.path.join(project_root, 'Editing')

# 10. Create the folder safely if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

os.chdir(target_dir)

OUTPUT_FILE = "pokemon_stadium_2_stat_sheet.txt"

def load_type_map(type_path):
    """Parses types_list.txt into a clean dictionary lookup."""
    type_map = {}
    if not os.path.exists(type_path):
        print(f"Warning: '{type_path}' not found. Defaulting to raw hex IDs.")
        return type_map
    with open(type_path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                hex_key, label = line.strip().split(":", 1)
                try:
                    type_map[int(hex_key.strip(), 16)] = label.strip()
                except ValueError:
                    continue
    return type_map

def parse_pokedex_id_map(map_path):
    """Reads the generated text map and extracts (Hex Offset, Name)."""
    ordered_pokemon = []
    if not os.path.exists(map_path):
        print(f"Error: Required master map file '{map_path}' missing. Please generate it first.")
        return []
    
    # Pattern to pull out the Offset and Pokedex name from: "0X98F20: 0xE2 - Bulbasaur"
    line_pattern = re.compile(r"^(0X[0-9A-F]+):\s*0x[0-9A-F]+\s*-\s*(.+)$")
    
    with open(map_path, "r", encoding="utf-8") as f:
        for line in f:
            match = line_pattern.match(line.strip())
            if match:
                offset_str, pkmn_name = match.groups()
                ordered_pokemon.append((int(offset_str, 16), pkmn_name.strip()))
    return ordered_pokemon

def run_clean_master_dump():
    if not os.path.exists(ROM_INPUT):
        print(f"Error: ROM file '{ROM_INPUT}' not found in working directory.")
        return

    type_map = load_type_map(TYPES_FILE)
    pokemon_list = parse_pokedex_id_map(ID_MAP_FILE)

    if not pokemon_list:
        return

    compiled_sheet = []
    print(f"Dumping stats directly from physical structural coordinates...")

    with open(ROM_INPUT, "rb") as rom_f:
        for base_offset, name in pokemon_list:
            # Stats begin exactly 1 byte inside the 22-byte block, right behind the ID byte
            rom_f.seek(base_offset + 1)
            raw_data = rom_f.read(8) # Read 6 stats + 2 types back-to-back
            
            if len(raw_data) < 8:
                continue

            hp, atk, df, spe, spa, spd, t1_id, t2_id = list(raw_data)

            # Resolve types via string conversion maps
            t1_name = type_map.get(t1_id, f"Unknown_Type_{hex(t1_id)}")
            t2_name = type_map.get(t2_id, f"Unknown_Type_{hex(t2_id)}") if t1_id != t2_id else "None"

            # Structure exactly as requested
            formatted_block = (
                f"# TARGET_ROM_OFFSET: {hex(base_offset).upper()}\n"
                f"SPECIES_ID: {name}\n"
                f"BASE_HP: {hp}\n"
                f"BASE_ATTACK: {atk}\n"
                f"BASE_DEFENSE: {df}\n"
                f"BASE_SPEED: {spe}\n"
                f"BASE_SPECIAL_ATTACK: {spa}\n"
                f"BASE_SPECIAL_DEFENSE: {spd}\n"
                f"TYPE_1: {t1_name}\n"
                f"TYPE_2: {t2_name}"
            )
            compiled_sheet.append(formatted_block)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        out_f.write("\n\n".join(compiled_sheet) + "\n")
    print(f"[Success] Pristine master stat sheet dumped cleanly to: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_clean_master_dump()