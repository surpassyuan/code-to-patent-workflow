"""Package only workflow assets, excluding Git, private cases, binary data and weights."""
from pathlib import Path
import argparse
import zipfile
from verify_vendor import verify

ROOT = Path(__file__).resolve().parents[1]
TOP = {"skills", "scripts", "tests", "examples", "docs", ".agents", ".claude", ".github"}
ROOT_FILES = {"README.md", "LICENSE", "THIRD_PARTY_NOTICES.md", "requirements-docx.txt", ".gitignore", ".gitattributes"}
SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".mmd"}

def package(output):
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    files = verify() + [ROOT / 'vendor/manifest.json']
    for file in sorted(ROOT.rglob("*")):
        if not file.is_file() or file.is_symlink():
            continue
        rel = file.relative_to(ROOT)
        if any(p in rel.parts for p in ("__pycache__", ".git", "vendor")):
            continue
        if len(rel.parts) == 1 and file.name in ROOT_FILES:
            files.append(file)
        elif rel.parts[0] in TOP and file.suffix in SUFFIXES:
            files.append(file)
    if output.exists():
        raise ValueError("Do not overwrite an existing public archive")
    with zipfile.ZipFile(output, "x", zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, "code-to-disclosure/" + file.relative_to(ROOT).as_posix())
    print(f"Packaged {len(files)} workflow files; inspect before uploading.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    package(parser.parse_args().output)
