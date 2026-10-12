import os

mods_dir = os.path.expanduser("~/Documents/Teardown/mods")

def make_all_mods_multiplayer_compatible():
    print("Updating all 19 mod info.txt files for Teardown Multiplayer compatibility...")
    
    folders = [f for f in os.listdir(mods_dir) if os.path.isdir(os.path.join(mods_dir, f))]
    
    for folder in folders:
        f_path = os.path.join(mods_dir, folder)
        info_file = os.path.join(f_path, "info.txt")
        
        if os.path.exists(info_file):
            with open(info_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            
            new_lines = []
            has_tags = False
            is_map = False
            
            # Check if it's a map or tool
            for line in lines:
                if "main.xml" in os.listdir(f_path) or "tags = Map" in line or "tags: map" in line:
                    is_map = True

            for line in lines:
                if line.strip().startswith("tags"):
                    has_tags = True
                    if is_map:
                        new_lines.append("tags = Map, Sandbox, Multiplayer\n")
                    else:
                        new_lines.append("tags = Global, Tool, Multiplayer\n")
                else:
                    new_lines.append(line)
            
            if not has_tags:
                if is_map:
                    new_lines.append("\ntags = Map, Sandbox, Multiplayer\n")
                else:
                    new_lines.append("\ntags = Global, Tool, Multiplayer\n")
            
            with open(info_file, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print(f"Updated info.txt for: {folder} (Tags: Multiplayer enabled)")

if __name__ == "__main__":
    make_all_mods_multiplayer_compatible()
