import os

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
        

OUTPUT_DIAG = "master_table_hex_check.txt"
START_OFFSET = 0X98F20  # The verified Data Crystal master offset

def analyze_true_table_alignment():
    if not os.path.exists(ROM_INPUT):
        print(f"Error: '{ROM_INPUT}' not found.")
        return

    with open(ROM_INPUT, "rb") as f:
        f.seek(START_OFFSET)
        # Read a clean 600-byte chunk of the actual data table zone
        raw_chunk = f.read(600)

    bytes_list = list(raw_chunk)

    with open(OUTPUT_DIAG, "w", encoding="utf-8") as out:
        out.write(f"=== RAW MASTER TABLE HEX CHECK STARTING AT {hex(START_OFFSET)} ===\n\n")
        
        # Print the data in rows of 12 bytes, 16 bytes, and 24 bytes 
        # so we can visually spot exactly where the next Pokémon ID starts.
        for width in [12, 16, 22, 24]:
            out.write(f"--- Visual Grid: {width} Bytes Per Row ---\n")
            for row_idx in range(15):
                start = row_idx * width
                end = start + width
                if end <= len(bytes_list):
                    row_bytes = bytes_list[start:end]
                    hex_string = " ".join(f"{b:02X}" for b in row_bytes)
                    dec_string = " ".join(f"{b:03d}" for b in row_bytes)
                    out.write(f"+{start:03d} (Hex): {hex_string}\n")
            out.write("\n" + "="*50 + "\n\n")

    print(f"Analysis file generated: {OUTPUT_DIAG}")

if __name__ == "__main__":
    analyze_true_table_alignment()