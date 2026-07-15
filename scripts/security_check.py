import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP = {"venv", ".venv", "node_modules", "dist", "build", ".git", "__pycache__", "tests", "src/static"}
PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "predictable-admin-password": re.compile(r"admin123", re.I),
    "hardcoded-legacy-secret": re.compile(r"pes-pakistan-entrepreneurship-society-2024", re.I),
    "unrestricted-credentialed-cors": re.compile(r"CORS\(app,\s*supports_credentials\s*=\s*True\s*\)"),
    "debug-server": re.compile(r"app\.run\([^\n]*debug\s*=\s*True"),
}
findings = []
for path in ROOT.rglob("*"):
    if not path.is_file() or any(part in SKIP for part in path.parts):
        continue
    if path.suffix.lower() not in {".py", ".md", ".txt", ".json", ".yml", ".yaml", ".bat", ".sh"}:
        continue
    relative = path.relative_to(ROOT).as_posix()
    if relative == "scripts/security_check.py":
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    for rule, pattern in PATTERNS.items():
        if pattern.search(text):
            findings.append((relative, rule))
for path in ROOT.iterdir():
    if path.name.startswith(".env") and path.name != ".env.example":
        findings.append((path.name, "populated-env-file"))
if findings:
    for file_name, rule in findings:
        print(f"ERROR: {file_name} [{rule}]")
    sys.exit(1)
print("Security source check passed.")
