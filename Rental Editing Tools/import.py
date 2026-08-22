import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

print(f"--- DEBUG START ---")
print(f"Script location: {script_dir}")
print(f"Searching inside: {project_root}")
print(f"--- SCANNING ALL FILES ---")

ROM_NAME = None

for root, dirs, files in os.walk(project_root):
    # Print every file found to see if it's even reaching the sibling folder
    for f in files:
        print(f"Found file: {f} (in {root})")
        
        # Case-insensitive check to protect against capitalization bugs
        if f.lower() == 'baserom.z64':
            ROM_NAME = os.path.join(root, f)
            print(f"\n MATCH FOUND USING LOWERCASE CHECK!")
            break
    if ROM_NAME:
        break

print(f"--- DEBUG END ---")
if ROM_NAME:
    print(f"Final ROM Path: {ROM_NAME}")
else:
    print("Final Result: Still Not Found")