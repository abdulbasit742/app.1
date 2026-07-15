import unittest

from src.security import AttemptLimiter, clean_text, normalize_email, normalize_role, origin_allowed, parse_origins, validate_password


class SecurityPolicyTests(unittest.TestCase):
    def test_normalizes_email(self):
        self.assertEqual(normalize_email(" User@Example.COM "), "user@example.com")

    def test_rejects_invalid_email(self):
        with self.assertRaises(ValueError):
            normalize_email("not-an-email")

    def test_requires_strong_password(self):
        with self.assertRaises(ValueError):
            validate_password("short1")
        self.assertEqual(validate_password("correct-horse-42"), "correct-horse-42")

    def test_public_registration_cannot_choose_admin(self):
        self.assertEqual(normalize_role("admin", public_registration=True), "member")

    def test_rejects_unknown_role(self):
        with self.assertRaises(ValueError):
            normalize_role("superuser")

    def test_cleans_and_bounds_text(self):
        self.assertEqual(clean_text("  A\x00  B  ", "Name", minimum=2), "A B")
        with self.assertRaises(ValueError):
            clean_text("x" * 201, "Name", maximum=200)

    def test_origins_are_explicit(self):
        self.assertEqual(parse_origins("https://app.example.com"), ("https://app.example.com",))
        with self.assertRaises(ValueError):
            parse_origins("*")

    def test_origin_matching_is_exact(self):
        allowed = parse_origins("https://app.example.com")
        self.assertTrue(origin_allowed("https://app.example.com", allowed))
        self.assertFalse(origin_allowed("https://evil.example.com", allowed))

    def test_limiter_blocks_after_threshold(self):
        now = [0]
        limiter = AttemptLimiter(max_failures=2, window_seconds=60, block_seconds=30, clock=lambda: now[0])
        self.assertTrue(limiter.failure("key")[0])
        allowed, retry = limiter.failure("key")
        self.assertFalse(allowed)
        self.assertEqual(retry, 30)
        now[0] = 31
        self.assertTrue(limiter.check("key")[0])

    def test_limiter_success_resets_state(self):
        limiter = AttemptLimiter(max_failures=2)
        limiter.failure("key")
        limiter.success("key")
        self.assertTrue(limiter.check("key")[0])


if __name__ == "__main__":
    unittest.main()
