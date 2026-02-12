import json
import sys
from pathlib import Path

def split_json(file_path: str):
    """
    Legge un JSON unico e crea tanti file separati per ogni chiave principale.
    I file vengono salvati nella stessa cartella del JSON originale.
    """
    json_file = Path(file_path)
    if not json_file.exists():
        print(f"❌ File non trovato: {json_file}")
        return

    # Legge JSON
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    output_dir = json_file.parent
    count = 0

    for key, value in data.items():
        # Crea file per ogni chiave
        output_file = output_dir / f"{key}.json"
        # Struttura compatibile con layout o tema
        if "nome" in value or "sezioni" in value:
            # Layout
            json_content = value
        elif "colore_primario" in value or "font" in value:
            # Tema
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
