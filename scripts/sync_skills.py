"""Install project-local skills for both hosts; no edits to global user settings."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
for scope in (".agents", ".claude"):
    for skill in (root / "skills").iterdir():
        if skill.is_dir():
            dest = root / scope / "skills" / skill.name
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copytree(skill, dest, dirs_exist_ok=True)
            if scope == ".agents":
                meta = dest / "agents/openai.yaml"
                meta.parent.mkdir(exist_ok=True)
                meta.write_text('interface:\n  display_name: "' + skill.name + '"\n  short_description: "代码证据驱动的技术交底起草、追溯与多轮复核工作流"\n  default_prompt: "Use $' + skill.name + ' in this repository for a code-grounded technical disclosure."\n', encoding="utf-8")
print("Synced project skills to .agents/skills and .claude/skills; vendor references remain pinned and are not auto-installed")
