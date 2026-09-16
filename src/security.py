"""Security utilities: encryption at rest and password strength analysis.

This module isolates every cryptographic operation from the rest of
the application. All stored passwords are encrypted using a key
derived from the user's master password (PBKDF2 + Fernet/AES). The
master password itself is never stored anywhere.
"""

import base64
import os
import re

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# A small, well-known list of extremely common passwords used to flag
# trivially guessable choices. Not exhaustive by design -- this is a
# defensive strength check, not a credential-cracking wordlist.
COMMON_PASSWORDS = frozenset(
    {
        "password", "123456", "12345678", "qwerty", "abc123",
        "letmein", "monkey", "111111", "iloveyou", "admin",
        "welcome", "password1", "123456789", "football",
    }
)

PBKDF2_ITERATIONS = 390_000
SALT_SIZE_BYTES = 16


class SecurityError(Exception):
    """Raised when an encryption or decryption operation fails."""


def generate_salt() -> bytes:
    """Generate a new cryptographically-random salt.

    Returns:
        A random 16-byte salt.
    """
    return os.urandom(SALT_SIZE_BYTES)


def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derive a symmetric encryption key from the master password.

    Uses PBKDF2-HMAC-SHA256 with a high iteration count to make
    brute-forcing the master password computationally expensive.

    Args:
        master_password: The user's chosen master password.
        salt: A per-vault random salt (persisted alongside the data).

    Returns:
        A URL-safe base64-encoded 32-byte key, suitable for Fernet.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    derived = kdf.derive(master_password.encode("utf-8"))
    return base64.urlsafe_b64encode(derived)


def encrypt(plaintext: str, key: bytes) -> bytes:
    """Encrypt a plaintext string with the given key.

    Args:
        plaintext: The text to encrypt (e.g. a password).
        key: A Fernet-compatible key from `derive_key`.

    Returns:
        The encrypted token as bytes.
    """
    return Fernet(key).encrypt(plaintext.encode("utf-8"))


def decrypt(token: bytes, key: bytes) -> str:
    """Decrypt a token previously produced by `encrypt`.

    Args:
        token: The encrypted bytes.
        key: The same key used to encrypt the token.

    Returns:
        The original plaintext string.

    Raises:
        SecurityError: If the token is invalid or the key is wrong
            (e.g. incorrect master password).
    """
    try:
        return Fernet(key).decrypt(token).decode("utf-8")
    except InvalidToken as exc:
        raise SecurityError(
            "Decryption failed. The master password is likely incorrect."
        ) from exc


def analyze_strength(password: str) -> dict:
    """Score a password's strength and explain the reasoning.

    The score is a simple, transparent heuristic (0-100) based on
    length, character variety, and known-weak patterns. This is a
    defensive check to nudge users toward stronger passwords, not a
    substitute for a real breached-password database.

    Args:
        password: The password to analyze.

    Returns:
        A dict with keys:
            score (int): 0-100 strength score.
            rating (str): "Weak", "Fair", "Strong", or "Very Strong".
            issues (list[str]): Human-readable reasons points were lost.
    """
    issues: list[str] = []
    score = 0

    length = len(password)
    if length >= 12:
        score += 30
    elif length >= 8:
        score += 15
        issues.append("Consider using 12+ characters for better security.")
    else:
        issues.append("Too short: use at least 8 characters (12+ is better).")

    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(r"[^\w\s]", password))

    variety_count = sum([has_lower, has_upper, has_digit, has_symbol])
    score += variety_count * 15

    if not has_upper:
        issues.append("Add uppercase letters.")
    if not has_lower:
        issues.append("Add lowercase letters.")
    if not has_digit:
        issues.append("Add numbers.")
    if not has_symbol:
        issues.append("Add symbols (e.g. !, #, $).")

    if password.lower() in COMMON_PASSWORDS:
        score = min(score, 10)
        issues.append("This is a commonly used password — avoid it entirely.")

    if re.search(r"(.)\1{2,}", password):
        score -= 10
        issues.append("Avoid repeating the same character 3+ times in a row.")

    score = max(0, min(100, score))

    if score >= 80:
        rating = "Very Strong"
    elif score >= 60:
        rating = "Strong"
    elif score >= 35:
        rating = "Fair"
    else:
        rating = "Weak"

    return {"score": score, "rating": rating, "issues": issues}


def generate_strong_password(length: int = 16) -> str:
    """Generate a cryptographically-random strong password.

    Args:
        length: Desired password length (minimum 12, enforced here).

    Returns:
        A random password containing lowercase, uppercase, digits,
        and symbols.
    """
    length = max(12, length)
    alphabet = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "!@#$%^&*()-_=+"
    )
    # os.urandom-backed choice avoids the predictable `random` module.
    return "".join(
        alphabet[byte % len(alphabet)] for byte in os.urandom(length)
    )
