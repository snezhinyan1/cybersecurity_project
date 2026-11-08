import hashlib
import io
import unittest
from contextlib import redirect_stdout
from importlib import import_module
from itertools import combinations, product
from unittest.mock import patch

from tasks import (
    authenticated_encryption as auth,
    cbc_mode_xor as cbc,
    diffie_hellman as dh,
    hamming_74 as hamming,
    heuristic_analysis as entropy,
    merkle_tree as merkle,
    onion_routing as onion,
    pbkdf2_hashing as passwords,
    proof_of_work as pow_demo,
    shamirs_secret_sharing as shamir,
    steganography_lsb as lsb,
    totp_2fa as totp,
)

ecc = import_module("tasks.elliptic-curve_cryptography")
lwe = import_module("tasks.post-quantum_cryptography")
schnorr = import_module("tasks.zero-knowledge_proof")


class ExistingTasksTests(unittest.TestCase):
    def test_authenticated_encryption(self):
        for text in ("", "Привет! 🙂"):
            ciphertext, tag = auth.authenticated_encrypt(text, b"k", b"mac")
            self.assertEqual(auth.authenticated_decrypt(ciphertext, tag, b"k", b"mac"), text)
        altered = bytes([ciphertext[0] ^ 1]) + ciphertext[1:]
        with self.assertRaises(ValueError):
            auth.authenticated_decrypt(altered, tag, b"k", b"mac")
        for enc_key, mac_key in ((b"", b"mac"), (b"k", b"")):
            with self.assertRaises(ValueError):
                auth.authenticated_encrypt("abc", enc_key, mac_key)

    def test_cbc_lengths_and_padding(self):
        key = b"KEY_1234"
        iv = bytes(8)
        self.assertEqual(len(cbc.cbc_encrypt_mock(b"12345678", key, iv)), 16)
        self.assertNotEqual(cbc.cbc_encrypt_mock(b"A", key, iv), cbc.cbc_encrypt_mock(b"A\0", key, iv))
        with self.assertRaises(ValueError):
            cbc.cbc_encrypt_mock(b"A", key, b"short")
        with self.assertRaises(ValueError):
            cbc.xor_byte_arrays(b"a", b"ab")

    def test_diffie_hellman_all_private_key_pairs(self):
        for alice, bob in product(range(10), repeat=2):
            with patch.object(dh.secrets, "randbelow", side_effect=[alice, bob]):
                secret_a, secret_b = dh.diffie_hellman_exchange()
            self.assertEqual(secret_a, secret_b)
            self.assertNotEqual(secret_a, 1)

    def test_elliptic_curve_addition(self):
        add = ecc.ecc_point_addition
        self.assertEqual(add((5, 1), (5, 1), 2, 17), (6, 3))
        self.assertIsNone(add((5, 1), (22, -1), 2, 17))
        self.assertIsNone(add((0, 0), (0, 0), 2, 17))
        self.assertEqual(add(None, (22, 18), 2, 17), (5, 1))
        with self.assertRaises(ValueError):
            add((5, 1), (5, 1), 2, 15)
        with self.assertRaises(ValueError):
            add((5, 1), (5, 2), 2, 17)
        with self.assertRaises(ValueError):
            add(5, (5, 1), 2, 17)

    def test_hamming_all_words_and_single_errors(self):
        with redirect_stdout(io.StringIO()):
            for original in product((0, 1), repeat=4):
                code = hamming.hamming_74_encode(original)
                self.assertEqual(hamming.hamming_74_decode_and_fix(code), list(original))
                for position in range(7):
                    damaged = code.copy()
                    damaged[position] ^= 1
                    self.assertEqual(hamming.hamming_74_decode_and_fix(tuple(damaged)), list(original))
        with self.assertRaises(ValueError):
            hamming.hamming_74_encode([0, 1, 2, 0])

    def test_entropy_at_different_window_sizes(self):
        self.assertEqual(entropy.find_high_entropy_windows(bytes(8), 8), [])
        self.assertEqual(entropy.find_high_entropy_windows(bytes(range(8)), 8), [(0, 3.0)])
        self.assertEqual(entropy.find_high_entropy_windows(b"abc", 4), [])
        with self.assertRaises(ValueError):
            entropy.find_high_entropy_windows(b"abc", 0)

    def test_merkle_proof_and_tampering(self):
        a, b, c, d = [hashlib.sha256(x).hexdigest() for x in (b"A", b"B", b"C", b"D")]
        left = merkle.hash_node(a, b)
        root = merkle.hash_node(left, merkle.hash_node(c, d))
        proof = [(d, False), (left, True)]
        self.assertTrue(merkle.verify_merkle_proof(c, proof, root))
        self.assertFalse(merkle.verify_merkle_proof(b, proof, root))
        self.assertFalse(merkle.verify_merkle_proof(c, [(d, True), (left, True)], root))

    def test_onion_unicode_and_invalid_keys(self):
        keys = [b"a", b"bc", b"def"]
        with redirect_stdout(io.StringIO()):
            for text in ("", "Привет 🙂"):
                encrypted = onion.onion_encrypt(text, keys)
                self.assertEqual(onion.onion_decrypt(encrypted, keys), text)
        with self.assertRaises(ValueError):
            onion.onion_encrypt("Привет", [b""])

    def test_pbkdf2_password_checks(self):
        salt, key = passwords.generate_password_hash("Пароль 🙂")
        self.assertEqual(len(salt), 16)
        self.assertTrue(passwords.verify_password(salt, key, "Пароль 🙂"))
        self.assertFalse(passwords.verify_password(salt, key, "Пароль"))

    def test_lwe_modular_error(self):
        matrix, values, secret = lwe.generate_postquantum_key(2, 17)
        self.assertEqual((len(matrix), len(values), len(secret)), (2, 2, 2))
        for row, value in zip(matrix, values):
            exact_value = sum(coefficient * item for coefficient, item in zip(row, secret))
            self.assertIn((value - exact_value) % 17, (0, 1, 16))
        with self.assertRaises(ValueError):
            lwe.generate_postquantum_key(0)

    def test_proof_of_work_success_and_search_limit(self):
        nonce, digest, _ = pow_demo.mine_block("abc", 2)
        self.assertTrue(digest.startswith("00"))
        self.assertEqual(digest, hashlib.sha256(f"abc:{nonce}".encode()).hexdigest())
        self.assertEqual(pow_demo.mine_block("abc", 0, max_attempts=1)[0], 0)
        with self.assertRaises(RuntimeError):
            pow_demo.mine_block("abc", 64, max_attempts=1)
        with self.assertRaises(ValueError):
            pow_demo.mine_block("abc", -1)

    def test_shamir_every_triple_and_invalid_shares(self):
        shares = [(x, (42 + 3 * x + 4 * x**2) % 257) for x in range(1, 6)]
        for triple in combinations(shares, 3):
            self.assertEqual(shamir.reconstruct_secret(triple, 257), 42)
        with self.assertRaises(ValueError):
            shamir.reconstruct_secret([(1, 42), (258, 42)], 257)
        with self.assertRaises(ValueError):
            shamir.reconstruct_secret(shares, 25)

    def test_lsb_unicode_capacity_and_terminator(self):
        for text in ("", "Привет\0🙂"):
            length = 8 * (len(text.encode()) + 1)
            encoded = lsb.embed_message(bytes([0xAA]) * length, text)
            self.assertEqual(lsb.extract_message(encoded), text)
            self.assertTrue(all(byte & 0xFE == 0xAA for byte in encoded))
            with self.assertRaises(ValueError):
                lsb.embed_message(bytes(length - 1), text)
        with self.assertRaises(ValueError):
            lsb.extract_message(bytes([1]) * 9)

    def test_totp_reference_codes_and_invalid_step(self):
        # RFC 6238, приложение B. Пример выдаёт шесть младших цифр SHA-1.
        vectors = [(59, "287082"), (1111111109, "081804"), (1111111111, "050471"),
                   (1234567890, "005924"), (2000000000, "279037"), (20000000000, "353130")]
        key = b"12345678901234567890"
        for timestamp, expected in vectors:
            with patch.object(totp.time, "time", return_value=timestamp):
                self.assertEqual(totp.generate_totp_code(key), expected)
        with self.assertRaises(ValueError):
            totp.generate_totp_code(key, 0)

    def test_schnorr_all_challenges_and_nonces(self):
        with redirect_stdout(io.StringIO()):
            for nonce, challenge in product(range(10), repeat=2):
                with patch.object(schnorr.secrets, "randbelow", side_effect=[nonce, challenge]):
                    self.assertTrue(schnorr.zkp_schnorr())
