"""Tests for scripts/grc_os.py. Run: python -m unittest discover -s tests -v"""
import datetime as dt
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("grc_os", REPO / "scripts" / "grc_os.py")
grc_os = importlib.util.module_from_spec(spec)
sys.modules["grc_os"] = grc_os  # dataclasses need the module registered
spec.loader.exec_module(grc_os)

TODAY = dt.date(2026, 11, 13)

SOURCE = """---
title: Access Control Policy
owner: Security
origin: DOC-001
version_date: 2026-01-10
captured: 2026-11-01
---
# Access Control Policy

All production access requires multi-factor authentication.
Access reviews run quarterly.
"""


def write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        # Copy the shipped template so tests exercise the real registers.
        for item in ["CLAUDE.md", "program", "context", "references", "connections.md"]:
            src = REPO / item
            if src.is_dir():
                shutil.copytree(src, self.tmp / item)
            elif src.exists():
                shutil.copy(src, self.tmp / item)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def errors(self, only=None):
        return [i for i in grc_os.run_lint(self.tmp, only) if i.level == "error"]

    def set_register(self, name, rows):
        file, cols = grc_os.REGISTERS[name]
        path = self.tmp / file
        text = path.read_text(encoding="utf-8")
        table = next(t for t in grc_os.parse_tables(text) if {c.lower() for c in cols} <= {h.lower() for h in t.header})
        header = "| " + " | ".join(table.header) + " |\n|" + "---|" * len(table.header) + "\n"
        body = "".join("| " + " | ".join(r.get(h, "") for h in table.header) + " |\n" for r in rows)
        write(self.tmp, file, f"# {name}\n\n{header}{body}")


class TemplateTests(unittest.TestCase):
    def test_shipped_template_lints_clean(self):
        errors = [i for i in grc_os.run_lint(REPO) if i.level == "error"]
        self.assertEqual(errors, [], "\n".join(e.render() for e in errors))

    def test_all_registers_present_with_columns(self):
        for name in grc_os.REGISTERS:
            path, table = grc_os.find_register(REPO, name)
            self.assertTrue(path.exists(), name)
            self.assertIsNotNone(table, f"{name} table missing required columns")

    def test_skills_exist(self):
        for skill in ["start", "audit", "feedback"]:
            p = REPO / ".claude" / "skills" / skill / "SKILL.md"
            self.assertTrue(p.exists(), skill)
            fm = grc_os.parse_frontmatter(p.read_text(encoding="utf-8"))
            self.assertEqual(fm.get("name"), skill)
            self.assertTrue(fm.get("description"))


class LintTests(Base):
    def test_broken_link_detected(self):
        write(self.tmp, "context/x.md", "See [missing](nope.md).\n")
        self.assertTrue(any("broken link" in e.message for e in self.errors()))

    def test_links_in_code_ignored(self):
        write(self.tmp, "context/x.md", "```\n[a](nope.md)\n```\nand `[b](nope.md)`\n")
        self.assertFalse(any("broken link" in e.message for e in self.errors()))

    def test_valid_quote_passes(self):
        write(self.tmp, "sources/policy.md", SOURCE)
        write(self.tmp, "context/x.md",
              '> "All production access requires multi-factor   authentication." - sources/policy.md\n')
        self.assertEqual(self.errors([self.tmp / "context/x.md"]), [])

    def test_fabricated_quote_detected(self):
        write(self.tmp, "sources/policy.md", SOURCE)
        write(self.tmp, "context/x.md", '> "Access reviews run monthly." — sources/policy.md\n')
        errs = self.errors([self.tmp / "context/x.md"])
        self.assertTrue(any("quotation not found" in e.message for e in errs))

    def test_quote_missing_source(self):
        write(self.tmp, "context/x.md", '> "Anything." - sources/ghost.md\n')
        self.assertTrue(any("quoted source not found" in e.message for e in self.errors()))

    def test_frontmatter_source_missing(self):
        write(self.tmp, "context/x.md", '---\nsources: ["sources/ghost.md"]\n---\n# x\n')
        self.assertTrue(any("frontmatter source not found" in e.message for e in self.errors()))

    def test_frontmatter_list_style(self):
        write(self.tmp, "sources/policy.md", SOURCE)
        write(self.tmp, "context/x.md", "---\nsources:\n  - sources/policy.md\n---\n# x\n")
        self.assertEqual(self.errors([self.tmp / "context/x.md"]), [])

    def test_source_provenance_warning(self):
        write(self.tmp, "sources/bare.md", "# No header\n")
        warns = [i for i in grc_os.run_lint(self.tmp) if i.level == "warning"]
        self.assertTrue(any("provenance missing" in w.message for w in warns))

    def test_duplicate_register_id(self):
        self.set_register("risks", [
            {"ID": "R-1", "Risk": "a", "Owner": "CTO", "Status": "open", "Next review": "2027-01-01"},
            {"ID": "R-1", "Risk": "b", "Owner": "CTO", "Status": "open", "Next review": "2027-01-01"},
        ])
        self.assertTrue(any("duplicate ID" in e.message for e in self.errors()))

    def test_bad_date(self):
        self.set_register("actions", [
            {"ID": "A-1", "Action": "x", "Type": "remediation", "Owner": "me", "Due": "next week", "Status": "open"},
        ])
        self.assertTrue(any("YYYY-MM-DD" in e.message for e in self.errors()))

    def test_tbd_date_allowed(self):
        self.set_register("actions", [
            {"ID": "A-1", "Action": "x", "Type": "discovery", "Owner": "me", "Due": "TBD", "Status": "open"},
        ])
        self.assertFalse(any("YYYY-MM-DD" in e.message for e in self.errors()))

    def test_missing_register_columns(self):
        write(self.tmp, "program/risks.md", "# Risks\n\n| ID | Thing |\n|---|---|\n| 1 | x |\n")
        self.assertTrue(any("missing required columns" in e.message for e in self.errors()))


