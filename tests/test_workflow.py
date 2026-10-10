import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("workflow", ROOT / "scripts/workflow.py")
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        self.code = self.source / "main.py"
        self.code.write_text("def transform(x):\n    return x + 1\n", encoding="utf-8")
        self.case = self.root / "case"
        w.start(self.source, self.case)
        self.bundle = w.read_json(self.case / "evidence.json")
        self.eid = next(e["id"] for e in self.bundle["evidence"] if e["symbol"] == "transform")
        self.features = {"title": "测试交底书", "features": [
            {"id": "F1", "name": "变换", "statement": "对输入加一。", "support": "explicit", "activation": "active",
             "origin": "modified", "evidence": [self.eid], "effect": {"status": "expected", "text": "待验证"}}]}
        self.feature_file = self.root / "features.json"
    def draft(self):
        w.save_json(self.feature_file, self.features)
        return w.draft(self.case, self.feature_file, "test")
    def reviews(self, blocking=False):
        state = w.read_json(self.case / "state.json")
        manifest = w.read_json(self.case / f"r{state['revision']:02d}/manifest.json")
        for role in w.ROLES:
            file = self.root / f"{role}.json"
            issues = [{"severity": "blocking", "description": "test blocker"}] if blocking and role == "adversarial" else []
            w.save_json(file, {"revision": state["revision"], "draft_sha256": manifest["files"]["disclosure.md"], "artifact_hashes": manifest['files'], "summary": "test review", "issues": issues})
            w.review(self.case, role, file)
    def test_end_to_end_two_rounds(self):
        self.draft(); self.reviews(True)
        self.features["features"][0]["statement"] = "获取输入并加一后输出。"
        self.draft(); self.reviews()
        self.assertEqual(w.finalize(self.case)["status"], "reviewed-draft-for-inventor")
        self.assertTrue((self.case / "r01/disclosure.md").exists())
    def test_one_round_cannot_finalize(self):
        self.draft(); self.reviews()
        with self.assertRaisesRegex(ValueError, "two"):
            w.finalize(self.case)
    def test_latest_blocker_cannot_finalize(self):
        self.draft(); self.reviews()
        self.draft(); self.reviews(True)
        with self.assertRaisesRegex(ValueError, "blocking"):
            w.finalize(self.case)
    def test_missing_review_cannot_finalize(self):
        self.draft(); self.reviews()
        self.draft()
        with self.assertRaisesRegex(ValueError, "Missing"):
            w.finalize(self.case)
    def test_unknown_evidence_rejected(self):
        self.features["features"][0]["evidence"] = ["fake"]
        with self.assertRaisesRegex(ValueError, "evidence"):
            self.draft()
    def test_supported_without_evidence_rejected(self):
        self.features["features"][0]["evidence"] = []
        with self.assertRaisesRegex(ValueError, "evidence"):
            self.draft()
    def test_disabled_feature_excluded(self):
        extra = dict(self.features["features"][0], id="F2", statement="DO_NOT_INCLUDE", activation="inactive")
        self.features["features"].append(extra)
        self.draft()
        self.assertNotIn("DO_NOT_INCLUDE", (self.case / "r01/disclosure.md").read_text(encoding="utf-8"))
        self.assertIn("DO_NOT_INCLUDE", (self.case / "r01/review-appendix.json").read_text(encoding="utf-8"))
    def test_source_drift_rejected(self):
        self.code.write_text("def transform(x): return x - 1\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "drift"):
            self.draft()
    def test_frozen_draft_edit_rejected(self):
        self.draft()
        (self.case / "r01/disclosure.md").write_text("tampered", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "changed"):
            w.finalize(self.case)
    def test_historical_draft_edit_rejected(self):
        self.draft(); self.reviews()
        self.draft(); self.reviews()
        (self.case / "r01/disclosure.md").write_text("tampered history", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Historical"):
            w.finalize(self.case)
    def test_stale_review_rejected(self):
        self.draft()
        file = self.root / "stale.json"
        w.save_json(file, {"revision": 0, "draft_sha256": "old", "summary": "old", "issues": []})
        with self.assertRaisesRegex(ValueError, "current"):
            w.review(self.case, "implementation", file)
    def test_revision_budget(self):
        self.draft(); self.draft(); self.draft()
        with self.assertRaisesRegex(ValueError, "budget"):
            self.draft()
    def test_effect_validation_requires_protocol(self):
        self.features["features"][0]["effect"] = {"status": "validated", "evidence": [self.eid]}
        with self.assertRaisesRegex(ValueError, "protocol"):
            self.draft()
    def test_scan_does_not_execute_source(self):
        marker = self.root / "executed"
        evil = self.source / "never_import.py"
        evil.write_text(f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n", encoding="utf-8")
        bundle = w.source_snapshot(self.source)
        self.assertFalse(marker.exists())
        self.assertTrue(any(f["path"] == "never_import.py" for f in bundle["files"]))
    def test_source_id_stable(self):
        again = w.source_snapshot(self.source)
        self.assertEqual(self.bundle["evidence"], again["evidence"])
    def test_secret_and_weights_not_scanned(self):
        (self.source / ".env").write_text("secret", encoding="utf-8")
        (self.source / "model.pt").write_bytes(b"weight")
        bundle = w.source_snapshot(self.source)
        self.assertEqual([f["path"] for f in bundle["files"]], ["main.py"])

    def packet(self):
        return w.read_json(ROOT / 'examples/application.template.json')

    def application_draft(self, packet=None):
        file = self.root / 'application.json'
        w.save_json(file, packet or self.packet())
        w.save_json(self.feature_file, self.features)
        return w.draft(self.case, self.feature_file, 'application test', file)

    def test_application_two_rounds_delivered_with_support_map(self):
        self.application_draft(); self.reviews()
        self.application_draft(); self.reviews()
        result = w.finalize(self.case)
        final = Path(result['delivery'])
        support = w.read_json(final / 'application-support.json')
        self.assertEqual(support['claims'][0]['code_evidence'], [self.eid])
        self.assertTrue((final / '说明书.md').exists())
        self.assertTrue((final / 'figure-1.mmd').exists())

    def test_application_disabled_claim_rejected(self):
        self.features['features'][0]['activation'] = 'inactive'
        with self.assertRaises(ValueError):
            self.application_draft()
        self.assertFalse((self.case / 'r01').exists())

    def test_application_unknown_claim_feature_rejected(self):
        packet = self.packet()
        packet['claims'][0]['features'] = ['FAKE']
        with self.assertRaisesRegex(ValueError, 'supported active'):
            self.application_draft(packet)

    def test_application_forward_or_self_claim_dependency_rejected(self):
        packet = self.packet()
        packet['claims'][0]['depends_on'] = [1]
        with self.assertRaisesRegex(ValueError, 'preceding'):
            self.application_draft(packet)

    def test_claim_feature_without_embodiment_step_rejected(self):
        self.features['features'].append(dict(self.features['features'][0], id='F2'))
        packet = self.packet()
        packet['claims'][0]['features'].append('F2')
        with self.assertRaisesRegex(ValueError, 'implementation step'):
            self.application_draft(packet)

    def test_prior_art_compared_without_source_rejected(self):
        packet = self.packet()
        packet['prior_art']['status'] = 'compared'
        with self.assertRaisesRegex(ValueError, 'sources'):
            self.application_draft(packet)

    def test_prior_art_unknown_comparison_source_rejected(self):
        packet = self.packet()
        packet['prior_art'] = {'status': 'partial', 'sources': [],
                               'differences': [{'feature': 'F1', 'source': 'FAKE', 'comparison': 'unsupported'}]}
        with self.assertRaisesRegex(ValueError, 'known prior-art source'):
            self.application_draft(packet)

    def test_formula_missing_symbol_definitions_rejected(self):
        packet = self.packet()
        packet['formulas'] = [{'id': 'E1', 'latex': 'x+1', 'features': ['F1'], 'variables': []}]
        with self.assertRaisesRegex(ValueError, 'symbol definitions'):
            self.application_draft(packet)

    def test_application_review_requires_whole_packet_binding(self):
        self.application_draft()
        manifest = w.read_json(self.case / 'r01/manifest.json')
        review_file = self.root / 'review.json'
        w.save_json(review_file, {'revision': 1, 'draft_sha256': manifest['files']['disclosure.md'],
                                 'summary': 'Only reviewed disclosure', 'issues': []})
        with self.assertRaisesRegex(ValueError, 'artifact_hashes'):
            w.review(self.case, 'implementation', review_file)

    def test_frozen_application_tamper_rejected(self):
        self.application_draft(); self.reviews()
        (self.case / 'r01/权利要求书.md').write_text('tampered claim', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'changed'):
            w.finalize(self.case)

    def test_review_packet_hash_tamper_rejected(self):
        self.application_draft(); self.reviews()
        self.application_draft(); self.reviews()
        path = self.case / 'r02/reviews/implementation.json'
        record = w.read_json(path)
        record['artifact_hashes']['application.md'] = 'old'
        w.save_json(path, record)
        with self.assertRaisesRegex(ValueError, 'record changed|artifact review'):
            w.finalize(self.case)

    def test_blocking_review_cannot_be_edited_into_clearance(self):
        self.draft(); self.reviews()
        self.draft(); self.reviews(True)
        path = self.case / 'r02/reviews/adversarial.json'
        record = w.read_json(path)
        record['issues'] = []
        w.save_json(path, record)
        with self.assertRaisesRegex(ValueError, 'record changed'):
            w.finalize(self.case)

    def test_versioned_delivery_does_not_reuse_old_application(self):
        self.application_draft(); self.reviews()
        self.application_draft(); self.reviews()
        first = Path(w.finalize(self.case)['delivery'])
        self.draft(); self.reviews()
        second = Path(w.finalize(self.case)['delivery'])
        self.assertNotEqual(first, second)
        self.assertTrue((first / 'application.md').is_file())
        self.assertFalse((second / 'application.md').exists())

    def test_vendored_files_match_pinned_checksums(self):
        import verify_vendor
        self.assertEqual(len(verify_vendor.verify()), 494)

if __name__ == "__main__":
    unittest.main()
