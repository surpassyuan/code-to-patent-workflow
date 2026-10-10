"""Verify pinned upstream files without running downloaded scripts."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def verify(root=ROOT):
    root = Path(root).resolve()
    lock = json.loads((root / 'vendor/manifest.json').read_text(encoding='utf-8'))
    files = []
    for project in lock['projects']:
        base = root / project['path']
        if base.parent != root / 'vendor' or not project['commit'] or project['license'] != 'MIT':
            raise ValueError('Invalid upstream lock entry')
        for rel, expected in project['files'].items():
            path = base / rel
            if not path.resolve().is_relative_to(base.resolve()) or path.is_symlink():
                raise ValueError('Upstream path escapes its package')
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise ValueError('Upstream checksum mismatch: ' + str(path.relative_to(root)))
            files.append(path)
        if 'LICENSE' not in project['files']:
            raise ValueError('Upstream license must be retained')
    return files


if __name__ == '__main__':
    print(f'Verified {len(verify())} pinned upstream files.')
