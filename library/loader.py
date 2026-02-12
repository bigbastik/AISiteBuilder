import json
from pathlib import Path

BASE_DIR = Path(__file__).parent


def load_layouts():
    layouts = []
    layout_dir = BASE_DIR / "layouts"

    # 🔧 FIX: cartella mancante → nessun crash
    if not layout_dir.exists():
        return []

    for file in layout_dir.glob("*.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))

            # 🔧 FIX: id e nome automatici
            data.setdefault("id", file.stem)
            data.setdefault("nome", file.stem.replace("_", " ").title())

            layouts.append(data)

        except Exception as e:
            print(f"[LAYOUT ERROR] {file.name}: {e}")

    return layouts


def load_themes():
    themes = []
    theme_dir = BASE_DIR / "themes"

    # 🔧 FIX: cartella mancante → nessun crash
    if not theme_dir.exists():
        return []

    for file in theme_dir.glob("*.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))

            # 🔧 FIX: id e nome automatici
            data.setdefault("id", file.stem)
            data.setdefault("nome", file.stem.replace("_", " ").title())

            themes.append(data)

        except Exception as e:
            print(f"[THEME ERROR] {file.name}: {e}")

    return themes
