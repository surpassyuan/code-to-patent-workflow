"""Deterministic two-round fixture. Findings are scripted, not generated model reviews."""
from pathlib import Path
import argparse
import json
import workflow as w

def run(destination, application=False):
    root = Path(__file__).resolve().parents[1]
    case = Path(destination).resolve()
    w.start(root / "examples/toy_transform", case)
    bundle = w.read_json(case / "evidence.json")
    def ref(symbol):
        return next(e["id"] for e in bundle["evidence"] if e["symbol"] == symbol)
    features = {"title": "数值变换技术交底书（合成演示）", "field": "计算机数值处理",
                "problem": "按照给定加法规则变换输入数值列表。",
                "embodiment": "输入数值列表，逐个加一，输出新列表；本演示不主张技术创新或性能收益。",
                "features": [
                    {"id": "F1", "name": "数值加一", "statement": "获取数值列表，将每个数值加一并输出新列表。",
                     "support": "explicit", "activation": "active", "origin": "new", "evidence": [ref("transform")],
                     "effect": {"status": "expected", "text": "按给定规则生成新列表"}},
                    {"id": "F2", "name": "附加元数据", "statement": "在处理路径中附加元数据。", "support": "explicit",
                     "activation": "active", "origin": "new", "evidence": [ref("attach_metadata"), ref("prepare")],
                     "effect": {"status": "expected", "text": "仅展示开关核查"}}]}
    candidate = case / "working-features.json"
    packet = root / 'examples/application.template.json' if application else None
    w.save_json(candidate, features)
    w.draft(case, candidate, "Synthetic round 1 intentionally overstates activation", packet)
    for role in w.ROLES:
        manifest = w.read_json(case / "r01/manifest.json")
        issues = [{"id": "I1", "severity": "blocking", "feature": "F2",
                   "description": "Code exists but configuration and default argument disable metadata; withdraw active-scheme assertion."}] if role == "implementation" else []
        findings = case / f"working-{role}.json"
        w.save_json(findings, {"revision": 1, "draft_sha256": manifest["files"]["disclosure.md"],
                              "artifact_hashes": manifest['files'],
                              "summary": "SCRIPTED fixture review: activation checked against source and config.", "issues": issues})
        w.review(case, role, findings)
    features["features"][1]["activation"] = "inactive"
    w.save_json(candidate, features)
    w.draft(case, candidate, "Resolve I1: move disabled metadata path to review appendix", packet)
    for role in w.ROLES:
        manifest = w.read_json(case / "r02/manifest.json")
        findings = case / f"working-{role}.json"
        w.save_json(findings, {"revision": 2, "draft_sha256": manifest["files"]["disclosure.md"],
                              "artifact_hashes": manifest['files'],
                              "summary": "SCRIPTED re-check: disabled feature removed from implementation narrative.", "issues": []})
        w.review(case, role, findings)
    result = w.finalize(case)
    return {"fixture": "scripted, not LLM evaluation", **result, "case": str(case)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--application", action='store_true')
    args = parser.parse_args()
    print(json.dumps(run(args.output, args.application), ensure_ascii=False))
