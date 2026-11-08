import hashlib
from pathlib import Path
import string
from tempfile import TemporaryDirectory
import unittest

from tasks.access_control import can_access
from tasks.file_integrity import file_sha256
from tasks.hmac_authentication import sign_document, verify_document
from tasks.password_generator import generate_password
from tasks.password_policy import check_password_rules


class PasswordPolicyTests(unittest.TestCase):
    def test_complete_and_empty_password(self):
        self.assertEqual(check_password_rules("SchoolProject7!"), [])
        self.assertEqual(len(check_password_rules("")), 5)

    def test_each_rule_independently(self):
        for password in ("Aa1!", "ABCDEFGHIJK1!", "abcdefghijk1!", "Abcdefghijkl!", "Abcdefghijkl1"):
            with self.subTest(password=password):
                self.assertEqual(len(check_password_rules(password)), 1)

    def test_exact_length_and_unicode(self):
        self.assertEqual(check_password_rules("Abcdefghij1!"), [])
        self.assertEqual(check_password_rules("ЯaA1!😀", min_length=6), [])
        self.assertEqual(len(check_password_rules("Пароль１２３!", min_length=1)), 3)

    def test_invalid_minimum(self):
        for minimum in (0, -1, 1.5, True):
            with self.subTest(minimum=minimum), self.assertRaises(ValueError):
                check_password_rules("Aa1!", minimum)


class PasswordGeneratorTests(unittest.TestCase):
    def test_lengths_characters_and_required_groups(self):
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        for length in (4, 12, 16, 100):
            for _ in range(10):
                password = generate_password(length)
                self.assertEqual(len(password), length)
                self.assertTrue(all(character in alphabet for character in password))
                self.assertEqual(check_password_rules(password, min_length=length), [])

    def test_default_length(self):
        self.assertEqual(len(generate_password()), 16)

    def test_invalid_length(self):
        for length in (-1, 0, 3, 4.5, "16", True):
            with self.subTest(length=length), self.assertRaises(ValueError):
                generate_password(length)


class FileIntegrityTests(unittest.TestCase):
    def test_known_digest_and_changed_document(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "документ.txt"
            path.write_bytes(b"abc")
            original = file_sha256(path)
            self.assertEqual(original, "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
            self.assertEqual(file_sha256(str(path)), original)
            path.write_bytes(b"abd")
            self.assertNotEqual(file_sha256(path), original)

    def test_empty_file(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "empty"
            path.write_bytes(b"")
            self.assertEqual(file_sha256(path), "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

    def test_multiple_chunks(self):
        content = bytes(range(256)) * 1025
        with TemporaryDirectory() as directory:
            path = Path(directory) / "large.bin"
            path.write_bytes(content)
            self.assertEqual(file_sha256(path), hashlib.sha256(content).hexdigest())

    def test_missing_file(self):
        with TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                file_sha256(Path(directory) / "missing")


class HmacAuthenticationTests(unittest.TestCase):
    def test_rfc_4231_sha256_vector(self):
        # RFC 4231, test case 1.
        signature = sign_document(b"Hi There", b"\x0b" * 20)
        self.assertEqual(signature.hex(), "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7")

    def test_original_changed_and_wrong_key(self):
        document = "Документ 😀".encode("utf-8")
        key = b"secret key"
        signature = sign_document(document, key)
        self.assertTrue(verify_document(document, signature, key))
        self.assertFalse(verify_document(document + b"!", signature, key))
        self.assertFalse(verify_document(document, signature, b"wrong key"))
        self.assertFalse(verify_document(document, signature[:-1], key))
        self.assertFalse(verify_document(document, b"", key))

    def test_empty_document(self):
        signature = sign_document(b"", b"key")
        self.assertTrue(verify_document(b"", signature, b"key"))

    def test_empty_key(self):
        with self.assertRaises(ValueError):
            sign_document(b"document", b"")
        with self.assertRaises(ValueError):
            verify_document(b"document", b"signature", b"")


class AccessControlTests(unittest.TestCase):
    def test_entire_role_action_table(self):
        expected = {
            "viewer": [True, False, False],
            "editor": [True, True, False],
            "admin": [True, True, True],
        }
        for role, decisions in expected.items():
            for action, decision in zip(("read", "edit", "delete"), decisions):
                with self.subTest(role=role, action=action):
                    self.assertIs(can_access(role, action), decision)

    def test_unknown_role_action_and_case(self):
        for role, action in (("unknown", "read"), ("", "read"), ("Admin", "delete"), ("admin", "execute"), ("admin", ""), ("admin", "READ")):
            with self.subTest(role=role, action=action):
                self.assertFalse(can_access(role, action))


if __name__ == "__main__":
    unittest.main()
