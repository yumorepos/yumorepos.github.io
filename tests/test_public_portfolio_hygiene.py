"""Guard current public GitHub Pages files, not historical Git revisions."""
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
UNSAFE_NAMES = {".env", ".env.local", ".env.production", "id_rsa", "id_ed25519"}
UNSAFE_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".sqlite", ".duckdb",
                     ".p12", ".pfx", ".pem", ".key", ".zip"}
TEXT_EXTENSIONS = {".html", ".md", ".css", ".js", ".yml", ".yaml", ".txt", ".json"}
SENSITIVE_PATTERNS = {
    "github-token": re.compile("gh" + "p_" + r"[A-Za-z0-9]{30,}"),
    "github-pat": re.compile("github_" + "pat_" + r"[A-Za-z0-9_]{35,}"),
    "openai-key": re.compile("sk-" + r"(?:proj-)?[A-Za-z0-9_-]{24,}"),
    "aws-key": re.compile("AK" + "IA" + r"[A-Z0-9]{16}"),
    "private-key": re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "local-home": re.compile(r"/" + r"Users/[A-Za-z0-9_.-]+/"),
}


def git_paths():
    cmd = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True)
    return [ROOT / p.decode("utf-8") for p in cmd.stdout.split(b"\x00") if p]


class PublicPortfolioHygiene(unittest.TestCase):
    def test_no_private_uploads_or_secrets_on_main(self):
        failures = []
        for path in git_paths():
            rel = path.relative_to(ROOT).as_posix()
            if path.name in UNSAFE_NAMES or path.suffix.lower() in UNSAFE_EXTENSIONS:
                failures.append(f"{rel}: unsafe document or credential file type")
                continue
            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                for category, pattern in SENSITIVE_PATTERNS.items():
                    if pattern.search(line):
                        failures.append(f"{rel}:{line_no}: {category}")
        self.assertEqual(failures, [], "Potential public-file risk (value redacted): " + "; ".join(failures))

    def test_active_portfolio_is_public_website_only(self):
        for required in ("index.html", "network-lab.html", "case-study.html",
                         "style.css", "main.js"):
            self.assertTrue((ROOT / required).is_file(), required)
        self.assertFalse((ROOT / "docs/AVIATION_PORTFOLIO_PROGRAM.md").exists())
        self.assertFalse((ROOT / "docs/AVIATION_PORTFOLIO_HANDOFF_2026-11-09.md").exists())


if __name__ == "__main__":
    unittest.main()
