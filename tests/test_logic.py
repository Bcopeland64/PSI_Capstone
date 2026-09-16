"""Unit tests for src/security.py, src/utils.py, and src/logic.py.

Run with:
    pytest
"""

import pytest

from src.logic import export_report_to_csv, find_reused_passwords, vault_health_report
from src.models import Credential
from src.security import (
    SecurityError,
    analyze_strength,
    decrypt,
    derive_key,
    encrypt,
    generate_salt,
    generate_strong_password,
)
from src.utils import (
    ValidationError,
    validate_master_password,
    validate_positive_int,
    validate_service,
    validate_username,
)


@pytest.fixture
def sample_credentials() -> list[Credential]:
    """A small, fixed set of credentials used across several tests."""
    return [
        Credential(entry_id=1, service="GitHub", username="dev@example.com",
                   password="Str0ng!Passw0rd#1"),
        Credential(entry_id=2, service="Email", username="dev@example.com",
                   password="Str0ng!Passw0rd#1"),  # reused on purpose
        Credential(entry_id=3, service="Forum", username="dev123",
                   password="password"),
    ]


# ---- security.py: encryption tests ------------------------------------


def test_encrypt_decrypt_roundtrip():
    salt = generate_salt()
    key = derive_key("my-master-password", salt)
    token = encrypt("super-secret", key)
    assert decrypt(token, key) == "super-secret"


def test_decrypt_fails_with_wrong_key():
    salt = generate_salt()
    correct_key = derive_key("correct-password", salt)
    wrong_key = derive_key("wrong-password", salt)
    token = encrypt("super-secret", correct_key)

    with pytest.raises(SecurityError):
        decrypt(token, wrong_key)


def test_derive_key_is_deterministic_for_same_salt():
    salt = generate_salt()
    key1 = derive_key("password123", salt)
    key2 = derive_key("password123", salt)
    assert key1 == key2


# ---- security.py: strength analysis tests ------------------------------


def test_analyze_strength_flags_common_password():
    result = analyze_strength("password")
    assert result["rating"] == "Weak"
    assert any("commonly used" in issue for issue in result["issues"])


def test_analyze_strength_rewards_long_varied_password():
    result = analyze_strength("Tr0ub4dor&3xtra!Long")
    assert result["score"] >= 60
    assert result["rating"] in ("Strong", "Very Strong")


def test_generate_strong_password_length_and_charset():
    password = generate_strong_password(20)
    assert len(password) == 20
    result = analyze_strength(password)
    assert result["rating"] in ("Strong", "Very Strong")


def test_generate_strong_password_enforces_minimum_length():
    password = generate_strong_password(4)
    assert len(password) == 12


# ---- utils.py tests -----------------------------------------------------


def test_validate_master_password_rejects_short():
    with pytest.raises(ValidationError):
        validate_master_password("short")


def test_validate_master_password_accepts_valid():
    assert validate_master_password("longenough1") == "longenough1"


def test_validate_service_rejects_empty():
    with pytest.raises(ValidationError):
        validate_service("   ")


def test_validate_username_rejects_empty():
    with pytest.raises(ValidationError):
        validate_username("")


def test_validate_positive_int_rejects_negative():
    with pytest.raises(ValidationError):
        validate_positive_int("-5", field_name="length")


def test_validate_positive_int_accepts_valid():
    assert validate_positive_int("16", field_name="length") == 16


# ---- logic.py tests -------------------------------------------------------


def test_find_reused_passwords_detects_reuse(sample_credentials):
    reused = find_reused_passwords(sample_credentials)
    assert len(reused) == 1
    services = list(reused.values())[0]
    assert set(services) == {"GitHub", "Email"}


def test_find_reused_passwords_empty_when_all_unique():
    creds = [
        Credential(entry_id=1, service="A", username="u", password="Unique1!Aa"),
        Credential(entry_id=2, service="B", username="u", password="Unique2!Bb"),
    ]
    assert find_reused_passwords(creds) == {}


def test_vault_health_report_handles_empty_vault():
    assert vault_health_report([]) == "Vault is empty -- no credentials to analyze."


def test_vault_health_report_warns_about_reuse(sample_credentials):
    report = vault_health_report(sample_credentials)
    assert "Reused passwords detected" in report


def test_vault_health_report_never_contains_plaintext_password(sample_credentials):
    report = vault_health_report(sample_credentials)
    assert "Str0ng!Passw0rd#1" not in report


def test_export_report_to_csv_excludes_passwords(tmp_path, sample_credentials):
    output_file = tmp_path / "report.csv"
    count = export_report_to_csv(sample_credentials, str(output_file))

    assert count == 3
    content = output_file.read_text(encoding="utf-8")
    assert "Str0ng!Passw0rd#1" not in content
    assert "GitHub" in content
    assert "strength_rating" in content
