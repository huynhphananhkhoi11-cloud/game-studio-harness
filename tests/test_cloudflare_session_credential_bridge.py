from __future__ import annotations
import unittest
from scripts import cloudflare_session_credential_bridge as b

AS_OF = "2026-09-05T08:00:00Z"
ACCOUNT = "0123456789abcdef0123456789abcdef"
SECRET = "cf_test_token_0123456789abcdef"

def lease():
    value = {
        "schema_version": "1.0",
        "credential_lease_id": "credential-lease:" + "a" * 32,
        "credential_profile_id": b.CREDENTIAL_PROFILE_ID,
        "profile_digest": "sha256:" + "1" * 64,
        "subject_ref": b.SUBJECT_REF,
        "capability": b.CAPABILITY,
        "purpose": b.PURPOSE,
        "repository_record_digest": None,
        "operation_digest": None,
        "issued_at": "2026-09-05T07:59:00Z",
        "expires_at": "2026-09-05T08:10:00Z",
        "idempotency_key": "v02-lease-test",
        "canonical_digest": "sha256:" + "0" * 64,
    }
    value["canonical_digest"] = b.canonical_digest(value)
    return value

class CloudflareSessionCredentialBridgeTests(unittest.TestCase):
    def assert_code(self, code, fn):
        with self.assertRaises(b.CloudflareSessionCredentialError) as cm: fn()
        self.assertEqual(cm.exception.code, code)
    def test_01_digest_round_trip(self):
        x = lease(); self.assertEqual(x["canonical_digest"], b.canonical_digest(x))
    def test_02_validate_valid_lease(self):
        self.assertEqual(b.validate_lease(lease(), as_of=AS_OF)["purpose"], b.PURPOSE)
    def test_03_reject_wrong_profile(self):
        x=lease(); x["credential_profile_id"]="credential-profile:wrong"; x["canonical_digest"]=b.canonical_digest(x)
        self.assert_code("LEASE_LINEAGE", lambda: b.validate_lease(x, as_of=AS_OF))
    def test_04_reject_wrong_subject(self):
        x=lease(); x["subject_ref"]="provider:wrong"; x["canonical_digest"]=b.canonical_digest(x)
        self.assert_code("LEASE_LINEAGE", lambda: b.validate_lease(x, as_of=AS_OF))
    def test_05_reject_wrong_purpose(self):
        x=lease(); x["purpose"]="WRONG"; x["canonical_digest"]=b.canonical_digest(x)
        self.assert_code("LEASE_LINEAGE", lambda: b.validate_lease(x, as_of=AS_OF))
    def test_06_reject_expired(self):
        self.assert_code("LEASE_TIME", lambda: b.validate_lease(lease(), as_of="2026-09-05T08:11:00Z"))
    def test_07_reject_digest_mismatch(self):
        x=lease(); x["canonical_digest"]="sha256:"+"2"*64
        self.assert_code("LEASE_DIGEST", lambda: b.validate_lease(x, as_of=AS_OF))
    def test_08_reject_account_length(self):
        self.assert_code("INVALID_ACCOUNT", lambda: b.with_account_and_secret(
            lease(), lambda a,s:{}, as_of=AS_OF, account_supplier=lambda:"abc", secret_supplier=lambda:SECRET))
    def test_09_reject_account_nonhex(self):
        self.assert_code("INVALID_ACCOUNT", lambda: b.with_account_and_secret(
            lease(), lambda a,s:{}, as_of=AS_OF, account_supplier=lambda:"z"*32, secret_supplier=lambda:SECRET))
    def test_10_reject_secret_short(self):
        self.assert_code("INVALID_SECRET", lambda: b.with_account_and_secret(
            lease(), lambda a,s:{}, as_of=AS_OF, account_supplier=lambda:ACCOUNT, secret_supplier=lambda:"short"))
    def test_11_reject_secret_whitespace(self):
        self.assert_code("INVALID_SECRET", lambda: b.with_account_and_secret(
            lease(), lambda a,s:{}, as_of=AS_OF, account_supplier=lambda:ACCOUNT, secret_supplier=lambda:"x"*16+" "))
    def test_12_with_suppliers_success(self):
        out=b.with_account_and_secret(lease(), lambda a,s:{"ok":a==ACCOUNT and s==SECRET}, as_of=AS_OF,
                                      account_supplier=lambda:ACCOUNT, secret_supplier=lambda:SECRET)
        self.assertEqual(out, {"ok":True})
    def test_13_secret_escape_result(self):
        self.assert_code("SECRET_ESCAPE", lambda: b.with_account_and_secret(
            lease(), lambda a,s:{"bad":s}, as_of=AS_OF, account_supplier=lambda:ACCOUNT, secret_supplier=lambda:SECRET))
    def test_14_account_escape_result(self):
        self.assert_code("SECRET_ESCAPE", lambda: b.with_account_and_secret(
            lease(), lambda a,s:{"bad":a}, as_of=AS_OF, account_supplier=lambda:ACCOUNT, secret_supplier=lambda:SECRET))
    def test_15_exception_secret_escape(self):
        def consumer(a,s): raise RuntimeError("provider failed with "+s)
        self.assert_code("SECRET_ESCAPE", lambda: b.with_account_and_secret(
            lease(), consumer, as_of=AS_OF, account_supplier=lambda:ACCOUNT, secret_supplier=lambda:SECRET))
