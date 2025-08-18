import os
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from Utils import local_path, user_path
from worlds.alttp.Rom import Sprite
from worlds.alttp.Adjuster import get_image_for_sprite, update_sprites

class NullTask:
    def update_status(self, text: str):
        pass

    def queue_event(self, fn):
        fn()

    def close_window(self):
        pass

    # Target directories
    input_dir = user_path("data", "sprites", "alttp", "remote")
    output_dir = local_path("WebHostLib", "static", "generated")  # TODO: move to user_path

def update_sprites_lttp(
    parallel: bool = True,
    max_workers: int = None,
    skip_remote_update: bool = False,
    remote_timeout: int = 8
):

    if not skip_remote_update:
        print(f"Fetching sprite index (timeout {remote_timeout}s)…")
        task = NullTask()
        t = threading.Thread(target=lambda: update_sprites(task), daemon=True)
        t.start()
        t.join(remote_timeout)
        if t.is_alive():
            print(f"⚠️ Sprite‐list update still running after {remote_timeout}s; proceeding without waiting.")
        else:
            print("✅ Sprite‐list update finished.")

    input_dir   = user_path("data", "sprites", "alttp", "remote")
    base_out    = local_path("WebHostLib", "static", "generated")
    sprites_out = os.path.join(base_out, "sprites")
    os.makedirs(sprites_out, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if not f.startswith(".")]

    def process_one(file_name):
        path = os.path.join(input_dir, file_name)
        sp   = Sprite(path)
        if not sp.name:
            sp.name = os.path.splitext(file_name)[0]
        if not sp.valid:
            return None

        img = get_image_for_sprite(sp, True)
        out = os.path.join(sprites_out, f"{os.path.splitext(file_name)[0]}.gif")
        with open(out, "wb") as wf:
            wf.write(img)
        return {"file": file_name, "author": sp.author_name, "name": sp.name}

    sprite_data = []
    if parallel:
        with ThreadPoolExecutor(max_workers=max_workers) as exe:
            futures = {exe.submit(process_one, fn): fn for fn in files}
            for fut in tqdm(as_completed(futures), total=len(files), desc="Generating sprites"):
                res = fut.result()
                if res:
                    sprite_data.append(res)
    else:
        for fn in tqdm(files, desc="Generating sprites"):
            res = process_one(fn)
            if res:
                sprite_data.append(res)

    sprite_data.sort(key=lambda e: e["name"])
    with open(os.path.join(base_out, "spriteData.json"), "w") as jf:
        json.dump({"sprites": sprite_data}, jf, indent=1)

    return sprite_data
