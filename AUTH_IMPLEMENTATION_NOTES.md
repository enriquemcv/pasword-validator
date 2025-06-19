# Password Hashing with bcrypt - Implementation Plan for auth.py

This document describes the planned implementation for password hashing and verification using the **bcrypt** algorithm within an `auth.py` module.

## 1. Choice of Hashing Algorithm

We will use **bcrypt** as the password hashing algorithm. Bcrypt is a strong, adaptive hashing algorithm specifically designed for passwords. It incorporates a work factor (cost factor) that can be adjusted over time to keep up with hardware improvements, making it resistant to brute-force attacks.

## 2. Salt Generation

Bcrypt's library functions handle salt generation internally. When a password is hashed using bcrypt, a unique salt is automatically generated and incorporated into the resulting hash string. This means our code does **not** need a separate step or function to generate salts. The salt is stored as part of the hash output itself.

## 3. Password Hashing Function

We will define a conceptual function for hashing passwords:

```python
def hash_password(plain_text_password: str) -> bytes:
    """
    Hashes a plain-text password using bcrypt and returns the hashed password.

    Args:
        plain_text_password: The password string to hash.

    Returns:
        The bcrypt hashed password as bytes.
    """
    # Ensure the password is a string
    if not isinstance(plain_text_password, str):
        raise TypeError("Password must be a string.")

    # Encode the plain-text password to bytes (UTF-8 is common)
    password_bytes = plain_text_password.encode('utf-8')

    # Generate a salt and hash the password using the bcrypt library
    # The bcrypt library typically handles salt generation automatically
    # Example using a hypothetical 'bcrypt_library':
    # hashed_password_bytes = bcrypt_library.hashpw(password_bytes, bcrypt_library.gensalt())

    # For the purpose of this description, we'll assume a library function exists.
    # Let's say the library is 'bcrypt':
    # import bcrypt # Hypothetical import
    # hashed_password_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # This function would return the resultant hash as bytes.
    # For now, we'll return a placeholder representing the concept.
    # In a real implementation, this would be:
    # import bcrypt
    # salt = bcrypt.gensalt()
    # hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    # return hashed_password_bytes

    # Placeholder for conceptual description:
    print(f"Conceptual: Hashing password '{plain_text_password}' using bcrypt.")
    # This would be replaced by actual bcrypt library calls.
    # e.g., return bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return b"conceptual_bcrypt_hash_for_" + password_bytes
}
```

**Logic:**
1.  The function accepts a `plain_text_password` (string).
2.  The password string is encoded into bytes (e.g., UTF-8), as cryptographic functions typically operate on bytes.
3.  A bcrypt library function (e.g., `bcrypt.hashpw` with `bcrypt.gensalt`) is called. This function:
    *   Generates a cryptographically secure salt.
    *   Combines the salt with the password bytes.
    *   Applies the bcrypt hashing algorithm for a configured number of rounds (work factor).
4.  The resulting hash (which includes the salt and work factor information) is returned as `bytes`.

## 4. Password Verification Function

We will define a conceptual function for verifying passwords:

