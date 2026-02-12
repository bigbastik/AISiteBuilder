import json
import sys
from pathlib import Path

def split_json(file_path: str):
    """
    Legge un JSON unico (layout o temi) e crea tanti file separati,
    uno per ogni chiave principale, in una sottocartella dedicata.
    """
    json_file = Path(file_path)
    if not json_file.exists():
        print(f"❌ File non trovato: {json_file}")
        return

    # Legge JSON
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Determina tipo (layout o tema) in base al contenuto della prima chiave
    first_value = next(iter(data.values()))
    if "sezioni" in first_value or "nome" in first_value:
        subfolder = "layouts"
    elif "colore_primario" in first_value:
        subfolder = "themes"
    else:
        subfolder = "output"

    output_dir = json_file.parent / subfolder
    output_dir.mkdir(exist_ok=True)

    count = 0
    for key, value in data.items():
        output_file = output_dir / f"{key}.json"

        # Per i temi, wrappa il contenuto in {"tema": ...} per compatibilità
        if subfolder == "themes":
            json_content = {"tema": value}
        else:
            json_content = value

        output_file.write_text(json.dumps(json_content, indent=2, ensure_ascii=False), encoding="utf-8")
        count += 1

    print(f"✅ Creati {count} file in {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python split.py nome_file.json")
        sys.exit(1)

    split_json(sys.argv[1])
