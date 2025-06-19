import re
import bcrypt

def check_password_strength(plain_text_password: str) -> dict:
    """
    Checks a plain-text password against predefined policy rules.

    Args:
        plain_text_password: The password string to check.

    Returns:
        A dictionary indicating which rules are met, whether all rules are met,
        and a feedback message.
        Example: {
            'length_ok': True,
            'lowercase_ok': True,
            'uppercase_ok': True,
            'digit_ok': True,
            'special_ok': True,
            'overall_ok': True,
            'message': 'Password meets all criteria.'
        }
    """
    if not isinstance(plain_text_password, str):
        # Early exit for non-string input, though type hinting should help prevent this.
        return {
            'length_ok': False,
            'lowercase_ok': False,
            'uppercase_ok': False,
            'digit_ok': False,
            'special_ok': False,
            'overall_ok': False,
            'message': 'Password must be a string.'
        }

    special_chars_pattern = r"[!@#$%^&*()\-_=+\[\]{};:'\",.<>/?]"

    results = {
        'length_ok': len(plain_text_password) >= 12,
        'lowercase_ok': bool(re.search(r"[a-z]", plain_text_password)),
        'uppercase_ok': bool(re.search(r"[A-Z]", plain_text_password)),
        'digit_ok': bool(re.search(r"[0-9]", plain_text_password)),
        'special_ok': bool(re.search(special_chars_pattern, plain_text_password))
    }

    overall_ok = True
    message = 'Password meets all criteria.'

    if not results['length_ok']:
        overall_ok = False
        message = 'Password must be at least 12 characters long.'
    elif not results['lowercase_ok']:
        overall_ok = False
        message = 'Password must include at least one lowercase letter (a-z).'
    elif not results['uppercase_ok']:
        overall_ok = False
        message = 'Password must include at least one uppercase letter (A-Z).'
    elif not results['digit_ok']:
        overall_ok = False
        message = 'Password must include at least one digit (0-9).'
    elif not results['special_ok']:
        overall_ok = False
        message = f"Password must include at least one special character (e.g., {special_chars_pattern})."

    results['overall_ok'] = overall_ok
    results['message'] = message

    return results

def hash_password(plain_text_password: str) -> bytes:
    """
    Hashes a plain-text password using bcrypt.

    Args:
        plain_text_password: The password string to hash.

    Returns:
        The bcrypt hashed password as bytes.

    Raises:
        TypeError: If plain_text_password is not a string.
    """
    if not isinstance(plain_text_password, str):
        raise TypeError("Password must be a string.")

    encoded_password = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(encoded_password, salt)
    return hashed_password

def verify_password(plain_text_password: str, hashed_password: bytes) -> bool:
    """
    Verifies a plain-text password attempt against a stored bcrypt hash.

    Args:
        plain_text_password: The plain-text password attempt (string).
        hashed_password: The stored bcrypt hashed password (bytes).

    Returns:
        True if the password matches the hash, False otherwise.
        Returns False if hashed_password is not a valid bcrypt hash format.

    Raises:
        TypeError: If plain_text_password is not a string or
                   hashed_password is not bytes.
    """
    if not isinstance(plain_text_password, str):
        raise TypeError("Plain text password must be a string.")
    if not isinstance(hashed_password, bytes):
        raise TypeError("Hashed password must be bytes.")

    encoded_password = plain_text_password.encode('utf-8')
    try:
        return bcrypt.checkpw(encoded_password, hashed_password)
    except ValueError:
        # This can happen if hashed_password is not in the expected format for bcrypt
        # (e.g., too short, wrong prefix, etc.)
        return False


if __name__ == '__main__':
    print("--- Testing check_password_strength ---")
    test_passwords = {
        "TooShort": "short",
        "NoLower": "UPPERCASE1!",
        "NoUpper": "lowercase1!",
        "NoDigit": "NoDigitChar!",
        "NoSpecial": "NoSpecial123",
        "Perfect": "ValidPass123!",
        "Empty": "",
        "JustOkay": "Abcdef123!@#" # 12 chars
    }

    for name, pwd in test_passwords.items():
        feedback = check_password_strength(pwd)
        print(f"\nPassword: '{pwd}' ({name})")
        # print(f"  Length OK: {feedback['length_ok']}")
        # print(f"  Lowercase OK: {feedback['lowercase_ok']}")
        # print(f"  Uppercase OK: {feedback['uppercase_ok']}")
        # print(f"  Digit OK: {feedback['digit_ok']}")
        # print(f"  Special OK: {feedback['special_ok']}")
        print(f"  Overall OK: {feedback['overall_ok']}")
        print(f"  Message: {feedback['message']}")

    print("\n--- Testing hash_password and verify_password ---")
    password_to_test = "MyS3cureP@sswOrd!"

    # Test TypeError for hash_password
    try:
        hash_password(12345)
    except TypeError as e:
        print(f"\nSuccessfully caught error for hash_password with non-string: {e}")

    hashed_pw = hash_password(password_to_test)
    print(f"\nOriginal password: {password_to_test}")
    print(f"Hashed password (bytes): {hashed_pw}")
    print(f"Type of hashed_pw: {type(hashed_pw)}")

    # Verification
    is_correct = verify_password(password_to_test, hashed_pw)
    print(f"\nVerification with correct password ('{password_to_test}'): {is_correct}")

    is_incorrect = verify_password("WrongPassword!", hashed_pw)
    print(f"Verification with incorrect password ('WrongPassword!'): {is_incorrect}")

    # Test TypeError for verify_password (plain_text_password)
    try:
        verify_password(123, hashed_pw)
    except TypeError as e:
        print(f"\nSuccessfully caught error for verify_password with non-string plain_text_password: {e}")

    # Test TypeError for verify_password (hashed_password)
    try:
        verify_password(password_to_test, "not_bytes")
    except TypeError as e:
        print(f"\nSuccessfully caught error for verify_password with non-bytes hashed_password: {e}")

    # Test verify_password with malformed hash
    malformed_hash = b"$2b$12$thisisnotarealhash"
    print(f"\nVerification with malformed hash: {verify_password(password_to_test, malformed_hash)}")

    another_password = "anotherTest123!"
    hashed_another = hash_password(another_password)
    print(f"\nVerification of '{password_to_test}' against hash of '{another_password}': {verify_password(password_to_test, hashed_another)}")

    # Salting check: hashing the same password twice should yield different hashes
    hashed_pw1 = hash_password(password_to_test)
    hashed_pw2 = hash_password(password_to_test)
    print(f"\nHash 1 for '{password_to_test}': {hashed_pw1}")
    print(f"Hash 2 for '{password_to_test}': {hashed_pw2}")
    print(f"Are Hash 1 and Hash 2 different? {hashed_pw1 != hashed_pw2}")
    # But both should verify correctly
    print(f"Verification of '{password_to_test}' against Hash 1: {verify_password(password_to_test, hashed_pw1)}")
    print(f"Verification of '{password_to_test}' against Hash 2: {verify_password(password_to_test, hashed_pw2)}")