```python
def verify_password(plain_text_password: str, hashed_password: bytes) -> bool:
    """
    Verifies a plain-text password attempt against a stored bcrypt hash.

    Args:
        plain_text_password: The plain-text password attempt (string).
        hashed_password: The stored bcrypt hashed password (bytes).

    Returns:
        True if the password matches the hash, False otherwise.
    """
    # Ensure inputs are of the correct type
    if not isinstance(plain_text_password, str):
        raise TypeError("Plain text password must be a string.")
    if not isinstance(hashed_password, bytes):
        raise TypeError("Hashed password must be bytes.")

    # Encode the plain-text password attempt to bytes
    password_bytes_attempt = plain_text_password.encode('utf-8')

    # Use the bcrypt library to check the password against the stored hash
    # The library will extract the salt and work factor from the 'hashed_password'
    # and use them to hash the 'password_bytes_attempt' for comparison.
    # Example using a hypothetical 'bcrypt_library':
    # return bcrypt_library.checkpw(password_bytes_attempt, hashed_password)

    # For the purpose of this description, we'll assume a library function exists.
    # Let's say the library is 'bcrypt':
    # import bcrypt # Hypothetical import
    # return bcrypt.checkpw(password_bytes_attempt, hashed_password)

    # Placeholder for conceptual description:
    print(f"Conceptual: Verifying password '{plain_text_password}' against stored hash.")
    # This would be replaced by actual bcrypt library calls.
    # e.g., return bcrypt.checkpw(password_bytes_attempt, hashed_password)
    # For this conceptual placeholder, we'll simulate a match if the plain text password
    # (when encoded) is part of the conceptual hash placeholder created above.
    return password_bytes_attempt in hashed_password
}
```

**Logic:**
1.  The function accepts a `plain_text_password` attempt (string) and the `hashed_password` (bytes) retrieved from storage.
2.  The `plain_text_password` attempt is encoded into bytes.
3.  A bcrypt library function (e.g., `bcrypt.checkpw`) is called. This function:
    *   Parses the provided `hashed_password` to extract the original salt, work factor, and the actual hash.
    *   Uses the extracted salt and work factor to hash the `password_bytes_attempt`.
    *   Compares the newly generated hash with the hash extracted from `hashed_password` in a way that is safe against timing attacks.
4.  Returns `True` if the hashes match, indicating the password is correct, and `False` otherwise.

This plan provides a foundation for implementing secure password storage using bcrypt in `auth.py`.
The actual implementation will require installing and using a Python bcrypt library (e.g., the `bcrypt` package).

## 5. Integration with User Registration Process

This section describes how the `hash_password` function is integrated into the user registration flow, assuming a hypothetical user registration function within `auth.py`.

### 5.1. Locate Registration Logic

We assume a hypothetical function `register_user(username: str, plain_text_password: str, email: str)` exists within the `auth.py` module. This function is responsible for handling new user sign-ups.

```python
# Conceptual representation of the registration function in auth.py
def register_user(username: str, plain_text_password: str, email: str):
    """
    Handles new user registration.
    This is a conceptual function.
    """
    # ... (validation of username, email, password policy etc.)

    # Hashing the password before storage
    hashed_pw = hash_password(plain_text_password) # Call to our hashing function

    # Storing user details
    # store_user_in_database(username, hashed_pw, email)
    print(f"Conceptual: Registering user '{username}' with email '{email}'.")
    print(f"Conceptual: Storing hashed password: {hashed_pw}")

    # ... (handle success or failure of storage)
    return True # Placeholder
}
```

### 5.2. Hashing Step

Before any user information is saved, the `plain_text_password` provided to the `register_user` function **must** be processed by our `hash_password` function (detailed in Section 3).

```python
    # Inside register_user function:
    # ...
    # plain_text_password_from_form = "UserS_P@sswOrd123" # Example input
    # hashed_user_password = hash_password(plain_text_password_from_form)
    # ...
```
This step converts the user's chosen password into a secure bcrypt hash.

### 5.3. Storing Hashed Password

The output from `hash_password` (i.e., the `hashed_user_password` which is in bytes) is what must be stored in the user database or chosen data store. **The original plain-text password must not be stored under any circumstances.**

The database record for a user would typically include fields such as `username`, `email`, and `password_hash` (storing the output of `hash_password`).

### 5.4. Error Handling

While detailed error handling isbeyond this conceptual description, a robust implementation should consider potential errors during the hashing process. For instance:
*   The `hash_password` function itself might raise an exception (e.g., if the underlying bcrypt library encounters an issue, though this is rare for hashing itself).
*   The system should gracefully handle such errors, perhaps by logging the issue and returning an appropriate error message to the user (e.g., "Registration failed, please try again later.").

