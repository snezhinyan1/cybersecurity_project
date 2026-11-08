*[🇷🇺 Читать на русском языке](README.ru.md)*

# Cybersecurity Applications in Computer Science

Welcome to the educational cybersecurity project repository!
This project demonstrates how cryptographic algorithms and information security concepts work. The examples use Python's standard library for building blocks such as hashes and HMAC.

## Zero Dependencies

The examples were tested with **Python 3.14**. They run with the standard library.

## Practical tasks

The project includes **25 practical tasks** with Python solutions in `tasks/`. See the [task collection in Russian](TASKS.ru.md) for instructions and expected results.

1. **`authenticated_encryption.py`** — Educational XOR + HMAC example.
2. **`elliptic-curve_cryptography.py`** — Point addition on an elliptic curve.
3. **`hamming_74.py`** — Error-Correcting Code (Hamming Code 7,4).
4. **`heuristic_analysis.py`** — Finding high-entropy regions.
5. **`merkle_tree.py`** — Merkle Tree.
6. **`onion_routing.py`** — Onion Routing.
7. **`post-quantum_cryptography.py`** — A two-equation example of Learning With Errors (LWE).
8. **`proof_of_work.py`** — Proof-of-Work by searching for a hash with leading hexadecimal zeros.
9. **`shamirs_secret_sharing.py`** — Reconstructing a secret from Shamir shares.
10. **`zero-knowledge_proof.py`** — Zero-Knowledge Proof (ZKP).
11. **`steganography_lsb.py`** — Steganography (LSB Data Embedding).
12. **`totp_2fa.py`** — Two-Factor Authentication (TOTP Code Generation).
13. **`diffie_hellman.py`** — Diffie-Hellman Key Exchange Algorithm.
14. **`pbkdf2_hashing.py`** — Salted Password Hashing using PBKDF2.
15. **`cbc_mode_xor.py`** — Cipher Block Chaining (CBC) Mode Simulation.
16. **`password_policy.py`** — Checking classroom password rules.
17. **`password_generator.py`** — Generating a random password.
18. **`file_integrity.py`** — Checking file integrity.
19. **`hmac_authentication.py`** — Authenticating a document with HMAC.
20. **`access_control.py`** — Role-based access control.
21. **`caesar_cipher.py`** — Caesar cipher.
22. **`secure_file_paths.py`** — Checking file paths.
23. **`login_rate_limit.py`** — Temporary login lockout.
24. **`parameterized_queries.py`** — Parameterized SQLite query.
25. **`data_masking.py`** — Masking an email address.

## Downloading the Source Code

You can clone the repository to your local machine using the terminal:

```sh
git clone https://github.com/snezhinyan1/cybersecurity_project
cd cybersecurity_project
```

## Running the Project

| Windows                    | Linux / macOS                   |
|----------------------------|---------------------------------|
| `python tasks/filename.py` | `python3 tasks/filename.py`     |

For example, to run the Zero-Knowledge Proof demonstration, execute:

```sh
python tasks/zero-knowledge_proof.py
```

## Running the tests

From the project folder, run:

```sh
python -m unittest discover -s tests -v
```

On Linux and macOS, use `python3` in the same command.

## Legal and Licensing

This project is distributed under the [MIT License][mit].

[mit]: LICENSE.txt

### Disclaimer

> [!Important]
> The code provided in this repository is developed **strictly for educational purposes** to demonstrate the mathematical principles of information security. These scripts are not intended for encrypting real confidential or commercial data in a production environment.

## Contributing and Development

If you want to suggest improvements, optimize algorithms, or add new concepts from the computer science curriculum, feel free to open an [Issue][issues] or submit a Pull Request.

[issues]: https://github.com/snezhinyan1/cybersecurity_project/issues
