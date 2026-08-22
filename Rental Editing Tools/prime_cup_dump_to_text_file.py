import os
import sys
import struct

# 1. Define your base project root (Up one level from the script)
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up to the parent folder
project_root = os.path.dirname(script_dir)

ROM_NAME = None

# 3. Use os.walk to search downward through the directories
# 3. Search downward using a case-insensitive check
for root, dirs, files in os.walk(project_root):
    for f in files:
        if f.lower() == 'baserom.z64':
            ROM_NAME = os.path.join(root, f)
            break
    if ROM_NAME:
        break  # Stop searching once found

if not ROM_NAME:
    print("Could not find 'baserom.z64' in the parent or its subfolders.")
    print("Please make sure the file exists and try again.")
    sys.exit(1)  # Stops the script safely right here

# 4. Define the folder path variable you want to ensure exists
target_dir = os.path.join(project_root, 'Editing')

# 5. Create the folder safely if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

os.chdir(target_dir)

# 7. Search downward for the file and save it to a variable
OUTPUT_TXT = "prime_cup_rental_pokemon.txt"

# 9. Search downward for the file and save it to a variable
MOVES_FILE = None

# 10. Use os.walk to search downward through the directories
for root, dirs, files in os.walk(project_root):
    for f in files:
        if f.lower() == 'moves_list.txt':
            MOVES_FILE = os.path.join(root, f)
            break
    if MOVES_FILE:
        break  # Stop searching once found

if not MOVES_FILE:
    print("Could not find 'moves_list.txt' in the parent or its subfolders.")
    print("Please make sure the file exists and try again.")
    sys.exit(1)  # Stops the script safely right here

# 11. Search downward for the file and save it to a variable
SPECIES_FILE = None

# 12. Use os.walk to search downward through the directories
for root, dirs, files in os.walk(project_root):
    for f in files:
        if f.lower() == 'species_list.txt':
            SPECIES_FILE = os.path.join(root, f)
            break
    if SPECIES_FILE:
        break  # Stop searching once found

if not SPECIES_FILE:
    print("Could not find 'species_list.txt' in the parent or its subfolders.")
    print("Please make sure the file exists and try again.")
    sys.exit(1)  # Stops the script safely right here
    

PRIME_CUP_START = 0x1708CB4
POKEMON_SIZE = 0x18
TOTAL_POKEMON = 246

def load_reverse_dictionary(filepath):
    """Maps internal hex IDs back to readable text names for seamless formatting"""
    rev_map = {}
    if not os.path.exists(filepath):
        return rev_map
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if ":" in line and not line.startswith("#"):
                hex_str, name = line.split(":", 1)
                try:
                    int_id = int(hex_str.strip(), 16)
                    rev_map[int_id] = name.strip()
                except ValueError:
                    continue
    return rev_map

def generate_ready_to_edit_config():
    if not os.path.exists(ROM_NAME):
        print(f"Error: Missing base ROM '{ROM_NAME}' in this folder.")
        print("Please make sure your uncompressed ROM is named exactly 'baserom.z64'.")
        return

    # Automatically load dictionaries to convert raw binary codes into plain English text names
    moves_dict = load_reverse_dictionary(MOVES_FILE)
    species_dict = load_reverse_dictionary(SPECIES_FILE)

    with open(ROM_NAME, "rb") as f:
        rom_bytes = f.read()

    print(f"Extracting all {TOTAL_POKEMON} entries from ROM and generating master editable text template...")

    with open(OUTPUT_TXT, "w", encoding="utf-8") as out:
        out.write("# === POKÉMON STADIUM 2 MASTER EDITABLE CONFIG SHEET ===\n")
        out.write("# This file was automatically generated from your active ROM file.\n")
        out.write("# Edit names and numbers, then run run_universal_modder.py to inject updates.\n\n")

        for i in range(TOTAL_POKEMON):
            base = PRIME_CUP_START + (i * POKEMON_SIZE)
            
            # Guard safety window check
            if base + POKEMON_SIZE > len(rom_bytes):
                break

            level = rom_bytes[base + 0]
            species_id = rom_bytes[base + 1]

            # Read 1-byte move assignments from verified layout columns
            b4 = rom_bytes[base + 4]
            b5 = rom_bytes[base + 5]
            b6 = rom_bytes[base + 6]
            b7 = rom_bytes[base + 7]

            # Convert Move Hex IDs to Text Names using your moves_list file data
            m1 = moves_dict.get(b4, f"Unknown_0x{b4:02X}")
            m2 = moves_dict.get(b5, f"Unknown_0x{b5:02X}")
            m3 = moves_dict.get(b6, f"Unknown_0x{b6:02X}")
            m4 = moves_dict.get(b7, f"Unknown_0x{b7:02X}")

            # Read Happiness
            happy = rom_bytes[base + 9]

            # Read 2-byte Stat EXP segments back-to-back using the unpacked format rules
            hp_exp, atk_exp, def_exp, spd_exp, spc_exp = struct.unpack(">HHHHH", rom_bytes[base+10:base+20])

            # Read 2 DV Bytes
            dv_byte1 = rom_bytes[base + 20]
            dv_byte2 = rom_bytes[base + 21]

            # Parse standard individual DVs out from raw file nibbles
            dv_attack  = (dv_byte1 >> 4) & 0x0F
            dv_defense = dv_byte1 & 0x0F
            dv_speed   = (dv_byte2 >> 4) & 0x0F
            dv_special = dv_byte2 & 0x0F

            # Get Species Text Name
            species_name = species_dict.get(species_id, f"Unknown_0x{species_id:02X}")

            # Format the output configuration text block exactly how your universal modder script handles it
            out.write(f"POKEMON_SLOT_INDEX: {i}\n")
            out.write(f"REPLACEMENT_SPECIES: {species_name}\n")
            out.write(f"MOVE1: {m1}\n")
            out.write(f"MOVE2: {m2}\n")
            out.write(f"MOVE3: {m3}\n")
            out.write(f"MOVE4: {m4}\n")
            out.write(f"HAPPINESS: {happy}\n")
            out.write(f"STAT_EXP_HP: {hp_exp}\n")
            out.write(f"STAT_EXP_ATK: {atk_exp}\n")
            out.write(f"STAT_EXP_DEF: {def_exp}\n")
            out.write(f"STAT_EXP_SPD: {spd_exp}\n")
            out.write(f"STAT_EXP_SPC: {spc_exp}\n")
            out.write(f"DV_ATTACK: {dv_attack}\n")
            out.write(f"DV_DEFENSE: {dv_defense}\n")
            out.write(f"DV_SPEED: {dv_speed}\n")
            out.write(f"DV_SPECIAL: {dv_special}\n")
            
            # Print entry split lines unless it reaches the absolute final record line
            if i < TOTAL_POKEMON - 1:
                out.write("---\n")

    print(f"\n[SUCCESS] Complete custom configuration layout written directly to file: '{OUTPUT_TXT}'")

if __name__ == '__main__':
    generate_ready_to_edit_config()