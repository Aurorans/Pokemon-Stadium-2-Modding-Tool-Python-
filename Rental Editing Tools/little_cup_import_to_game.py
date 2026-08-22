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
        
 
if not ROM_INPUT:
    print("Could not find 'baserom.z64' in the parent or its subfolders.")
    print("Please make sure the file exists and try again.")
    sys.exit(1)  # Stops the script safely right here

# 4. Set the variable ROM_OUTPUT to the directory pathname with baserom_modified.z64 (the output file)

rom_folder = os.path.dirname(ROM_INPUT)
ROM_OUTPUT = os.path.join(rom_folder, "baserom_modified.z64")   

RENTAL_FILE = None

# 5. Use os.walk to search downward through the directories
for root, dirs, files in os.walk(project_root):
    for f in files:
        if f.lower() == 'little_cup_rental_pokemon.txt':
            RENTAL_FILE = os.path.join(root, f)
            break
    if RENTAL_FILE:
        break  # Stop searching once found

if not RENTAL_FILE:
    print("Could not find 'little_cup_rental_pokemon.txt' in the parent or its subfolders.")
    print("Please make sure the file exists and try again.")
    sys.exit(1)  # Stops the script safely right here    
    
# 6. Search downward for the file and save it to a variable
MOVES_FILE = None

# 7. Use os.walk to search downward through the directories
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

# 8. Search downward for the file and save it to a variable
SPECIES_FILE = None

# 9. Use os.walk to search downward through the directories
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

LITTLE_CUP_START = 0x1708494
POKEMON_SIZE = 0x18

def load_text_map(filepath):
    text_map = {}
    if not os.path.exists(filepath):
        print(f"Error: Missing required resource mapping asset: '{filepath}'")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if ":" in line and not line.startswith("#"):
                hex_str, name = line.split(":", 1)
                try:
                    text_map[name.strip().lower()] = int(hex_str.strip(), 16)
                except ValueError: continue
    return text_map

def parse_config():
    if not os.path.exists(RENTAL_FILE):
        print(f"Error: Configurations file '{RENTAL_FILE}' missing.")
        return []
    
    entries = []
    current = {}
    with open(RENTAL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or not line: continue
            if line == "---":
                if current: entries.append(current); current = {}
                continue
            if ":" in line:
                key, val = line.split(":", 1)
                current[key.strip().upper()] = val.strip()
        if current: entries.append(current)
    return entries

def execute_modding_resource():
    species_dict = load_text_map(SPECIES_FILE)
    moves_dict = load_text_map(MOVES_FILE)
    config_entries = parse_config()
    
    if not species_dict or not moves_dict or not config_entries:
        print("Compilation aborted due to missing map file definitions.")
        return

    if not os.path.exists(ROM_INPUT):
        print(f"Error: Could not locate baseline cartridge ROM file '{ROM_INPUT}'")
        return

    with open(ROM_INPUT, "rb") as f:
        rom_bytes = bytearray(f.read())

    print("Compiling user asset maps into uncompressed ROM stream...")
    print("-----------------------------------------------------------------")

    for entry in config_entries:
        try:
            slot_idx = int(entry["POKEMON_SLOT_INDEX"])
            spec_name = entry["REPLACEMENT_SPECIES"].lower()
            spec_id = species_dict.get(spec_name)
            
            if spec_id is None:
                print(f"Skipping entry: Unknown species descriptor '{entry['REPLACEMENT_SPECIES']}'")
                continue

            # Fetch move IDs via the lookup map matching your external index
            m1 = moves_dict.get(entry["MOVE1"].lower(), 0x00)
            m2 = moves_dict.get(entry["MOVE2"].lower(), 0x00)
            m3 = moves_dict.get(entry["MOVE3"].lower(), 0x00)
            m4 = moves_dict.get(entry["MOVE4"].lower(), 0x00)

            # Decimal to Hexadecimal Conversion handling for Stat EXPs
            hp_exp  = int(entry.get("STAT_EXP_HP", 0))
            atk_exp = int(entry.get("STAT_EXP_ATK", 0))
            def_exp = int(entry.get("STAT_EXP_DEF", 0))
            spd_exp = int(entry.get("STAT_EXP_SPD", 0))
            spc_exp = int(entry.get("STAT_EXP_SPC", 0))
            happy   = int(entry.get("HAPPINESS", 255))

            # Decimal to Hexadecimal Conversion handling for individual DVs
            dv_atk  = int(entry.get("DV_ATTACK", 15)) & 0x0F
            dv_def  = int(entry.get("DV_DEFENSE", 15)) & 0x0F
            dv_spd  = int(entry.get("DV_SPEED", 15)) & 0x0F
            dv_spc  = int(entry.get("DV_SPECIAL", 15)) & 0x0F

            base = LITTLE_CUP_START + (slot_idx * POKEMON_SIZE)

            # --- APPLY BYTE WRITING ---
#           rom_bytes[base + 0] = 0x05 #Level 5
            rom_bytes[base + 1] = spec_id
            rom_bytes[base + 2] = 0x00  # Structural Padding
            rom_bytes[base + 3] = 0x00
            
            # Write Move Slots 4, 5, 6, and 7
            rom_bytes[base + 4] = m1
            rom_bytes[base + 5] = m2
            rom_bytes[base + 6] = m3
            rom_bytes[base + 7] = m4

            # Write Happiness Tracker Field
            rom_bytes[base + 8] = 0x00
            rom_bytes[base + 9] = happy & 0xFF

            # Inject 2-Byte Stat EXP Pairs
            struct.pack_into(">HHHHH", rom_bytes, base + 10, hp_exp, atk_exp, def_exp, spd_exp, spc_exp)

            # Pack Individual DVs into the final two bytes
            dv_b1 = (dv_atk << 4) | dv_def
            dv_b2 = (dv_spd << 4) | dv_spc
            rom_bytes[base + 20] = dv_b1
            rom_bytes[base + 21] = dv_b2

            print(f" -> Compiled Slot {slot_idx:03d}: {entry['REPLACEMENT_SPECIES']} with custom stats.")
        except KeyError as e:
            print(f"Configuration formatting syntax failure: Missing key field {e}")
            continue

    with open(ROM_OUTPUT, "wb") as f: f.write(rom_bytes)
    print("-----------------------------------------------------------------")
    print(f"Mod successfully compiled to: '{ROM_OUTPUT}'")

if __name__ == "__main__":
    execute_modding_resource()