class PulseTests(Base):
    def test_empty_registers_quiet(self):
        text, highs = grc_os.pulse_report(self.tmp, TODAY)
        self.assertEqual(highs, 0)
        self.assertIn("No overdue", text)

    def test_overdue_action_and_unowned(self):
        self.set_register("actions", [
            {"ID": "A-1", "Action": "Enable MFA", "Type": "remediation", "Owner": "IT", "Due": "2026-10-01", "Status": "open"},
            {"ID": "A-2", "Action": "Find DPA", "Type": "discovery", "Owner": "", "Due": "2026-12-30", "Status": "open"},
            {"ID": "A-3", "Action": "Done thing", "Type": "remediation", "Owner": "IT", "Due": "2026-01-01", "Status": "Done"},
        ])
        text, highs = grc_os.pulse_report(self.tmp, TODAY)
        self.assertIn("A-1", text)
        self.assertIn("overdue since 2026-10-01", text)
        self.assertIn("A-2", text)
        self.assertNotIn("A-3", text)
        self.assertEqual(highs, 2)

    def test_exception_expiry(self):
        self.set_register("exceptions", [
            {"ID": "E-1", "Exception": "Legacy VPN", "Approved by": "CEO", "Expires": "2026-11-01", "Status": "active"},
            {"ID": "E-2", "Exception": "No SSO", "Approved by": "CEO", "Expires": "", "Status": "active"},
            {"ID": "E-3", "Exception": "Old", "Approved by": "CEO", "Expires": "2025-01-01", "Status": "closed"},
        ])
        text, _ = grc_os.pulse_report(self.tmp, TODAY)
        self.assertIn("expired 2026-11-01 but still active", text)
        self.assertIn("no expiry date", text)
        self.assertNotIn("E-3", text)

    def test_stale_evidence_vs_missing_pointer(self):
        self.set_register("controls", [
            {"ID": "C-1", "Control": "Access review", "Owner": "IT", "Evidence location": "Jira ACC",
             "Last evidence": "2026-05-01", "Frequency": "Quarterly", "Status": "operating"},
            {"ID": "C-2", "Control": "Backups", "Owner": "IT", "Evidence location": "",
             "Last evidence": "", "Frequency": "Daily", "Status": "operating"},
            {"ID": "C-3", "Control": "Policy review", "Owner": "IT", "Evidence location": "Drive",
             "Last evidence": "2026-06-01", "Frequency": "Annual", "Status": "operating"},
        ])
        text, _ = grc_os.pulse_report(self.tmp, TODAY)
        self.assertIn("C-1", text)
        self.assertIn("evidence stale", text)
        self.assertIn("not proof of control failure", text)
        self.assertNotIn("C-3", text)


class AcceptTests(Base):
    def test_accept_then_change_requires_review(self):
        write(self.tmp, "sources/policy.md", SOURCE)
        write(self.tmp, "context/x.md", '---\nsources: ["sources/policy.md"]\n---\n'
                                        '> "Access reviews run quarterly." - sources/policy.md\n')
        ok, msgs = grc_os.accept(self.tmp, "sources/policy.md", [], TODAY)
        self.assertTrue(ok, msgs)
        manifest = json.loads((self.tmp / ".grc-os/manifest.json").read_text())
        self.assertIn("sources/policy.md", manifest["sources"])
        self.assertEqual(grc_os.source_states(self.tmp)["accepted"], ["sources/policy.md"])

        write(self.tmp, "sources/policy.md", SOURCE + "\nNew clause.\n")
        self.assertEqual(grc_os.source_states(self.tmp)["changed"], ["sources/policy.md"])
        ok, msgs = grc_os.accept(self.tmp, "sources/policy.md", [], TODAY)
        self.assertFalse(ok)
        self.assertTrue(any("context/x.md" in m for m in msgs))
        ok, msgs = grc_os.accept(self.tmp, "sources/policy.md", ["context/x.md"], TODAY)
        self.assertTrue(ok, msgs)

    def test_accept_refuses_when_citing_page_has_fabricated_quote(self):
        write(self.tmp, "sources/policy.md", SOURCE)
        write(self.tmp, "context/x.md", '> "Access reviews run weekly." - sources/policy.md\n')
        ok, msgs = grc_os.accept(self.tmp, "sources/policy.md", [], TODAY)
        self.assertFalse(ok)
        self.assertFalse((self.tmp / ".grc-os/manifest.json").exists())

    def test_accept_outside_sources_refused(self):
        ok, msgs = grc_os.accept(self.tmp, "CLAUDE.md", [], TODAY)
        self.assertFalse(ok)


class ReviewTests(Base):
    def test_review_saves_unique_reports(self):
        _, _, p1 = grc_os.review(self.tmp, TODAY)
        _, _, p2 = grc_os.review(self.tmp, TODAY)
        self.assertNotEqual(p1, p2)
        self.assertTrue(p1.exists() and p2.exists())
        self.assertIn("report_kind: grc-os-review", p1.read_text(encoding="utf-8"))

    def test_cli_lint_exit_code(self):
        self.assertEqual(grc_os.main(["--root", str(self.tmp), "lint"]), 0)
        write(self.tmp, "context/x.md", "[bad](nope.md)\n")
        self.assertEqual(grc_os.main(["--root", str(self.tmp), "lint"]), 1)


if __name__ == "__main__":
    unittest.main()
