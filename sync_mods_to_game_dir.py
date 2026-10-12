import os
import shutil

doc_mods_dir = os.path.expanduser("~/Documents/Teardown/mods")
game_mods_dir = r"S:\Teardown\Teardown.Build.12032026-OFME\Teardown\mods"

def sync_mods():
    print(f"Syncing mods from {doc_mods_dir} to {game_mods_dir}...")
    
    if not os.path.exists(game_mods_dir):
        print("Game mods directory not found!")
        return

    items = os.listdir(doc_mods_dir)
    for item in items:
        src = os.path.join(doc_mods_dir, item)
        dst = os.path.join(game_mods_dir, item)
        
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"Copied mod to game directory: {item}")

    print("Sync completed successfully!")

if __name__ == "__main__":
    sync_mods()
