import os
import sys
import re
import shutil

# Configuration parameters matching your workspace

# 1. Define your base project root (Up one level from the script)
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up to the parent folder
project_root = os.path.dirname(script_dir)

# Define tracking files based on your workspace setup
DUMP_TEXT_FILE = None

# 3. Use os.walk to search downward through the directories
###. Search downward using a case-insensitive check
for root, dirs, files in os.walk(project_root):
    for f in files:
        if f.lower() == 'pokemon_stadium_2_stat_sheet.txt':
            DUMP_TEXT_FILE = os.path.join(root, f)
            break
    if DUMP_TEXT_FILE:
        break  # Stop searching once found

if not DUMP_TEXT_FILE:
    print("Could not find 'pokemon_stadium_2_stat_sheet.txt' in the parent or its subfolders.")
    print("Please make sure the file exists and try again.")
    sys.exit(1)  # Stops the script safely right here


# Define tracking files based on your workspace setup

LOOKUP_SHEET = None

# 4. Use os.walk to search downward through the directories
###. Search downward using a case-insensitive check
for root, dirs, files in os.walk(project_root):
    for f in files:
        if f.lower() == 'pokemon_reverse_lookup_sheet.txt':
            LOOKUP_SHEET = os.path.join(root, f)
            break
    if LOOKUP_SHEET:
        break  # Stop searching once found

if not LOOKUP_SHEET:
    print("Could not find 'pokemon_reverse_lookup_sheet.txt' in the parent or its subfolders.")
    print("Please make sure the file exists and try again.")
    sys.exit(1)  # Stops the script safely right here

ROM_INPUT = None

# 5. Use os.walk to search downward through the directories
###. Search downward using a case-insensitive check
for root, dirs, files in os.walk(project_root):
    for f in files:
        if f.lower() == 'baserom_modified.z64':
            ROM_INPUT = os.path.join(root, f)
            break
    if ROM_INPUT:
        break  # Stop searching once found

if not ROM_INPUT:
    print("Could not find 'baserom.z64' in the parent or its subfolders.")
    print("Please make sure the file exists and try again.")
    sys.exit(1)  # Stops the script safely right here

# 6. Set the variable ROM_OUTPUT to the directory pathname with baserom_modified.z64 (the output file)

# 7. Search downward for the file and save it to a variable
DUMP_TEXT_FILE  = None

# 8. Use os.walk to search downward through the directories
for root, dirs, files in os.walk(project_root):
    for f in files:
        if f.lower() == 'pokemon_stadium_2_stat_sheet.txt':
            DUMP_TEXT_FILE  = os.path.join(root, f)
            break
    if DUMP_TEXT_FILE :
        break  # Stop searching once found
		
# 9. Search downward for the file and save it to a variable
TYPES_FILE = None

# 10. Use os.walk to search downward through the directories
for root, dirs, files in os.walk(project_root):
    for f in files:
        if f.lower() == 'types_list.txt':
            TYPES_FILE = os.path.join(root, f)
            break
    if TYPES_FILE:
        break  # Stop searching once found

# 11. Define the folder path variable you want to ensure exists
target_dir = os.path.join(project_root, 'Editing')

# 12. Create the folder safely if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

os.chdir(target_dir)

#13. Set the variable ROM_OUTPUT to the directory pathname with baserom_modified.z64 (the output file)
rom_folder = os.path.dirname(ROM_INPUT)
ROM_OUTPUT = os.path.join(rom_folder, "baserom_modified2.z64")   


def load_reverse_type_map(type_path):
    """Parses text labels back into single-byte hex representations."""
    rev_type_map = {}
    if not os.path.exists(type_path):
        print(f"Error: Missing reverse types map registry file: '{type_path}'")
        return rev_type_map
    with open(type_path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                hex_key, label = line.strip().split(":", 1)
                try:
                    rev_type_map[label.strip().lower()] = int(hex_key.strip(), 16)
                except ValueError:
                    continue
    return rev_type_map

def run_safe_injection():
    if not os.path.exists(DUMP_TEXT_FILE) or not os.path.exists(ROM_INPUT):
        print("Error: Missing 'stadium2_master_stats_dump.txt' or 'baserom.z64' in directory.")
        return

    rev_types = load_reverse_type_map(TYPES_FILE)

    # Initialize a secure test environment duplicate copy
    shutil.copyfile(ROM_INPUT, ROM_OUTPUT)
    print(f"Working copy successfully generated at: {ROM_OUTPUT}")

    with open(DUMP_TEXT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex engine configuration to extract data fields safely from text file blocks
    block_pattern = re.compile(
        r"#\s*TARGET_ROM_OFFSET:\s*(0X[0-9a-fA-F]+)\s*\n"
        r"SPECIES_ID:\s*[^\n]+\s*\n"
        r"BASE_HP:\s*(\d+)\s*\n"
        r"BASE_ATTACK:\s*(\d+)\s*\n"
        r"BASE_DEFENSE:\s*(\d+)\s*\n"
        r"BASE_SPEED:\s*(\d+)\s*\n"
        r"BASE_SPECIAL_ATTACK:\s*(\d+)\s*\n"
        r"BASE_SPECIAL_DEFENSE:\s*(\d+)\s*\n"
        r"TYPE_1:\s*([^\n]+)\s*\n"
        r"TYPE_2:\s*([^\n]+)"
    )

    matches = block_pattern.findall(content)
    flash_count = 0

    with open(ROM_OUTPUT, "r+b") as rom_f:
        for match in matches:
            offset_str, hp, atk, df, spe, spa, spd, t1, t2 = match
            
            # The exact, unshifting file layout coordinate
            base_address = int(offset_str, 16)

            # Compile values into clean numeric lists
            stats_payload = [int(hp), int(atk), int(df), int(spe), int(spa), int(spd)]
            
            # Translate element naming strings directly back to their internal IDs
            t1_byte = rev_types.get(t1.lower().strip(), 0x00) # Default Normal fallback
            t2_byte = rev_types.get(t2.lower().strip(), t1_byte)
            if t2.strip().lower() == "none":
                t2_byte = t1_byte

            # Construct the complete binary update payload
            payload = bytes(stats_payload + [t1_byte, t2_byte])
            
            # Jump 1 byte forward (skipping the valid Pokemon ID byte) and overwrite stats and types
            rom_f.seek(base_address + 1)
            rom_f.write(payload)
            flash_count += 1

    print(f"\n[Success] Flashed {flash_count} records strictly to their target structural addresses!")
    print(f"Modifications saved safely to: {ROM_OUTPUT}")

if __name__ == "__main__":
    run_safe_injection()