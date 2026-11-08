import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

from tasks.caesar_cipher import shift_text
from tasks.data_masking import mask_email
from tasks.login_rate_limit import LoginLimiter
from tasks.parameterized_queries import find_user
from tasks.secure_file_paths import resolve_safe_path


class CaesarCipherTests(unittest.TestCase):
    def test_wraps_both_cases_and_preserves_other_characters(self):
        self.assertEqual(shift_text("Abc XYZ 123 Привет!", 3), "Def ABC 123 Привет!")

    def test_negative_large_and_empty_input(self):
        self.assertEqual(shift_text("AbZ", -1), "ZaY")
        self.assertEqual(shift_text("AbZ", 26 * 100), "AbZ")
        self.assertEqual(shift_text("", -100), "")

    def test_inverse_for_all_shifts(self):
        original = "AZaz-Ж-😀"
        for shift in range(-52, 53):
            with self.subTest(shift=shift):
                self.assertEqual(shift_text(shift_text(original, shift), -shift), original)

    def test_rejects_noninteger_shift(self):
        for shift in (1.5, True, "3"):
            with self.subTest(shift=shift), self.assertRaises(ValueError):
                shift_text("test", shift)


class SafePathTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.base = self.root / "allowed"
        self.base.mkdir()

    def test_allows_normalized_internal_path(self):
        self.assertEqual(
            resolve_safe_path(self.base, "folder/../document.txt"),
            self.base.resolve() / "document.txt",
        )

    def test_rejects_parent_traversal_and_similar_prefix(self):
        for path in ("../private.txt", "../allowed-other/document.txt"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                resolve_safe_path(self.base, path)

    def test_rejects_absolute_path_even_inside_base(self):
        with self.assertRaises(ValueError):
            resolve_safe_path(self.base, self.base / "document.txt")

    @unittest.skipUnless(os.name == "nt", "Зарезервированные имена Windows")
    def test_rejects_windows_device_names_and_alternate_streams(self):
        for path in ("NUL.txt", "report.txt:hidden"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                resolve_safe_path(self.base, path)

    def test_requires_existing_base_directory(self):
        with self.assertRaises(FileNotFoundError):
            resolve_safe_path(self.root / "missing", "document.txt")
        file_path = self.root / "file.txt"
        file_path.write_text("test", encoding="utf-8")
        with self.assertRaises(NotADirectoryError):
            resolve_safe_path(file_path, "document.txt")

    def test_rejects_symbolic_link_to_outside(self):
        outside = self.root / "private"
        outside.mkdir()
        link = self.base / "shortcut"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"Создание символических ссылок недоступно: {error}")
        with self.assertRaises(ValueError):
            resolve_safe_path(self.base, "shortcut/secret.txt")


class LoginLimiterTests(unittest.TestCase):
    def test_blocks_exactly_after_limit_and_expires_at_boundary(self):
        limiter = LoginLimiter(max_attempts=3, block_seconds=60)
        self.assertTrue(limiter.record_result("alice", False, 0))
        self.assertTrue(limiter.record_result("alice", False, 1))
        self.assertTrue(limiter.can_attempt("alice", 1))
        self.assertTrue(limiter.record_result("alice", False, 2))
        self.assertFalse(limiter.can_attempt("alice", 61.9))
        self.assertTrue(limiter.can_attempt("alice", 62))
        self.assertNotIn("alice", limiter.failures)

    def test_success_resets_previous_failures(self):
        limiter = LoginLimiter(max_attempts=2)
        limiter.record_result("alice", False, 0)
        limiter.record_result("alice", True, 1)
        limiter.record_result("alice", False, 2)
        self.assertTrue(limiter.can_attempt("alice", 2))

    def test_blocked_results_do_not_unlock_or_extend_block(self):
        limiter = LoginLimiter(max_attempts=1, block_seconds=10)
        limiter.record_result("alice", False, 0)
        self.assertFalse(limiter.record_result("alice", True, 3))
        self.assertFalse(limiter.record_result("alice", False, 4))
        self.assertEqual(limiter.blocked_until["alice"], 10)
        self.assertTrue(limiter.can_attempt("alice", 10))

    def test_accounts_are_independent(self):
        limiter = LoginLimiter(max_attempts=1)
        limiter.record_result("alice", False, 0)
        self.assertFalse(limiter.can_attempt("alice", 1))
        self.assertTrue(limiter.can_attempt("bob", 1))

    def test_invalid_settings(self):
        for attempts in (0, -1, 1.5, True):
            with self.subTest(attempts=attempts), self.assertRaises(ValueError):
                LoginLimiter(max_attempts=attempts)
        for seconds in (0, -1, float("nan"), float("inf")):
            with self.subTest(seconds=seconds), self.assertRaises(ValueError):
                LoginLimiter(block_seconds=seconds)

    def test_rejects_invalid_time_name_and_result(self):
        limiter = LoginLimiter()
        self.assertTrue(limiter.can_attempt("alice", 10))
        for now in (9, -1, float("nan"), float("inf")):
            with self.subTest(now=now), self.assertRaises(ValueError):
                limiter.can_attempt("alice", now)
        with self.assertRaises(ValueError):
            limiter.can_attempt("", 10)
        with self.assertRaises(ValueError):
            limiter.record_result("alice", "False", 10)


class ParameterizedQueryTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.connection.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE)"
        )
        self.connection.executemany(
            "INSERT INTO users (id, username) VALUES (?, ?)",
            [(1, "alice"), (2, "O'Connor"), (3, "Анна")],
        )

    def test_normal_quoted_and_unicode_names(self):
        self.assertEqual(find_user(self.connection, "alice"), (1, "alice"))
        self.assertEqual(find_user(self.connection, "O'Connor"), (2, "O'Connor"))
        self.assertEqual(find_user(self.connection, "Анна"), (3, "Анна"))

    def test_missing_and_empty_names(self):
        self.assertIsNone(find_user(self.connection, "missing"))
        self.assertIsNone(find_user(self.connection, ""))

    def test_sql_text_cannot_change_query_or_delete_table(self):
        for name in ("' OR 1=1 --", "'; DROP TABLE users; --"):
            with self.subTest(name=name):
                self.assertIsNone(find_user(self.connection, name))
        self.assertEqual(self.connection.execute("SELECT COUNT(*) FROM users").fetchone()[0], 3)

    def test_sql_text_can_be_an_exact_username(self):
        name = "' OR 1=1 --"
        self.connection.execute("INSERT INTO users (username) VALUES (?)", (name,))
        self.assertEqual(find_user(self.connection, name), (4, name))


class DataMaskingTests(unittest.TestCase):
    def test_masks_local_part_preserving_domain(self):
        self.assertEqual(mask_email("student@example.org"), "s***@example.org")
        self.assertEqual(mask_email("Name+tag@sub.example.org"), "N***@sub.example.org")

    def test_hides_single_character_and_uses_fixed_mask_length(self):
        self.assertEqual(mask_email("a@example.org"), "***@example.org")
        self.assertEqual(mask_email("ab@example.org"), mask_email("abcdefgh@example.org"))

    def test_rejects_malformed_or_unsupported_addresses(self):
        invalid = (
            "", "no-at", "a@@example.org", "@example.org", "a@", "a@example",
            "a@.example.org", "a@-example.org", "a@exam_ple.org",
            "a b@example.org", "a..b@example.org", ".a@example.org",
            "a.@example.org", "имя@example.org", "a@example.org\n", None,
        )
        for email in invalid:
            with self.subTest(email=email), self.assertRaises(ValueError):
                mask_email(email)


if __name__ == "__main__":
    unittest.main()
