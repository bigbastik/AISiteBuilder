import os
import json
import uuid
import shutil
from pathlib import Path
from library.loader import load_layouts
from copy import deepcopy
from core.project_identity import generate_project_identity

# =================================================
# STATO PROGETTO ATTIVO
# =================================================

PROJECTS_DIR = Path("project")
PROJECTS_DIR.mkdir(exist_ok=True)

CURRENT_PROJECT: str | None = None


def set_current_project(name: str):
    global CURRENT_PROJECT
    CURRENT_PROJECT = name
    (PROJECTS_DIR / name).mkdir(parents=True, exist_ok=True)


def _project_file() -> Path:
    if not CURRENT_PROJECT:
        raise RuntimeError("Nessun progetto attivo")
    return PROJECTS_DIR / CURRENT_PROJECT / "project.json"


# =================================================
# BASE
# =================================================

def load_project(project_name: str | None = None) -> dict:
    if project_name:
        set_current_project(project_name)

    project_file = _project_file()

    if not project_file.exists():
        save_project({
            "meta": {
                "title": "",
                "description": "",
                "keywords": ""
             },
                "brand": {
                "nome": "",
                "tagline": "",
                "settore": ""
             },
                "tema": {},
                "pagine": []
        })


    data = json.loads(project_file.read_text(encoding="utf-8"))
    _normalize_pages(data)
    return data



def ensure_project_exists(arg):
    # -------------------------------------------------
    # CASE 1: nome progetto (legacy)
    # -------------------------------------------------
    if isinstance(arg, str):
        set_current_project(arg)
        file = _project_file()

        if not file.exists():
            save_project({
                "meta": {
                    "title": "",
                    "description": "",
                    "keywords": ""
                },
                "tema": {},
                "pagine": []
            })
        return

    # -------------------------------------------------
    # CASE 2: struttura dict (NUOVA o VECCHIA)
    # -------------------------------------------------
    if isinstance(arg, dict):
        if not CURRENT_PROJECT:
            raise RuntimeError("CURRENT_PROJECT non impostato")

        site = arg.get("site", {})

        project = {
            "meta": arg.get("meta") or {
                "title": site.get("titolo_sito", ""),
                "description": "",
                "keywords": ""
            },
            "tema": site.get("tema", arg.get("tema", {})),
            "pagine": []
        }

        # 🔹 PAGINE
        if isinstance(site.get("pagine"), list):
            project["pagine"] = site["pagine"]
        elif isinstance(arg.get("pagine"), list):
            project["pagine"] = arg["pagine"]

        # 🔹 LAYOUT (retrocompatibilità)
        layout = arg.get("layout")
        if layout and isinstance(layout.get("pagine"), list):
            project["pagine"] = layout["pagine"]

        save_project(project)


        return

    raise TypeError("ensure_project_exists accetta solo str o dict")

    # -------------------------------------------------
    # CASE 2: struttura dict (NUOVA o VECCHIA)
    # -------------------------------------------------
    if isinstance(arg, dict):
        if not CURRENT_PROJECT:
            raise RuntimeError("CURRENT_PROJECT non impostato")

        site = arg.get("site", {})

        project = {
            "meta": arg.get("meta") or {
                "title": site.get("titolo_sito", ""),
                "description": "",
                "keywords": ""
            },
            "tema": site.get("tema", arg.get("tema", {})),
            "pagine": []
        }

        # 🔹 PAGINE
        if isinstance(site.get("pagine"), list):
            project["pagine"] = site["pagine"]
        elif isinstance(arg.get("pagine"), list):
            project["pagine"] = arg["pagine"]

        # 🔹 LAYOUT (retrocompatibilità)
        layout = arg.get("layout")
        if layout and isinstance(layout.get("pagine"), list):
            project["pagine"] = layout["pagine"]

        save_project(project)

        return

    raise TypeError("ensure_project_exists accetta solo str o dict")


# =================================================
# NORMALIZZAZIONE STRUTTURA
# =================================================

def _normalize_pages(data: dict):
    pagine = data.setdefault("pagine", [])

    if not pagine:
        pagine.append({
            "nome": "Home",
            "sections": []
        })

    page_names = [p.get("nome", f"Pagina{i}") for i, p in enumerate(pagine)]

    for page in pagine:
        page.setdefault("sections", [])
        # 🔹 aggiunge il menu per ogni pagina
        page["menu"] = [{"nome": n, "link": f"{n.replace(' ', '_').lower()}.html"} for n in page_names]

    # 🔥 REALISTIC MODE: brand sempre presente
    brand = data.setdefault("brand", {})
    brand.setdefault("nome", "")
    brand.setdefault("tagline", "")
    brand.setdefault("settore", "")


# =================================================
# META
# =================================================

