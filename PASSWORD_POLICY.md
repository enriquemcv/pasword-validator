# Password Policy

This document outlines the password policy requirements for user accounts.

## Requirements

Passwords must meet the following criteria to be considered strong and secure:

1.  **Minimum Length:** Passwords must be at least **12 characters** long.

2.  **Complexity:** Passwords must include a mix of character types. They must contain at least one character from each of the following categories:
    *   At least one **uppercase letter** (A-Z).
    *   At least one **lowercase letter** (a-z).
    *   At least one **digit** (0-9).
    *   At least one **special character** (e.g., !@#$%^&*).

3.  **Common Passwords (Recommendation):**
    *   Passwords should not be commonly used or easily guessable.
    *   *Recommendation for implementation:* Check passwords against a database of known breached or common passwords (e.g., Have I Been Pwned Pwned Passwords list).

4.  **Sequences (Recommendation):**
    *   Passwords should not contain easily guessable sequences, such as:
        *   Keyboard sequences (e.g., "qwerty", "asdfgh").
        *   Numeric sequences (e.g., "123456", "987654").
        *   Alphabetical sequences (e.g., "abcdef", "zyxwvu").
    *   *Recommendation for implementation:* Implement checks to detect and disallow such sequences.

## Password Changes

*   Users may be required to change their passwords periodically (e.g., every 90 days).
*   Passwords that have been used previously should not be reused.

## Security Best Practices

*   Users should not share their passwords with anyone.
*   Users should avoid writing down their passwords. If a password must be written down, it should be stored securely.
*   Use unique passwords for different accounts and services.
*   Enable multi-factor authentication (MFA) wherever available.

This policy aims to enhance the security of user accounts and protect sensitive information. Adherence to these guidelines is mandatory for all users.