This ensures that the plain-text password is never stored, significantly enhancing the security of user credentials.

## 6. Integration with User Login Process

This section describes how the `verify_password` function is integrated into the user login flow, assuming a hypothetical user login function within `auth.py`.

### 6.1. Locate Login Logic

We assume a hypothetical function `login_user(username: str, plain_text_password_attempt: str)` exists within the `auth.py` module. This function handles attempts by users to sign in.

```python
# Conceptual representation of the login function in auth.py
def login_user(username: str, plain_text_password_attempt: str):
    """
    Handles user login attempts.
    This is a conceptual function.
    """
    # Retrieve the stored hashed password for the user
    # stored_hashed_password = get_hashed_password_for_user(username) # Placeholder
    # For conceptual purposes, let's assume we have a way to get it:
    # In a real system, this would involve a database lookup.
    # If the user 'username' was registered with 'password123',
    # hash_password('password123') would yield a hash. We'd retrieve that hash here.
    # For this example, we'll use a placeholder consistent with hash_password's example.
    # This assumes username itself was part of the original plain_text_password for the placeholder.
    # A real system would look up based on username to get the *actual* stored hash.
    retrieved_conceptual_hash = b"conceptual_bcrypt_hash_for_" + plain_text_password_attempt.encode('utf-8') # This line is illustrative for the example to work with verify_password placeholder

    # A more realistic placeholder for a retrieved hash for 'username':
    # stored_hashed_password = database.get_user(username).password_hash
    # For now, we'll use a simplified version for the conceptual flow:
    # Let's assume the user 'testuser' registered with 'password123'.
    # And hash_password('password123') resulted in b'conceptual_bcrypt_hash_for_password123'
    if username == "testuser":
        stored_hashed_password = b"conceptual_bcrypt_hash_for_password123" # Example stored hash
    else:
        stored_hashed_password = None # User not found or no hash

    if stored_hashed_password is None:
        print(f"Conceptual: Login failed for user '{username}'. User not found or no hash available.")
        return False # User not found or hash missing

    # Verify the provided password against the stored hash
    is_password_correct = verify_password(plain_text_password_attempt, stored_hashed_password)

    if is_password_correct:
        print(f"Conceptual: Login successful for user '{username}'.")
        # Proceed with creating a session, issuing a token, etc.
        return True
    else:
        print(f"Conceptual: Login failed for user '{username}'. Incorrect password.")
        # It's important to return a generic error message here in a real system
        return False
}
```

### 6.2. Retrieve Stored Hash

When a user attempts to log in by providing their `username` and a `plain_text_password_attempt`:
1.  The system must first query the database or user store to find the record associated with the given `username`.
2.  If the user is found, retrieve their stored `hashed_password` (the bytes that were originally produced by `hash_password` during registration).
3.  If the user is not found, the login attempt should fail. It's generally good practice to provide a generic "invalid username or password" message to avoid disclosing whether a username exists.

### 6.3. Verification Step

The `plain_text_password_attempt` (provided by the user during login) and the `hashed_password` (retrieved from storage) are then passed as arguments to our `verify_password` function (detailed in Section 4).

```python
    # Inside login_user function, after retrieving stored_hashed_password:
    # ...
    # password_attempt_from_form = "UserS_P@sswOrd123" # Example input
    # is_match = verify_password(password_attempt_from_form, stored_hashed_password)
    # ...
```
The `verify_password` function will securely compare the attempt against the stored hash.

### 6.4. Login Success/Failure

*   If `verify_password` returns `True`, the plain-text password attempt matches the stored hash. The login is considered successful. The system would then typically create a user session, issue an authentication token, or perform other actions appropriate for a successful login.
*   If `verify_password` returns `False`, the password attempt does not match. The login attempt must be rejected. The user should be presented with an appropriate error message (e.g., "Invalid username or password").

### 6.5. Security Note: Timing Attacks

