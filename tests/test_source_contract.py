import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class SourceContractTests(unittest.TestCase):
    def test_main_has_no_hardcoded_secret_or_default_password(self):
        text = (ROOT / "src/main.py").read_text(encoding="utf-8")
        self.assertNotIn("admin123", text)
        self.assertNotIn("pes-pakistan-entrepreneurship-society-2024", text)
        self.assertNotIn("CORS(app, supports_credentials=True)", text)
        self.assertNotIn("debug=True", text)

    def test_public_registration_forces_member_role(self):
        text = (ROOT / "src/routes/auth.py").read_text(encoding="utf-8")
        self.assertIn("public_registration=True", text)
        self.assertNotIn("role=data.get('role'", text)

    def test_sensitive_routes_do_not_return_raw_internal_exceptions(self):
        for relative in ["src/routes/auth.py", "src/routes/user.py", "src/main.py"]:
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("except Exception as e", text)

    def test_app_factory_exists(self):
        self.assertIn("def create_app(", (ROOT / "src/main.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
