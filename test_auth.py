import unittest
from auth import check_password_strength, hash_password, verify_password
import bcrypt # Needed for checking specific bcrypt exception if chosen, though not strictly for current verify_password

class TestPasswordStrength(unittest.TestCase):

    def test_meets_all_criteria(self):
        password = "Str0ngP@sswOrd123" # 17 chars
        result = check_password_strength(password)
        self.assertTrue(result['length_ok'])
        self.assertTrue(result['lowercase_ok'])
        self.assertTrue(result['uppercase_ok'])
        self.assertTrue(result['digit_ok'])
        self.assertTrue(result['special_ok'])
        self.assertTrue(result['overall_ok'])
        self.assertEqual(result['message'], 'Password meets all criteria.')

    def test_too_short(self):
        password = "Sh0rtP@ss" # 9 chars
        result = check_password_strength(password)
        self.assertFalse(result['length_ok'])
        self.assertTrue(result['lowercase_ok']) # Has 'h', 'r', 't', 's', 's'
        self.assertTrue(result['uppercase_ok']) # Has 'S', 'P'
        self.assertTrue(result['digit_ok'])     # Has '0'
        self.assertTrue(result['special_ok'])   # Has '@'
        self.assertFalse(result['overall_ok'])
        self.assertEqual(result['message'], 'Password must be at least 12 characters long.')

    def test_missing_lowercase(self):
        password = "STR0NGP@SSWORD123" # 17 chars
        result = check_password_strength(password)
        self.assertTrue(result['length_ok'])
        self.assertFalse(result['lowercase_ok'])
        self.assertTrue(result['uppercase_ok'])
        self.assertTrue(result['digit_ok'])
        self.assertTrue(result['special_ok'])
        self.assertFalse(result['overall_ok'])
        self.assertEqual(result['message'], 'Password must include at least one lowercase letter (a-z).')

    def test_missing_uppercase(self):
        password = "str0ngp@ssword123" # 17 chars
        result = check_password_strength(password)
        self.assertTrue(result['length_ok'])
        self.assertTrue(result['lowercase_ok'])
        self.assertFalse(result['uppercase_ok'])
        self.assertTrue(result['digit_ok'])
        self.assertTrue(result['special_ok'])
        self.assertFalse(result['overall_ok'])
        self.assertEqual(result['message'], 'Password must include at least one uppercase letter (A-Z).')

    def test_missing_digit(self):
        password = "StrongP@sswOrd" # 14 chars
        result = check_password_strength(password)
        self.assertTrue(result['length_ok'])
        self.assertTrue(result['lowercase_ok'])
        self.assertTrue(result['uppercase_ok'])
        self.assertFalse(result['digit_ok'])
        self.assertTrue(result['special_ok'])
        self.assertFalse(result['overall_ok'])
        self.assertEqual(result['message'], 'Password must include at least one digit (0-9).')

    def test_missing_special_character(self):
        password = "Str0ngPassword123" # 17 chars
        result = check_password_strength(password)
        self.assertTrue(result['length_ok'])
        self.assertTrue(result['lowercase_ok'])
        self.assertTrue(result['uppercase_ok'])
        self.assertTrue(result['digit_ok'])
        self.assertFalse(result['special_ok'])
        self.assertFalse(result['overall_ok'])
        self.assertEqual(result['message'], "Password must include at least one special character (e.g., [!@#$%^&*()-_=+\[\]{};:'\",.<>/?]).")

    def test_failing_multiple_criteria(self):
        password = "short" # 5 chars, no uppercase, no digit, no special
        result = check_password_strength(password)
        self.assertFalse(result['length_ok'])
        self.assertTrue(result['lowercase_ok']) # s, h, o, r, t
        self.assertFalse(result['uppercase_ok'])
        self.assertFalse(result['digit_ok'])
        self.assertFalse(result['special_ok'])
        self.assertFalse(result['overall_ok'])
        # Message should be for the first unmet criteria
        self.assertEqual(result['message'], 'Password must be at least 12 characters long.')

    def test_failing_multiple_criteria_no_lower(self):
        password = "SHORT" # 5 chars, no lowercase, no digit, no special
        result = check_password_strength(password)
        self.assertFalse(result['length_ok'])
        self.assertFalse(result['lowercase_ok'])
        self.assertTrue(result['uppercase_ok'])
        self.assertFalse(result['digit_ok'])
        self.assertFalse(result['special_ok'])
        self.assertFalse(result['overall_ok'])
        # Message should be for the first unmet criteria
        self.assertEqual(result['message'], 'Password must be at least 12 characters long.')


    def test_empty_password(self):
        password = ""
        result = check_password_strength(password)
        self.assertFalse(result['length_ok'])
        self.assertFalse(result['lowercase_ok'])
        self.assertFalse(result['uppercase_ok'])
        self.assertFalse(result['digit_ok'])
        self.assertFalse(result['special_ok'])
        self.assertFalse(result['overall_ok'])
        self.assertEqual(result['message'], 'Password must be at least 12 characters long.')

    def test_just_meets_length(self):
        password = "Str0ngP@ss12" # 12 chars
        result = check_password_strength(password)
        self.assertTrue(result['length_ok'])
        self.assertTrue(result['lowercase_ok'])
        self.assertTrue(result['uppercase_ok'])
        self.assertTrue(result['digit_ok'])
        self.assertTrue(result['special_ok'])
        self.assertTrue(result['overall_ok'])
        self.assertEqual(result['message'], 'Password meets all criteria.')

    def test_various_special_characters(self):
        special_chars_to_test = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '{', '}', ';', ':', "'", '"', ',', '.', '<', '>', '/', '?']
        base_password_start = "Val1dPassw" # 10 chars, needs 2 more + special
        for char_code, char in enumerate(special_chars_to_test):
            # Ensure password is long enough even with short char codes
            password = f"{base_password_start}{char_code:02d}{char}"
            with self.subTest(special_char=char, password_tested=password):
                result = check_password_strength(password)
                self.assertTrue(result['length_ok'], f"Length check failed for '{password}' with '{char}'")
                self.assertTrue(result['lowercase_ok'], f"Lowercase check failed for '{password}' with '{char}'")
                self.assertTrue(result['uppercase_ok'], f"Uppercase check failed for '{password}' with '{char}'")
                self.assertTrue(result['digit_ok'], f"Digit check failed for '{password}' with '{char}'")
                self.assertTrue(result['special_ok'], f"Special char check failed for '{password}' with '{char}'")
                self.assertTrue(result['overall_ok'], f"Overall check failed for '{password}' with '{char}'")
                self.assertEqual(result['message'], 'Password meets all criteria.', f"Message incorrect for '{password}' with '{char}'")

    def test_non_string_input(self):
        # As per implementation, it should handle non-string gracefully
        result_none = check_password_strength(None)
        self.assertFalse(result_none['overall_ok'])
        self.assertEqual(result_none['message'], 'Password must be a string.')

        result_int = check_password_strength(12345)
        self.assertFalse(result_int['overall_ok'])
        self.assertEqual(result_int['message'], 'Password must be a string.')

    # --- Tests for hash_password and verify_password ---

    def test_hash_password_returns_bytes(self):
        password = "testPassword123"
        hashed = hash_password(password)
        self.assertIsInstance(hashed, bytes)
        self.assertTrue(len(hashed) > 0)

    def test_hash_password_different_salts(self):
        password = "testPassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        self.assertNotEqual(hash1, hash2, "Hashing the same password twice should produce different hashes due to salting.")

    def test_verify_password_correct(self):
        plain_password = "mySecurePassword!@#"
        hashed_password = hash_password(plain_password)
        self.assertTrue(verify_password(plain_password, hashed_password))

    def test_verify_password_incorrect(self):
        plain_password = "mySecurePassword!@#"
        hashed_password = hash_password(plain_password)
        self.assertFalse(verify_password("incorrectPassword!@#", hashed_password))

    def test_verify_password_malformed_hash(self):
        plain_password = "mySecurePassword!@#"
        # These are not valid bcrypt hashes
        malformed_hashes = [
            b"notavalidhash",
            b"$2a$12$short",
            b"",
            b"justaStringNotBytesEncodedProperly",
            b"$2a$05$usesomesillystringforsalt$", # Missing actual hash part
            b"$2a$12$abcdefghijklmnopqrstuv.abcdefghijklmnopqrstuv" # Correct length but potentially invalid chars
        ]
        for mal_hash in malformed_hashes:
            with self.subTest(malformed_hash=mal_hash):
                self.assertFalse(verify_password(plain_password, mal_hash))
                # Depending on bcrypt version and specific malformation,
                # bcrypt.checkpw might raise ValueError, which our function turns into False.
                # Or it might return False directly.

    def test_hash_password_type_error(self):
        with self.assertRaises(TypeError, msg="hash_password should raise TypeError for None input"):
            hash_password(None)
        with self.assertRaises(TypeError, msg="hash_password should raise TypeError for integer input"):
            hash_password(12345)

    def test_verify_password_type_error(self):
        sample_hash = hash_password("aPassword")

        with self.assertRaises(TypeError, msg="verify_password should raise TypeError for non-string password (None)"):
            verify_password(None, sample_hash)
        with self.assertRaises(TypeError, msg="verify_password should raise TypeError for non-string password (int)"):
            verify_password(123, sample_hash)

        with self.assertRaises(TypeError, msg="verify_password should raise TypeError for non-bytes hash (None)"):
            verify_password("aPassword", None)
        with self.assertRaises(TypeError, msg="verify_password should raise TypeError for non-bytes hash (str)"):
            verify_password("aPassword", "notbytesstring")

if __name__ == '__main__':
    unittest.main()
