from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent

NAVBARS = {
    "en": ROOT / "tools" / "navbars" / "navbar-en.html",
    "ar": ROOT / "tools" / "navbars" / "navbar-ar.html",
    "de": ROOT / "tools" / "navbars" / "navbar-de.html",
    "zh": ROOT / "tools" / "navbars" / "navbar-zh.html",
}

SKIP_DIRS = {
    ".git",
    ".vscode",
    "node_modules",
    "tools",
}


def get_language(file_path: Path) -> str:
    parts = file_path.parts

    if "ar" in parts:
        return "ar"

    if "de" in parts:
        return "de"

    if "zh" in parts:
        return "zh"

    return "en"


def load_navbar(lang: str) -> str:
    navbar_file = NAVBARS[lang]

    if not navbar_file.exists():
        raise FileNotFoundError(f"Navbar template missing: {navbar_file}")

    content = navbar_file.read_text(encoding="utf-8")

    if not content.strip():
        raise ValueError(f"Navbar template empty: {navbar_file}")

    return content


def replace_header(html: str, navbar: str) -> str:
    start = html.find("<header")
    if start == -1:
        return html

    end = html.find("</header>", start)

    if end == -1:
        return html

    end += len("</header>")

    return html[:start] + navbar + html[end:]


def process_file(file_path: Path):
    lang = get_language(file_path)
    navbar = load_navbar(lang)

    content = file_path.read_text(encoding="utf-8", errors="ignore")

    new_content = replace_header(content, navbar)

    if new_content == content:
        return False

    backup = file_path.with_suffix(file_path.suffix + ".bak")

    if not backup.exists():
        shutil.copy2(file_path, backup)

    file_path.write_text(new_content, encoding="utf-8")

    print(f"Updated: {file_path}")

    return True


def should_skip(path: Path):
    return any(part in SKIP_DIRS for part in path.parts)


def main():
    updated = 0

    for html_file in ROOT.rglob("*.html"):
        if should_skip(html_file):
            continue

        try:
            if process_file(html_file):
                updated += 1

        except Exception as e:
            print(f"ERROR: {html_file} -> {e}")

    print()
    print("=" * 50)
    print(f"Files updated: {updated}")
    print("=" * 50)


if __name__ == "__main__":
    main()