It is crucial that the comparison process within `verify_password` is performed in a way that is resistant to timing attacks. A timing attack could potentially allow an attacker to discern information about the stored hash by measuring the time it takes for the comparison to complete.

Standard, well-vetted bcrypt libraries (like `bcrypt.checkpw` in the Python `bcrypt` package) are designed to perform comparisons in constant time, mitigating this risk. Therefore, relying on the library's verification function is essential. Avoid implementing custom comparison logic for hashes.

## 7. Password Strength Feedback during Registration

This section outlines how real-time or pre-submission feedback on password strength can be provided to users during the registration process. This helps users choose compliant and stronger passwords.

### 7.1. Timing of Feedback

Password strength feedback should be provided to the user **before** the `hash_password` function is called and before any attempt to store user details. Ideally, this feedback occurs:
*   **In real-time:** As the user types their password into the registration form (often implemented with JavaScript on the client-side).
*   **Upon form submission (server-side):** If real-time client-side checks are not feasible or as a secondary server-side validation, the check must occur when the registration form is submitted, before proceeding with user creation.

### 7.2. Policy Check Function

We will define a conceptual function to check a password against the defined policy:

```python
import re # Needed for regex-based checks

# Assume PASSWORD_POLICY.md requirements are:
# - Min length: 12
# - At least one uppercase
# - At least one lowercase
# - At least one digit
# - At least one special character

def check_password_strength(plain_text_password: str) -> dict:
    """
    Checks a plain-text password against predefined policy rules.

    Args:
        plain_text_password: The password string to check.

    Returns:
        A dictionary indicating which rules are met and a list of messages
        for rules that are not met.
        Example: {
            'overall_ok': False,
            'checks': {
                'length_ok': True,
                'uppercase_ok': False,
                'lowercase_ok': True,
                'digit_ok': True,
                'special_char_ok': False
            },
            'messages': [
                "Password must include an uppercase letter.",
                "Password must include a special character."
            ]
        }
    """
    results = {
        'length_ok': len(plain_text_password) >= 12,
        'uppercase_ok': bool(re.search(r'[A-Z]', plain_text_password)),
        'lowercase_ok': bool(re.search(r'[a-z]', plain_text_password)),
        'digit_ok': bool(re.search(r'[0-9]', plain_text_password)),
        'special_char_ok': bool(re.search(r'[^a-zA-Z0-9\s]', plain_text_password)) # Example: any non-alphanumeric, non-whitespace
    }

    messages = []
    if not results['length_ok']:
        messages.append("Password must be at least 12 characters long.")
    if not results['uppercase_ok']:
        messages.append("Password must include at least one uppercase letter (A-Z).")
    if not results['lowercase_ok']:
        messages.append("Password must include at least one lowercase letter (a-z).")
    if not results['digit_ok']:
        messages.append("Password must include at least one digit (0-9).")
    if not results['special_char_ok']:
        messages.append("Password must include at least one special character (e.g., !@#$%^&*).")

    overall_ok = all(results.values())

    return {
        'overall_ok': overall_ok,
        'checks': results,
        'messages': messages
    }
```
This function explicitly references the rules defined in `PASSWORD_POLICY.md` (minimum length, character type requirements). The "Common Passwords" and "No Sequences" recommendations from the policy are harder to implement in such a simple function and would typically involve more complex libraries or services.

### 7.3. User Feedback

The dictionary returned by `check_password_strength` (specifically the `messages` list) can be used to generate user-friendly feedback on the registration form.
*   If `overall_ok` is `False`, the messages explain why the password is not acceptable.
*   For example, if the password "password" is entered, the feedback might be:
    *   "Password must be at least 12 characters long."
    *   "Password must include at least one uppercase letter (A-Z)."
    *   "Password must include at least one digit (0-9)."
    *   "Password must include at least one special character (e.g., !@#$%^&*)."
This feedback helps the user correct their password to meet the policy.

### 7.4. Enforcement