def update_meta(title: str, description: str, keywords: str):
    data = load_project()
    data.setdefault("meta", {})
    data["meta"]["title"] = title
    data["meta"]["description"] = description
    data["meta"]["keywords"] = keywords
    save_project(data)


# =================================================
# PAGINE / SEZIONI
# =================================================

def get_pages() -> list:
    data = load_project()

    # FIX: garantisce struttura coerente prima di passarla alla UI
    _normalize_pages(data)

    return data.get("pagine", [])


def update_section_text(
    page_index: int,
    section_index: int,
    titolo: str | None = None,
    testo: str | None = None
):
    data = load_project()

    try:
        section = data["pagine"][page_index]["sections"][section_index]
    except (KeyError, IndexError):
        raise ValueError("Pagina o sezione non valida")

    # ✅ il titolo è sempre valido
    if titolo is not None:
        section["titolo"] = titolo

    # ✅ il testo è valido per TUTTE le sezioni
    if testo is not None:
        section["testo"] = testo

    save_project(data)


# =================================================
# THEME
# =================================================

def get_theme() -> dict:
    data = load_project()
    return data.get("tema", {})


def update_theme(
    primary: str,
    secondary: str,
    background: str,
    text: str,
    font: str | None = None
):
    data = load_project()
    data.setdefault("tema", {})
    data["tema"]["colore_primario"] = primary
    data["tema"]["colore_secondario"] = secondary
    data["tema"]["sfondo"] = background
    data["tema"]["testo"] = text
    if font is not None:
        data["tema"]["font"] = font
    save_project(data)

#===================================================
# LAYOUT
#===================================================

def apply_layout_legacy(layout_id: str):
    data = load_project()
    layouts = load_layouts()

    layout = next((l for l in layouts if l["id"] == layout_id), None)
    if not layout:
        raise ValueError("Layout non trovato")

    data["pagine"] = []

    for p in layout["pagine"]:
        data["pagine"].append({
            "nome": p["nome"],
            "sections": p["sections"]
        })

    save_project(data)

# =====================================================
# LAYOUT & THEME PRESETS
# =====================================================

import json

BASE_DIR = Path(__file__).resolve().parent.parent
LIBRARY_DIR = BASE_DIR / "library"

LAYOUTS_DIR = "library/layouts"
THEMES_DIR = "library/themes"

def list_layouts():
    if not os.path.exists(LAYOUTS_DIR):
        return []
    return [
        f.replace(".json", "")
        for f in os.listdir(LAYOUTS_DIR)
        if f.endswith(".json")
    ]


def apply_layout(layout_name: str):
    project = load_project()
    path = os.path.join(LAYOUTS_DIR, f"{layout_name}.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Layout '{layout_name}' non trovato")

    with open(path, "r", encoding="utf-8") as f:
        layout = json.load(f)

    layout_pages = layout.get("pagine", [])
    project_pages = project.get("pagine", [])

    layout_map = {
        p.get("nome"): p.get("sections", [])
        for p in layout_pages
        if "nome" in p
    }

    for page in project_pages:
        nome = page.get("nome")
        if nome in layout_map:
            page["sections"] = deepcopy(layout_map[nome])


    _normalize_pages(project)
    save_project(project)
   
def list_themes():
    if not os.path.exists(THEMES_DIR):
        return []
    return [
        f.replace(".json", "")
        for f in os.listdir(THEMES_DIR)
        if f.endswith(".json")
    ]


def apply_theme(theme_name: str):
    project = load_project()
    path = os.path.join(THEMES_DIR, f"{theme_name}.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Tema '{theme_name}' non trovato")

    with open(path, "r", encoding="utf-8") as f:
        theme = json.load(f)

    project["tema"] = theme.get("tema", {})
    save_project(project)

def _normalize_pages(data: dict):
    pagine = data.setdefault("pagine", [])

    if not pagine:
        pagine.append({
            "nome": "Home",
            "sections": []
        })

    for page in pagine:
        page.setdefault("sections", [])

    # 🔥 REALISTIC MODE: brand sempre presente
    brand = data.setdefault("brand", {})
    brand.setdefault("nome", "")
    brand.setdefault("tagline", "")
    brand.setdefault("settore", "")

def save_project(data: dict):
    project_file = _project_file()
    _normalize_pages(data)
    project_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

# =================================================
# SEZIONI DINAMICHE
# =================================================

def add_section(page_index: int, tipo: str) -> dict:
    """
    Aggiunge una nuova sezione di tipo specifico SOLO alla pagina indicata.
    Ritorna la sezione appena creata.
    """
    pages = get_pages()  # recupera le pagine correnti
    if page_index < 0 or page_index >= len(pages):
        raise IndexError("Indice pagina non valido")

    page = pages[page_index]

    new_section = {
        "titolo": f"Nuova Sezione ({tipo})",
        "testo": "",
        "immagine": None,
        "tipo": tipo,
        "id": f"sec_{len(page['sections'])}"
    }

    page["sections"].append(new_section)

    save_project(load_project())  # salva subito il JSON
    return new_section

