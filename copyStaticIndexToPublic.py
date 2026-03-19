from pathlib import Path
import shutil

# Quelle deiner Landing Page
SOURCE_INDEX = Path("static/index.html")

# Ziel im Hugo-Build
TARGET_INDEX = Path("public/index.html")

# Optionaler Ordner für Assets
SOURCE_ASSETS = Path("static/landing")
TARGET_ASSETS = Path("public/landing")


def copy_index():
    if not SOURCE_INDEX.exists():
        raise FileNotFoundError(f"Landing page not found: {SOURCE_INDEX}")

    TARGET_INDEX.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(SOURCE_INDEX, TARGET_INDEX)

    print(f"✔ Copied landing page → {TARGET_INDEX}")


def copy_assets():
    if not SOURCE_ASSETS.exists():
        print("No landing assets directory found, skipping asset copy.")
        return

    if TARGET_ASSETS.exists():
        shutil.rmtree(TARGET_ASSETS)

    shutil.copytree(SOURCE_ASSETS, TARGET_ASSETS)

    print(f"✔ Copied landing assets → {TARGET_ASSETS}")


def main():
    print("Replacing Hugo root index with landing page...")
    copy_index()
    copy_assets()
    print("Done.")


if __name__ == "__main__":
    main()