If `check_password_strength(plain_text_password)['overall_ok']` is `False` after the user submits the registration form, the registration process **must be halted**. The user should be prompted to provide a stronger password, displaying the specific reasons (from the `messages` list) why their current password does not meet the requirements.

### 7.5. Integration with Registration Logic

The `check_password_strength` function would be called within the `register_user` function before any hashing or database operations occur.

```python
# Conceptual update to register_user in auth.py
def register_user(username: str, plain_text_password: str, email: str):
    """
    Handles new user registration, including password strength checks.
    This is a conceptual function.
    """
    # ... (other validations like username availability, email format)

    password_strength_feedback = check_password_strength(plain_text_password)

    if not password_strength_feedback['overall_ok']:
        # In a real web application, these messages would be passed to the UI
        print(f"Conceptual: Password for user '{username}' is too weak. Reasons:")
        for msg in password_strength_feedback['messages']:
            print(f"- {msg}")
        # Halt registration
        return False # Indicate failure

    # If password is OK, proceed to hash and store
    hashed_pw = hash_password(plain_text_password)

    # Storing user details
    # store_user_in_database(username, hashed_pw, email)
    print(f"Conceptual: Registering user '{username}' with email '{email}' after password strength check.")
    print(f"Conceptual: Storing hashed password: {hashed_pw}")

    # ... (handle success or failure of storage)
    return True # Placeholder for successful registration
}
```
This ensures that only passwords meeting the defined policy are ever hashed and stored, enhancing overall system security.

## 8. Secure Password Reset Functionality

Implementing a secure password reset mechanism is critical for user account recovery. The following points outline key considerations for its design.

### 8.1. Initiation

A user typically initiates a password reset by providing an identifier, which is usually their **username or registered email address**, on a designated "Forgot Password" page.

*   **Request Handling:** The system receives this identifier and prepares to send reset instructions if the identifier is found (see point 8.6 regarding account enumeration).

### 8.2. Token Generation

Upon a valid initiation request (i.e., the user account exists), the system must generate a password reset token with the following characteristics:

*   **Securely Random:** The token must be cryptographically strong and unpredictable. Use a secure random number generator (e.g., `secrets` module in Python).
*   **Time-Limited:** Tokens must have a limited validity period (e.g., 15-60 minutes) to reduce the window of opportunity for misuse. An expiration timestamp should be stored with the token.
*   **Single-Use:** A token must be invalidated immediately after it's successfully used to reset a password. This prevents replay attacks.
*   **Storage:** The token (or a hash of it) needs to be stored securely, associated with the user's account, alongside its expiry time. Storing a hash of the token prevents an attacker with database access from directly using the token.

### 8.3. Token Delivery

The generated reset token must be delivered to the user through a previously verified communication channel.

*   **Primary Method: Registered Email:** The most common and generally accepted method is sending a link containing the token to the user's registered email address. This email should clearly state the purpose of the link and its expiry time.
*   **Security of Delivery:**
    *   The token should **not** be displayed directly to the user in their browser session after requesting a reset.
    *   Avoid sending tokens via unencrypted or easily intercepted channels. Email, while standard, relies on underlying transport security (TLS).
    *   The link should use HTTPS.

### 8.4. Reset Page

The link in the reset email directs the user to a dedicated, secure (HTTPS) page where they can complete the password reset process. This page will typically require the user to:

1.  **Enter the Token (Often part of the URL):** The token itself is usually embedded in the URL, automatically populating a hidden field or processed by the server directly from the URL query parameter.
2.  **Enter New Password:** The user provides their new desired password.
3.  **Confirm New Password:** The user re-enters the new password to prevent typos.
4.  **Policy Adherence:** The new password entered by the user **must** be validated against the `PASSWORD_POLICY.md` (e.g., using the `check_password_strength` function described in Section 7) before it is accepted.

### 8.5. Verification and Update

Upon submission of the new password on the reset page:

1.  **Token Validation:** The system must:
    *   Verify that the token exists in the system.
    *   Check that the token has not expired.
    *   Ensure the token is associated with the correct user account (if the token itself is not user-specific, the lookup might be based on the token to find the user).
    *   Confirm the token has not already been used.
2.  **Password Update:** If the token is valid and the new password meets policy requirements:
    *   The new password is hashed using the `hash_password` function.
    *   The old password hash in the user's database record is replaced with this new hash.
3.  **Token Invalidation:** The reset token **must** be immediately invalidated (e.g., by deleting it or marking it as used) to prevent reuse.

### 8.6. Security Considerations

Several additional security measures are crucial:

*   **Rate Limiting:** Implement rate limiting on password reset requests (both by IP address and by user account/email) to protect against denial-of-service attacks or attempts to spam users.
*   **User Notification:** After a password has been successfully changed, send a notification email to the user's registered address informing them of this action. This alerts the user if the reset was performed by someone else.
*   **Avoid Weak Security Questions:** Do not use "security questions" as a method for account recovery, as their answers are often easily guessed or socially engineered.
*   **Account Enumeration Prevention (Trade-off):**
    *   **Privacy-Preserving Approach:** On the initial "Forgot Password" page, after the user submits their email/username, display a generic message like, "If an account with this identifier exists, a password reset link has been sent." This prevents an attacker from discovering valid usernames or emails.
    *   **Usability Trade-off:** The downside is that a legitimate user with a typo in their identifier won't know if they made a mistake or if their account doesn't exist. Some systems choose to explicitly state if an account is not found for better usability, but this has security implications.
*   **Audit Trails:** Log password reset requests and successful changes for security monitoring.

## 9. Unit Testing Strategy for Password Management

