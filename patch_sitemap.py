from pathlib import Path
import xml.etree.ElementTree as ET

PUBLIC_DIR = Path("public")
SITEMAP_INDEX_PATH = PUBLIC_DIR / "sitemap.xml"
LANDING_SITEMAP_FILENAME = "landing-sitemap.xml"
LANDING_SITEMAP_PATH = PUBLIC_DIR / LANDING_SITEMAP_FILENAME

ROOT_URL = "https://jonaskufner.com/"
LANDING_SITEMAP_URL = f"{ROOT_URL}{LANDING_SITEMAP_FILENAME}"

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", SITEMAP_NS)


def qname(tag: str) -> str:
    return f"{{{SITEMAP_NS}}}{tag}"


def indent_xml(elem: ET.Element, level: int = 0) -> None:
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i


def create_landing_sitemap() -> None:
    urlset = ET.Element(qname("urlset"))

    url = ET.SubElement(urlset, qname("url"))
    loc = ET.SubElement(url, qname("loc"))
    loc.text = ROOT_URL

    changefreq = ET.SubElement(url, qname("changefreq"))
    changefreq.text = "weekly"

    priority = ET.SubElement(url, qname("priority"))
    priority.text = "1.0"

    indent_xml(urlset)
    tree = ET.ElementTree(urlset)
    tree.write(LANDING_SITEMAP_PATH, encoding="utf-8", xml_declaration=True)
    print(f"Created {LANDING_SITEMAP_PATH}")


def patch_sitemap_index(root: ET.Element, tree: ET.ElementTree) -> None:
    existing_locs = [
        loc.text for loc in root.findall(f"./{qname('sitemap')}/{qname('loc')}")
        if loc.text
    ]

    if LANDING_SITEMAP_URL in existing_locs:
        print("landing-sitemap.xml already present in sitemap index.")
        return

    sitemap = ET.Element(qname("sitemap"))
    loc = ET.SubElement(sitemap, qname("loc"))
    loc.text = LANDING_SITEMAP_URL

    root.insert(0, sitemap)
    indent_xml(root)
    tree.write(SITEMAP_INDEX_PATH, encoding="utf-8", xml_declaration=True)
    print(f"Patched sitemap index: added {LANDING_SITEMAP_URL}")


def patch_urlset(root: ET.Element, tree: ET.ElementTree) -> None:
    existing_locs = [
        loc.text for loc in root.findall(f"./{qname('url')}/{qname('loc')}")
        if loc.text
    ]

    if ROOT_URL in existing_locs:
        print("Root URL already present in sitemap urlset.")
        return

    url = ET.Element(qname("url"))

    loc = ET.SubElement(url, qname("loc"))
    loc.text = ROOT_URL

    changefreq = ET.SubElement(url, qname("changefreq"))
    changefreq.text = "weekly"

    priority = ET.SubElement(url, qname("priority"))
    priority.text = "1.0"

    root.insert(0, url)
    indent_xml(root)
    tree.write(SITEMAP_INDEX_PATH, encoding="utf-8", xml_declaration=True)
    print(f"Patched sitemap urlset: added {ROOT_URL}")


def main() -> None:
    if not SITEMAP_INDEX_PATH.exists():
        raise FileNotFoundError(f"Missing sitemap: {SITEMAP_INDEX_PATH}")

    create_landing_sitemap()

    tree = ET.parse(SITEMAP_INDEX_PATH)
    root = tree.getroot()

    root_tag = root.tag.split("}")[-1]

    if root_tag == "sitemapindex":
        patch_sitemap_index(root, tree)
    elif root_tag == "urlset":
        patch_urlset(root, tree)
    else:
        raise ValueError(
            f"Unsupported sitemap root element: {root.tag}. "
            "Expected sitemapindex or urlset."
        )


if __name__ == "__main__":
    main()