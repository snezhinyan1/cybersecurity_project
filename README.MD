*[🇷🇺 Читать на русском языке](README.ru.md)*

# Cybersecurity Applications in Computer Science

Welcome to the educational cybersecurity project repository!
This project was created to visually demonstrate how fundamental cryptographic algorithms and information security concepts work. All algorithms are written from scratch in pure Python to reveal their internal mathematical logic without relying on pre-built, black-box cryptographic libraries.

## Zero Dependencies

Unlike many modern solutions, this project has no external dependencies. To run and test any of the algorithms, all you need is an installed **Python 3.6+** interpreter. You will not need to use `pip`, create virtual environments, or install third-party packages.

## Implemented Algorithms

The project includes 15 thematic scripts located in the `tasks/` directory. Each script represents a distinct security concept (*15 tasks*):

1. **`authenticated_encryption.py`** — Authenticated Encryption (AEAD).
2. **`elliptic-curve_cryptography.py`** — Elliptic Curve Cryptography (ECC).
3. **`hamming_74.py`** — Error-Correcting Code (Hamming Code 7,4).
4. **`heuristic_analysis.py`** — Heuristic Analyzer.
5. **`merkle_tree.py`** — Merkle Tree.
6. **`onion_routing.py`** — Onion Routing.
7. **`post-quantum_cryptography.py`** — Post-Quantum Cryptography.
8. **`proof_of_work.py`** — Proof-of-Work Algorithm.
9. **`shamirs_secret_sharing.py`** — Shamir's Secret Sharing.
10. **`zero-knowledge_proof.py`** — Zero-Knowledge Proof (ZKP).
11. **`steganography_lsb.py`** — Steganography (LSB Data Embedding).
12. **`totp_2fa.py`** — Two-Factor Authentication (TOTP Code Generation).
13. **`diffie_hellman.py`** — Diffie-Hellman Key Exchange Algorithm.
14. **`pbkdf2_hashing.py`** — Salted Password Hashing using PBKDF2.
15. **`cbc_mode_xor.py`** — Cipher Block Chaining (CBC) Mode Simulation.

## Downloading the Source Code

You can clone the repository to your local machine using the terminal:

```sh
git clone [https://github.com/snezhinyan1/cybersecurity_project](https://github.com/snezhinyan1/cybersecurity_project)
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

## Legal and Licensing

This project is distributed under the [MIT License][mit].

[mit]: LICENSE.txt

### Disclaimer

> [!Important]
> The code provided in this repository is developed **strictly for educational purposes** to demonstrate the mathematical principles of information security. These scripts are not intended for encrypting real confidential or commercial data in a production environment.

## Contributing and Development

If you want to suggest improvements, optimize algorithms, or add new concepts from the computer science curriculum, feel free to open an [Issue][issues] or submit a Pull Request.

[issues]: https://github.com/snezhinyan1/cybersecurity_project/issues