#!/usr/bin/env python3
import time
import shutil
from pathlib import Path
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileMovedEvent

from PIL import Image, UnidentifiedImageError

# ==== Einstellungen ====
PROJECT_ROOT = Path(__file__).resolve().parent
WATCH_DIR = (PROJECT_ROOT / "static" / "images").resolve()
OG_DIR = WATCH_DIR / "og"
VALID_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}  # was wir verarbeiten
WEBP_QUALITY = 82  # Zielqualität für verlustbehaftete Formate
STABILIZE_TRIES = 10  # Anzahl Versuche, bis die Datei-Größe stabil ist
STABILIZE_SLEEP = 0.25  # Wartezeit pro Versuch in Sekunden
# =======================

def ensure_dirs():
    OG_DIR.mkdir(parents=True, exist_ok=True)

def is_temp_or_hidden(p: Path) -> bool:
    name = p.name.lower()
    return (
        name.endswith(".part") or name.endswith(".tmp") or
        name.startswith("~$") or name.startswith(".")
    )

def wait_until_stable(p: Path) -> bool:
    """Warte, bis die Datei nicht mehr wächst (z.B. während Kopieren/Download)."""
    last = -1
    for _ in range(STABILIZE_TRIES):
        if not p.exists():
            time.sleep(STABILIZE_SLEEP)
            continue
        size = p.stat().st_size
        if size > 0 and size == last:
            return True
        last = size
        time.sleep(STABILIZE_SLEEP)
    return p.exists() and p.stat().st_size > 0

def to_webp(src: Path) -> Path:
    dst = src.with_suffix(".webp")
    try:
        with Image.open(src) as im:
            # Farbmodi sauber aufbereiten
            if im.mode == "P":
                im = im.convert("RGBA")
            elif im.mode in ("CMYK", "YCbCr"):
                im = im.convert("RGB")

            ext = src.suffix.lower()
            save_kwargs = {}

            if ext == ".png":
                # PNG -> WEBP lossless bewahrt Transparenz ohne Artefakte
                save_kwargs["lossless"] = True
                # Pillow nimmt dann quality nicht; ist ok.
            else:
                # JPG/TIFF -> WEBP mit Zielqualität
                save_kwargs["quality"] = WEBP_QUALITY
                save_kwargs["method"] = 6  # bessere, langsamere Kompression

            im.save(dst, "WEBP", **save_kwargs)
    except UnidentifiedImageError:
        raise RuntimeError(f"Keine unterstützte Bilddatei: {src}")
    return dst

def move_to_og(src: Path) -> Path:
    rel = src.relative_to(WATCH_DIR)
    target = (OG_DIR / rel).with_suffix(src.suffix)  # Originalendung behalten
    target.parent.mkdir(parents=True, exist_ok=True)
    # Kollisionen vermeiden
    if target.exists():
        stem = target.stem
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        target = target.with_name(f"{stem}-{ts}{target.suffix}")
    shutil.move(str(src), str(target))
    return target

def should_process(p: Path) -> bool:
    if not p.exists():
        return False
    if OG_DIR in p.parents:  # nichts im og/ erneut angreifen
        return False
    if p.suffix.lower() == ".webp":
        return False
    if p.suffix.lower() not in VALID_EXTS:
        return False
    if is_temp_or_hidden(p):
        return False
    # bereits vorhandene webp?
    if p.with_suffix(".webp").exists():
        return False
    return True

def process_file(path_str: str):
    p = Path(path_str)
    if not should_process(p):
        return
    if not wait_until_stable(p):
        print(f"[WARN] Datei wurde nicht stabil: {p}")
        return
    print(f"[INFO] Konvertiere -> WEBP: {p}")
    webp_path = to_webp(p)
    moved = move_to_og(p)
    print(f"[OK]  {p.name} -> {webp_path.name} (Original verschoben nach {moved})")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if isinstance(event, FileCreatedEvent) and not event.is_directory:
            process_file(event.src_path)

    def on_moved(self, event):
        if isinstance(event, FileMovedEvent) and not event.is_directory:
            # Auch Dateien berücksichtigen, die in den Ordner verschoben wurden
            process_file(event.dest_path)

def main():
    print(f"[START] Beobachte: {WATCH_DIR}")
    ensure_dirs()
    observer = Observer()
    observer.schedule(Handler(), str(WATCH_DIR), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