# =================================================
# SEZIONI DINAMICHE
# =================================================

def add_section(page_index: int, tipo: str = "text"):
    """Aggiunge una nuova sezione SOLO alla pagina selezionata, con titolo coerente col tipo"""
    data = load_project()
    try:
        page = data["pagine"][page_index]
    except IndexError:
        raise ValueError("Pagina non valida")

    tipo_default_title = {
        "head": "Header",
        "hero": "Hero",
        "text": "Testo",
        "footer": "Footer"
    }
    titolo = tipo_default_title.get(tipo, "Nuova Sezione")

    new_section = {
        "id": str(uuid.uuid4()),
        "tipo": tipo,
        "titolo": titolo,
        "testo": "",
        "immagini": []
    }

    page["sections"].append(new_section)

    # Aggiorna il menu della pagina
    page["menu"] = [{"nome": s.get("titolo", "Sezione"),
                     "link": f"{s.get('titolo', 'sezione').replace(' ', '_').lower()}.html"}
                    for s in page["sections"]]

    save_project(data)
    return new_section


def remove_section(page_index: int, section_index: int):
    """Rimuove una sezione dalla pagina"""
    data = load_project()
    try:
        page = data["pagine"][page_index]
        page["sections"].pop(section_index)
        # Aggiorna il menu dopo la rimozione
        page["menu"] = [{"nome": s.get("titolo", "Sezione"),
                         "link": f"{s.get('titolo', 'sezione').replace(' ', '_').lower()}.html"}
                        for s in page["sections"]]
    except IndexError:
        raise ValueError("Pagina o sezione non valida")
    save_project(data)


def move_section(page_index: int, section_index: int, direction: str):
    """Sposta una sezione su o giù"""
    data = load_project()
    try:
        sections = data["pagine"][page_index]["sections"]
    except IndexError:
        raise ValueError("Pagina non valida")

    if direction == "up" and section_index > 0:
        sections[section_index], sections[section_index - 1] = sections[section_index - 1], sections[section_index]
    elif direction == "down" and section_index < len(sections) - 1:
        sections[section_index], sections[section_index + 1] = sections[section_index + 1], sections[section_index]
    else:
        return  # niente da fare

    # Aggiorna il menu dopo lo spostamento
    page = data["pagine"][page_index]
    page["menu"] = [{"nome": s.get("titolo", "Sezione"),
                     "link": f"{s.get('titolo', 'sezione').replace(' ', '_').lower()}.html"}
                    for s in sections]

    save_project(data)


def update_section_text(page_index: int, section_index: int, titolo: str | None = None, testo: str | None = None):
    """Aggiorna titolo e testo di una sezione e rigenera il menu della pagina"""
    data = load_project()
    try:
        section = data["pagine"][page_index]["sections"][section_index]
    except (KeyError, IndexError):
        raise ValueError("Pagina o sezione non valida")

    if titolo is not None:
        section["titolo"] = titolo
        # Aggiorna il menu della pagina
        page = data["pagine"][page_index]
        page["menu"] = [{"nome": s.get("titolo", "Sezione"),
                         "link": f"{s.get('titolo', 'sezione').replace(' ', '_').lower()}.html"}
                        for s in page["sections"]]

    if testo is not None:
        section["testo"] = testo

    save_project(data)


def update_section_type(page_index: int, section_index: int, tipo: str):
    """Cambia il tipo di una sezione"""
    data = load_project()
    try:
        section = data["pagine"][page_index]["sections"][section_index]
    except IndexError:
        raise ValueError("Pagina o sezione non valida")

    section["tipo"] = tipo
    save_project(data)


def add_image_to_section(page_index: int, section_index: int, image_path: str):
    """Aggiunge un'immagine a una sezione e la copia in assets/images"""
    data = load_project()
    try:
        section = data["pagine"][page_index]["sections"][section_index]
    except IndexError:
        raise ValueError("Pagina o sezione non valida")

    # Assicurati che la cartella esista
    assets_dir = Path("project") / CURRENT_PROJECT / "assets" / "images"
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Copia l'immagine dentro assets/images
    image_name = Path(image_path).name
    dest_path = assets_dir / image_name
    shutil.copy(image_path, dest_path)

    # Salva il path relativo nella sezione
    section.setdefault("immagini", []).append(f"assets/images/{image_name}")

    save_project(data)


def remove_image_from_section(page_index: int, section_index: int, image_index: int):
    """Rimuove un'immagine da una sezione"""
    data = load_project()
    try:
        section = data["pagine"][page_index]["sections"][section_index]
        section["immagini"].pop(image_index)
    except IndexError:
        raise ValueError("Pagina, sezione o immagine non valida")
    save_project(data)
