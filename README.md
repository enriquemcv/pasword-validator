## Authentication Utilities (`auth.py`)

This module provides core functions for user authentication, focusing on secure password handling.

### Features:

-   **`check_password_strength(plain_text_password: str) -> dict`**:
    -   Validates a given plain-text password against a predefined security policy.
    -   Checks for minimum length, presence of uppercase and lowercase letters, digits, and special characters.
    -   Returns a dictionary indicating which criteria are met and an overall status, along with a feedback message.

-   **`hash_password(plain_text_password: str) -> bytes`**:
    -   Takes a plain-text password and securely hashes it using the `bcrypt` algorithm.
    -   Automatically handles salt generation.
    -   Returns the resulting hash as a byte string, suitable for storage.

-   **`verify_password(plain_text_password: str, hashed_password: bytes) -> bool`**:
    -   Compares a plain-text password attempt against a stored `bcrypt` hash.
    -   Returns `True` if the password matches the hash, `False` otherwise.

### Testing:

Unit tests for these utilities are available in `test_auth.py`, ensuring functionality and reliability.

### Dependencies:

-   `bcrypt`: Required for hashing and verification. Ensure it is installed (`pip install bcrypt`).