Thorough unit testing is essential to ensure the reliability and security of password management functionalities. Tests should be atomic, focus on individual functions, and cover both expected behavior and edge cases. (Actual implementation of these tests would use a testing framework like Python's `unittest` or `pytest`).

### 9.1. Testing `hash_password` (Conceptual Function)

*   **Output Type and Non-Emptiness:**
    *   Verify that `hash_password(password)` returns a `bytes` string.
    *   Verify that the returned byte string is not empty for a non-empty input password.
*   **Salting Effect (Different Hashes for Same Password):**
    *   `hash1 = hash_password("test_password123")`
    *   `hash2 = hash_password("test_password123")`
    *   Assert `hash1 != hash2`. (This is a key property of bcrypt due to internal salting).
*   **Output Differs from Input:**
    *   `plain = "test_password123"`
    *   `hashed = hash_password(plain)`
    *   Assert `hashed != plain.encode('utf-8')`.
*   **Input Type Handling (Optional, if not handled by type hints/static analysis):**
    *   Test with non-string input (e.g., `None`, `int`) to ensure it raises a `TypeError` as per the conceptual function's guard clause.

### 9.2. Testing `verify_password` (Conceptual Function)

Let `plain_password = "ValidPass123!"` and `correct_hash = hash_password(plain_password)`.

*   **Correct Password and Hash:**
    *   Assert `verify_password(plain_password, correct_hash) is True`.
*   **Incorrect Password, Correct Hash:**
    *   Assert `verify_password("WrongPass123!", correct_hash) is False`.
*   **Correct Password, Tampered/Incorrect Hash:**
    *   `tampered_hash = correct_hash[:-5] + b"abcde"` (an example of a malformed hash)
    *   Assert `verify_password(plain_password, tampered_hash) is False`.
    *   (Note: Some bcrypt libraries might raise an error for malformed hashes, e.g., `ValueError`. The test should expect this specific error if that's the library's behavior).
*   **Empty Plain Password or Hash:**
    *   `empty_hash = b""`
    *   `empty_plain = ""`
    *   Assert `verify_password(empty_plain, correct_hash) is False`.
    *   Assert `verify_password(plain_password, empty_hash) is False` (or raises error, depending on library).
    *   Assert `verify_password(empty_plain, empty_hash) is False` (or raises error).
*   **Type Handling (Optional):**
    *   Test with inputs not matching `(str, bytes)` to ensure `TypeError` is raised.

### 9.3. Testing `check_password_strength` (Conceptual Function)

These tests should refer to the rules in `PASSWORD_POLICY.md`.

*   **Minimum Length (12 characters):**
    *   Test `check_password_strength("short")['checks']['length_ok'] is False`.
    *   Test `check_password_strength("Exactly12Chr")['checks']['length_ok'] is True`.
    *   Test `check_password_strength("MuchLongerThan12Characters")['checks']['length_ok'] is True`.
*   **Uppercase Letter:**
    *   Test `check_password_strength("nouppercase1!")['checks']['uppercase_ok'] is False`.
    *   Test `check_password_strength("HasUppercase1!")['checks']['uppercase_ok'] is True`.
*   **Lowercase Letter:**
    *   Test `check_password_strength("NOLOWERCASE1!")['checks']['lowercase_ok'] is False`.
    *   Test `check_password_strength("HasLowercase1!")['checks']['lowercase_ok'] is True`.
*   **Digit:**
    *   Test `check_password_strength("NoDigitChar!")['checks']['digit_ok'] is False`.
    *   Test `check_password_strength("HasDigit1Char!")['checks']['digit_ok'] is True`.
*   **Special Character:**
    *   Test `check_password_strength("NoSpecial123")['checks']['special_char_ok'] is False`.
    *   Test `check_password_strength("HasSpecial123!")['checks']['special_char_ok'] is True`.
*   **All Rules Met:**
    *   `result = check_password_strength("ValidPass123!")`
    *   Assert `result['overall_ok'] is True`.
    *   Assert `len(result['messages']) == 0`.
*   **Multiple Rules Failed:**
    *   `result = check_password_strength("weak")`
    *   Assert `result['overall_ok'] is False`.
    *   Assert `len(result['messages']) > 1` (e.g., length, uppercase, digit, special char messages).
*   **Empty Password:**
    *   `result = check_password_strength("")`
    *   Assert `result['overall_ok'] is False`.
    *   Assert that appropriate failure messages are present.

### 9.4. Testing Registration Flow (Conceptual Components)

While full flow testing is integration testing, unit tests can cover components:

*   **Password Policy Check during Registration:**
    *   Mock the `check_password_strength` function when testing `register_user`.
    *   Simulate `check_password_strength` returning `{'overall_ok': False, 'messages': [...]}`.
    *   Assert that `register_user` does not proceed to call `hash_password` or attempt to store the user. Assert it returns an appropriate failure indicator.
*   **Password Hashing during Registration:**
    *   If `check_password_strength` returns `{'overall_ok': True}`:
        *   Assert that `register_user` calls `hash_password` with the plain-text password.
        *   Assert that the value passed to the (mocked) database storage function for the password field is the output of `hash_password`, not the plain text.

### 9.5. Testing Login Flow (Conceptual Components)

*   **Successful Login:**
    *   Mock database retrieval to return a valid `username` and its `correct_hash`.
    *   Mock `verify_password(plain_attempt, correct_hash)` to return `True`.
    *   Assert `login_user(username, plain_attempt)` returns a success indicator.
*   **Incorrect Password:**
    *   Mock database retrieval for `username` and `correct_hash`.
    *   Mock `verify_password(plain_attempt, correct_hash)` to return `False`.
    *   Assert `login_user(username, plain_attempt)` returns a failure indicator.
*   **Non-Existent User:**
    *   Mock database retrieval to indicate user not found (e.g., return `None`).
    *   Assert `login_user("nonexistent_user", "any_password")` returns a failure indicator.
    *   Ensure `verify_password` is not even called in this case.

This unit testing strategy aims to build confidence in each part of the password management system before they are integrated.
