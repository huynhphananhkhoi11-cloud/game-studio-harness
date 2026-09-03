from __future__ import annotations

import unittest

from scripts import credential_redaction as cr


class CredentialRedactionTests(unittest.TestCase):
    def test_plain_text_is_unchanged(self):
        self.assertEqual(cr.redact_text("metadata only"), "metadata only")

    def test_non_string_redacts(self):
        self.assertEqual(cr.redact_text({"x": 1}), cr.REDACTED)

    def test_bearer_is_detected(self):
        self.assertTrue(cr.contains_secret_like("Bearer ABCDEFGHIJKLMNOP"))

    def test_bearer_is_redacted(self):
        self.assertNotIn("ABCDEFGHIJKLMNOP", cr.redact_text("Bearer ABCDEFGHIJKLMNOP"))

    def test_github_token_shape_is_detected(self):
        self.assertTrue(cr.contains_secret_like("ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234"))

    def test_openai_key_shape_is_detected(self):
        self.assertTrue(cr.contains_secret_like("sk-abcdefghijklmnopqrstuv"))

    def test_password_assignment_is_detected(self):
        self.assertTrue(cr.contains_secret_like("password=synthetic-value"))

    def test_api_key_assignment_is_detected(self):
        self.assertTrue(cr.contains_secret_like("api_key: synthetic-value"))

    def test_url_userinfo_is_detected(self):
        self.assertTrue(cr.contains_secret_like("https://user:password@example.invalid/x"))

    def test_private_key_block_is_detected(self):
        value = "-----BEGIN PRIVATE KEY-----\nSYNTHETIC\n-----END PRIVATE KEY-----"
        self.assertTrue(cr.contains_secret_like(value))

    def test_public_safe_accepts_nested_metadata(self):
        cr.assert_public_safe({"profile": ["credential-profile:x", {"status": "ACTIVE"}]})

    def test_public_safe_rejects_nested_secretlike_text(self):
        with self.assertRaises(cr.SafeCredentialError) as ctx:
            cr.assert_public_safe({"x": ["Bearer ABCDEFGHIJKLMNOP"]})
        self.assertEqual(ctx.exception.code, "SECRET_MATERIAL")

    def test_public_safe_is_bounded(self):
        value = ["safe"] * (cr.MAX_REDACTION_ITEMS + 2)
        with self.assertRaises(cr.SafeCredentialError) as ctx:
            cr.assert_public_safe(value)
        self.assertEqual(ctx.exception.code, "STRUCTURE_LIMIT")

    def test_safe_error_has_fixed_message(self):
        exc = cr.safe_error("LEASE_LIMIT")
        self.assertEqual(exc.code, "LEASE_LIMIT")
        self.assertEqual(exc.safe_message, "requested credential lease exceeds the accepted duration")

    def test_unknown_error_does_not_echo_input(self):
        exc = cr.safe_error("UNTRUSTED secret=abcdefghi")
        self.assertEqual(exc.safe_message, "credential operation rejected")
        self.assertNotIn("abcdefghi", exc.safe_message)

    def test_redaction_is_bounded(self):
        text = "x" * (cr.MAX_REDACTION_CHARS + 50)
        self.assertEqual(len(cr.redact_text(text)), cr.MAX_REDACTION_CHARS)

    def test_synthetic_marker_is_not_mistaken_for_usable_secret(self):
        self.assertFalse(cr.contains_secret_like("NOT_A_REAL_TOKEN_FIXTURE"))

    def test_reference_metadata_is_not_secretlike(self):
        self.assertFalse(cr.contains_secret_like("secret-locator:fixture-001"))

    def test_redact_multiple_patterns(self):
        text = "Bearer ABCDEFGHIJKLMNOP password=synthetic-value"
        redacted = cr.redact_text(text)
        self.assertNotIn("ABCDEFGHIJKLMNOP", redacted)
        self.assertNotIn("synthetic-value", redacted)

    def test_redaction_has_no_empty_output_for_safe_text(self):
        self.assertTrue(cr.redact_text("trace:studio-009c"))


if __name__ == "__main__":
    unittest.main()
