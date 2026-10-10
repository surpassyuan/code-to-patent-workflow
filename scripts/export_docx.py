"""Optional pinned-upstream Word export. Output is a candidate pending visual QA."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess
import sys
import zipfile
import workflow as w
from verify_vendor import verify, ROOT


def export(case):
    verify()
    case, state, _ = w.load_case(case)
    rev, manifest = w.current_revision(case, state)
    if 'application.json' not in manifest['files']:
        raise ValueError('Create a reviewed application packet before Word export')
    # Validate the complete review history and all blockers, not only a status string.
    w.finalize(case)
    output = case / 'exports' / f"r{state['revision']:02d}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')}"
    output.mkdir(parents=True)
    rendered = output / 'application.md'
    docx = output / '申请文件_排版候选.docx'
    application_tools = ROOT / 'vendor/patent-disclosure-skill/skills/patent-application/tools'
    text = (rev / 'application.md').read_text(encoding='utf-8')
    if '```mermaid' in text:
        renderer = ROOT / 'vendor/patent-disclosure-skill/skills/patent-disclosure/tools/mermaid_render.py'
        subprocess.run([sys.executable, str(renderer), '-i', str(rev / 'application.md'), '-o', str(rendered), '--no-docx'], check=True)
        result = rendered.read_text(encoding='utf-8')
        expected = text.count('```mermaid')
        if len(re.findall(r'<!--\s*!\[.*?\]\(.*?\)\s*-->', result)) < expected:
            raise ValueError('Not all diagrams rendered; retain Markdown and repair before Word delivery')
    else:
        rendered.write_text(text, encoding='utf-8')
    process = subprocess.run([sys.executable, str(application_tools / 'md_to_docx.py'), '-i', str(rendered), '-o', str(docx)],
                             check=True, capture_output=True, text=True, encoding='utf-8')
    log = process.stdout + process.stderr
    (output / 'conversion.log').write_text(log, encoding='utf-8')
    with zipfile.ZipFile(docx) as archive:
        if archive.testzip():
            raise ValueError('Broken DOCX archive')
        xml = archive.read('word/document.xml').decode('utf-8')
        if '```mermaid' in xml:
            raise ValueError('Unrendered diagram in Word output')
    formula_fallback = bool(re.search(r'OMML_FAIL:|omml_text_fallback=[1-9]|MATH:.*(?:png|text)=[1-9]', log))
    report = {'status': 'requires-formula-repair' if formula_fallback else 'pending-visual-qa',
              'revision': state['revision'], 'reviewed_artifact_hashes': manifest['files'],
              'docx_sha256': w.digest(docx.read_bytes()), 'docx': str(docx),
              'note': 'Render and inspect pages; Word export is not final formatting or legal approval.'}
    w.save_json(output / 'export-status.json', report)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True)
    try:
        print(__import__('json').dumps(export(parser.parse_args().case), ensure_ascii=False))
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
