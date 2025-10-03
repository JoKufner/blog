#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import shutil
import re
from pathlib import Path
from datetime import datetime

# --- Konfiguration ------------------------------------------------------------
WATCH_DIR   = Path(r"C:\Users\PCUser\Pictures\Screenshots")  # Quellverzeichnis
TARGET_DIR  = Path(r"D:\repos\blog\static\images")           # Zielverzeichnis
VALID_EXTS  = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}  # beobachtete Endungen

PLAY_SOUND  = True     # Systemton vor der Benutzereingabe abspielen?
BEEP_KIND   = "ASTERISK"  # "OK", "ASTERISK", "EXCLAMATION", "HAND"

# Warte-Strategie, bis die Datei "fertig geschrieben" ist
STABILIZE_TRIES = 20
STABILIZE_SLEEP = 0.25  # Sekunden
# ------------------------------------------------------------------------------

import winsound  # stdlib (Windows)
import pyperclip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileMovedEvent

BEEP_MAP = {
    "OK": winsound.MB_OK,
    "ASTERISK": winsound.MB_ICONASTERISK,
    "EXCLAMATION": winsound.MB_ICONEXCLAMATION,
    "HAND": winsound.MB_ICONHAND,
}

def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def ensure_dirs():
    if not WATCH_DIR.exists():
        raise FileNotFoundError(f"WATCH_DIR existiert nicht: {WATCH_DIR}")
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

def is_temp_or_hidden(p: Path) -> bool:
    n = p.name.lower()
    return n.startswith("~$") or n.startswith(".") or n.endswith(".tmp") or n.endswith(".part")

def wait_until_stable(p: Path) -> bool:
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

def sanitize_filename(name: str, max_len: int = 100) -> str:
    name = name.strip()
    name = re.sub(r'[\\/:*?"<>|]+', "-", name)
    name = re.sub(r"[\x00-\x1f]", "", name)
    name = name.strip(" .")
    if not name:
        name = "unnamed"
    if len(name) > max_len:
        name = name[:max_len].rstrip(" .")
    reserved = {"CON","PRN","AUX","NUL","COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9",
                "LPT1","LPT2","LPT3","LPT4","LPT5","LPT6","LPT7","LPT8","LPT9"}
    if name.upper() in reserved:
        name = f"{name}_file"
    return name

def get_clipboard_text(min_len=4, max_len=50) -> str | None:
    try:
        text = pyperclip.paste()
    except pyperclip.PyperclipException:
        return None
    if not isinstance(text, str):
        return None
    txt = text.strip()
    if min_len <= len(txt) <= max_len:
        return txt
    return None

def prompt_for_name() -> str:
    if PLAY_SOUND:
        winsound.MessageBeep(BEEP_MAP.get(BEEP_KIND, winsound.MB_OK))
    while True:
        try:
            name = input("Bitte Dateinamen (ohne Endung) eingeben: ").strip()
        except (EOFError, KeyboardInterrupt):
            name = ""
        if 4 <= len(name) <= 50:
            return name
        print("Name muss zwischen 4 und 50 Zeichen lang sein.")

def unique_path(dirpath: Path, stem: str, ext: str) -> Path:
    candidate = dirpath / f"{stem}{ext}"
    if not candidate.exists():
        return candidate
    for i in range(1, 1000):
        c = dirpath / f"{stem}-{i:02d}{ext}"
        if not c.exists():
            return c
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return dirpath / f"{stem}-{ts}{ext}"

def handle_file(src: Path):
    if not src.exists() or is_temp_or_hidden(src):
        return
    ext = src.suffix.lower()
    if ext not in VALID_EXTS:
        return

    log(f"Neu erkannt: {src.name} (Endung: {ext})")

    if not wait_until_stable(src):
        log(f"Warnung: Datei wurde nicht stabil: {src}")
        return

    # -------- Zielname ermitteln --------
    clip = get_clipboard_text()
    if clip:
        stem = sanitize_filename(clip)
        log(f"Clipboard-Name erkannt: '{stem}'")
    else:
        log("Kein gültiger Clipboard-Text (4–50 Zeichen). Frage Benutzer…")
        stem = sanitize_filename(prompt_for_name())
        log(f"Benutzereingabe: '{stem}'")

    # >>> NEU: <name>.webp in die Zwischenablage schreiben
    webp_name_for_clipboard = f"{stem}.webp"
    try:
        pyperclip.copy(webp_name_for_clipboard)
        log(f"Clipboard gesetzt: {webp_name_for_clipboard}")
    except pyperclip.PyperclipException as e:
        log(f"Clipboard konnte nicht gesetzt werden: {e}")

    # -------- Datei kopieren (mit Original-Endung) --------
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    dst = unique_path(TARGET_DIR, stem, ext)
    shutil.copy2(src, dst)
    log(f"Kopiert nach: {dst}")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if isinstance(event, FileCreatedEvent) and not event.is_directory:
            handle_file(Path(event.src_path))

    def on_moved(self, event):
        if isinstance(event, FileMovedEvent) and not event.is_directory:
            handle_file(Path(event.dest_path))

def main():
    ensure_dirs()
    log(f"Überwache: {WATCH_DIR}")
    log(f"Zielordner: {TARGET_DIR}")
    observer = Observer()
    observer.schedule(Handler(), str(WATCH_DIR), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        log("Beende…")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
