from PIL import Image
import os
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parents[2]
asset_path = BASE_DIR / "assets"


def get_key(filename: str):
    if "2" in filename:
        return "2"
    elif "3" in filename:
        return "3"
    elif "4" in filename:
        return "4"
    elif "5" in filename:
        return "5"
    elif "6" in filename:
        return "6"
    elif "7" in filename:
        return "7"
    elif "8" in filename:
        return "8"
    elif "9" in filename:
        return "9"
    elif "10" in filename:
        return "10"
    elif "Jack" in filename:
        return "J"
    elif "Queen" in filename:
        return "Q"
    elif "King" in filename:
        return "K"
    elif "Ace" in filename:
        return "A"
    elif "Back" in filename:
        return "Back"
    elif "Joker" in filename:
        return "Joker"


def load_images(asset_path: Path = asset_path):
    images = defaultdict(list)
    for file in os.listdir(asset_path):
        img = Image.open(asset_path / file)
        key = get_key(file)
        if key == "Joker":
            continue
        images[key].append(img)
    return images
