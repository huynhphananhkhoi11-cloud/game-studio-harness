from __future__ import annotations

import copy
import unittest
from unittest import mock

from scripts import nvidia_nim_session_credential_bridge as b

SECRET = "synthetic_session_secret_0123456789"
AS_OF = "2026-09-08T17:00:00Z"

def lease():
    x = {
        "schema_version": "1.0",
        "credential_lease_id": "credential-lease:" + "a" * 32,
        "credential_profile_id": b.CREDENTIAL_PROFILE_ID,
        "account_ref": b.ACCOUNT_REF,
        "profile_digest": "sha256:" + "b" * 64,
        "subject_ref": b.SUBJECT_REF,
        "capability": b.CAPABILITY,
        "purpose": b.PURPOSE,
        "repository_record_digest": None,
        "operation_digest": None,
        "issued_at": "2026-09-08T16:59:00Z",
        "expires_at": "2026-09-08T17:10:00Z",
        "idempotency_key": "v03-test-0001",
        "canonical_digest": "",
    }
    x["canonical_digest"] = b.canonical_digest(x)
    return x

class NvidiaSessionCredentialBridgeTests(unittest.TestCase):
    def assert_code(self, code, fn, *args, **kwargs):
        with self.assertRaises(b.NvidiaSessionCredentialError) as cm:
            fn(*args, **kwargs)
        self.assertEqual(cm.exception.code, code)
        self.assertNotIn(SECRET, str(cm.exception))

    def test_01_constants(self):
        self.assertEqual(b.CREDENTIAL_PROFILE_ID, "credential-profile:nvidia-nim-api-key")
        self.assertEqual(b.ACCOUNT_REF, "account-ref:nvidia-developer-program-owner-account")

    def test_02_valid_lease(self):
        out = b.validate_lease(lease(), as_of=AS_OF)
        self.assertEqual(out["credential_profile_id"], b.CREDENTIAL_PROFILE_ID)

    def test_03_lease_immutable(self):
        x = lease(); before = copy.deepcopy(x)
        b.validate_lease(x, as_of=AS_OF)
        self.assertEqual(x, before)

    def test_04_bad_profile(self):
        x = lease(); x["credential_profile_id"] = "credential-profile:wrong"; x["canonical_digest"] = b.canonical_digest(x)
        self.assert_code("LEASE_LINEAGE", b.validate_lease, x, as_of=AS_OF)

    def test_05_bad_account_ref(self):
        x = lease(); x["account_ref"] = "account-ref:wrong"; x["canonical_digest"] = b.canonical_digest(x)
        self.assert_code("LEASE_LINEAGE", b.validate_lease, x, as_of=AS_OF)

    def test_06_bad_subject(self):
        x = lease(); x["subject_ref"] = "provider:wrong"; x["canonical_digest"] = b.canonical_digest(x)
        self.assert_code("LEASE_LINEAGE", b.validate_lease, x, as_of=AS_OF)

    def test_07_bad_purpose(self):
        x = lease(); x["purpose"] = "WRONG"; x["canonical_digest"] = b.canonical_digest(x)
        self.assert_code("LEASE_LINEAGE", b.validate_lease, x, as_of=AS_OF)

    def test_08_repository_digest_forbidden(self):
        x = lease(); x["repository_record_digest"] = "sha256:" + "c"*64; x["canonical_digest"] = b.canonical_digest(x)
        self.assert_code("LEASE_LINEAGE", b.validate_lease, x, as_of=AS_OF)

    def test_09_expired(self):
        self.assert_code("LEASE_TIME", b.validate_lease, lease(), as_of="2026-09-08T17:11:00Z")

    def test_10_before_issued(self):
        self.assert_code("LEASE_TIME", b.validate_lease, lease(), as_of="2026-09-08T16:58:59Z")

    def test_11_digest_mismatch(self):
        x = lease(); x["canonical_digest"] = "sha256:" + "0"*64
        self.assert_code("LEASE_DIGEST", b.validate_lease, x, as_of=AS_OF)

    def test_12_extra_field(self):
        x = lease(); x["extra"] = 1
        self.assert_code("INVALID_LEASE", b.validate_lease, x, as_of=AS_OF)

    def test_13_hidden_supplier_success(self):
        out = b.with_secret(lease(), lambda s: {"ok": s == SECRET}, as_of=AS_OF,
                            secret_supplier=lambda: SECRET)
        self.assertEqual(out, {"ok": True})

    def test_14_secret_cannot_escape_result(self):
        self.assert_code("SECRET_ESCAPE", b.with_secret, lease(), lambda s: {"x": s},
                         as_of=AS_OF, secret_supplier=lambda: SECRET)

    def test_15_secret_cannot_escape_exception(self):
        def consumer(s):
            raise ValueError("failure " + s)
        self.assert_code("SECRET_ESCAPE", b.with_secret, lease(), consumer,
                         as_of=AS_OF, secret_supplier=lambda: SECRET)

    def test_16_short_secret(self):
        self.assert_code("INVALID_SECRET", b.with_secret, lease(), lambda s: {},
                         as_of=AS_OF, secret_supplier=lambda: "short")

    def test_17_whitespace_secret(self):
        self.assert_code("INVALID_SECRET", b.with_secret, lease(), lambda s: {},
                         as_of=AS_OF, secret_supplier=lambda: "synthetic secret 012345")

    def test_18_noninteractive_requires_supplier(self):
        with mock.patch.object(b.sys.stdin, "isatty", return_value=False):
            self.assert_code("INTERACTIVE_REQUIRED", b.with_secret, lease(), lambda s: {},
                             as_of=AS_OF)

    def test_19_no_os_import(self):
        self.assertNotIn("os", b.__dict__)

    def test_20_no_subprocess_import(self):
        self.assertNotIn("subprocess", b.__dict__)

    def test_21_no_pathlib_import(self):
        self.assertNotIn("Path", b.__dict__)

    def test_22_canonical_digest_stable(self):
        x = lease()
        self.assertEqual(b.canonical_digest(x), x["canonical_digest"])

    def test_23_invalid_idempotency(self):
        x = lease(); x["idempotency_key"] = "bad"; x["canonical_digest"] = b.canonical_digest(x)
        self.assert_code("INVALID_LEASE", b.validate_lease, x, as_of=AS_OF)

    def test_24_operation_digest_forbidden(self):
        x = lease(); x["operation_digest"] = "sha256:"+"d"*64; x["canonical_digest"] = b.canonical_digest(x)
        self.assert_code("LEASE_LINEAGE", b.validate_lease, x, as_of=AS_OF)
