import string
import unittest
from unittest.mock import patch
from io import StringIO
from generator import generate_pools, generate_password, symbols_pool


class TestGeneratePools(unittest.TestCase):
    """
    Unit tests for the generate_pools function.

    Validates that the character pools returned correspond exactly to the
    expected sets based on enabled character categories:
    uppercase, lowercase, digits, and symbols.

    Each test checks:
        - The tuple of active pools matches the expected constant pools.
        - The count of enabled categories is accurate.
    """

    def test_generate_pools_upper_only(self):
        """Test pool with only uppercase letters enabled."""
        pools, count = generate_pools(True, False, False, False)
        self.assertEqual(pools, (string.ascii_uppercase,))
        self.assertEqual(count, 1)

    def test_generate_pools_lower_only(self):
        """Test pool with only lowercase letters enabled."""
        pools, count = generate_pools(False, True, False, False)
        self.assertEqual(pools, (string.ascii_lowercase,))
        self.assertEqual(count, 1)

    def test_generate_pools_digits_only(self):
        """Test pool with only digits enabled."""
        pools, count = generate_pools(False, False, True, False)
        self.assertEqual(pools, (string.digits,))
        self.assertEqual(count, 1)

    def test_generate_pools_symbols_only(self):
        """Test pool with only symbols enabled."""
        pools, count = generate_pools(False, False, False, True)
        self.assertEqual(pools, (symbols_pool,))
        self.assertEqual(count, 1)

    def test_generate_pools_upper_and_lower(self):
        """Test pool with uppercase and lowercase letters enabled (combined)."""
        pools, count = generate_pools(True, True, False, False)
        self.assertEqual(pools, (string.ascii_letters,))
        self.assertEqual(count, 1)

    def test_generate_pools_upper_and_digits(self):
        """Test pool with uppercase letters and digits enabled."""
        pools, count = generate_pools(True, False, True, False)
        self.assertEqual(
            pools,
            (
                string.ascii_uppercase,
                string.digits,
            ),
        )
        self.assertEqual(count, 2)

    def test_generate_pools_upper_and_symbols(self):
        """Test pool with uppercase letters and symbols enabled."""
        pools, count = generate_pools(True, False, False, True)
        self.assertEqual(
            pools,
            (
                string.ascii_uppercase,
                symbols_pool,
            ),
        )
        self.assertEqual(count, 2)

    def test_generate_pools_lower_and_digits(self):
        """Test pool with lowercase letters and digits enabled."""
        pools, count = generate_pools(False, True, True, False)
        self.assertEqual(
            pools,
            (
                string.ascii_lowercase,
                string.digits,
            ),
        )
        self.assertEqual(count, 2)

    def test_generate_pools_lower_and_symbols(self):
        """Test pool with lowercase letters and symbols enabled."""
        pools, count = generate_pools(False, True, False, True)
        self.assertEqual(
            pools,
            (
                string.ascii_lowercase,
                symbols_pool,
            ),
        )
        self.assertEqual(count, 2)

    def test_generate_pools_digits_and_symbols(self):
        """Test pool with digits and symbols enabled."""
        pools, count = generate_pools(False, False, True, True)
        self.assertEqual(
            pools,
            (
                string.digits,
                symbols_pool,
            ),
        )
        self.assertEqual(count, 2)

    def test_generate_pools_upper_lower_and_digits(self):
        """Test pool with uppercase, lowercase letters, and digits enabled."""
        pools, count = generate_pools(True, True, True, False)
        self.assertEqual(
            pools,
            (
                string.ascii_letters,
                string.digits,
            ),
        )
        self.assertEqual(count, 2)

    def test_generate_pools_upper_lower_and_symbols(self):
        """Test pool with uppercase, lowercase letters, and symbols enabled."""
        pools, count = generate_pools(True, True, False, True)
        self.assertEqual(
            pools,
            (
                string.ascii_letters,
                symbols_pool,
            ),
        )
        self.assertEqual(count, 2)

    def test_generate_pools_upper_digits_and_symbols(self):
        """Test pool with uppercase letters, digits, and symbols enabled."""
        pools, count = generate_pools(True, False, True, True)
        self.assertEqual(
            pools,
            (
                string.ascii_uppercase,
                string.digits,
                symbols_pool,
            ),
        )
        self.assertEqual(count, 3)

    def test_generate_pools_lower_digits_and_symbols(self):
        """Test pool with lowercase letters, digits, and symbols enabled."""
        pools, count = generate_pools(False, True, True, True)
        self.assertEqual(
            pools,
            (
                string.ascii_lowercase,
                string.digits,
                symbols_pool,
            ),
        )
        self.assertEqual(count, 3)

    def test_generate_pools_all(self):
        """Test pool with all character categories enabled."""
        pools, count = generate_pools(True, True, True, True)
        self.assertEqual(
            pools,
            (
                string.ascii_letters,
                string.digits,
                symbols_pool,
            ),
        )
        self.assertEqual(count, 3)

    def test_generate_pools_none(self):
        """Test pool when no categories are enabled (should return empty and print error)."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            pools, count = generate_pools(False, False, False, False)
            output = fake_out.getvalue()

        self.assertEqual(pools, ())
        self.assertEqual(count, 0)
        self.assertIn("You didn't select any character categories!", output)


class TestGeneratePassword(unittest.TestCase):
    """
    Tests for `generate_password`.

    These tests confirm:
        - Generated passwords match the requested length.
        - Required character types always appear at least once.
        - Unrequested character types never appear.
    """

    # Helper validation methods
    def contains_uppercase(self, s: str) -> bool:
        """Return True if the string contains at least one uppercase letter."""
        return any(c.isupper() for c in s)

    def contains_lowercase(self, s: str) -> bool:
        """Return True if the string contains at least one lowercase letter."""
        return any(c.islower() for c in s)

    def contains_digits(self, s: str) -> bool:
        """Return True if the string contains at least one digit."""
        return any(c.isdigit() for c in s)

    def contains_symbols(self, s: str) -> bool:
        """Return True if the string contains at least one valid symbol."""
        return any(c in symbols_pool for c in s)

    # --- Length tests ---

    def test_generate_password_length(self):
        """Generated passwords must match the requested length."""
        for length in (7, 12, 50, 1000):
            password = generate_password(length)
            self.assertEqual(len(password), length)

    # --- Category-presence tests (one category) ---

    def test_generate_password_contains_upper(self):
        """Passwords with only uppercase enabled must contain only uppercase."""
        password = generate_password(12, True, False, False, False)
        self.assertTrue(self.contains_uppercase(password))
        self.assertFalse(self.contains_lowercase(password))
        self.assertFalse(self.contains_digits(password))
        self.assertFalse(self.contains_symbols(password))

    def test_generate_password_contains_lower(self):
        """Lowercase only."""
        password = generate_password(12, False, True, False, False)
        self.assertTrue(self.contains_lowercase(password))
        self.assertFalse(self.contains_uppercase(password))
        self.assertFalse(self.contains_digits(password))
        self.assertFalse(self.contains_symbols(password))

    def test_generate_password_contains_digits(self):
        """Digits only."""
        password = generate_password(12, False, False, True, False)
        self.assertTrue(self.contains_digits(password))
        self.assertFalse(self.contains_lowercase(password))
        self.assertFalse(self.contains_uppercase(password))
        self.assertFalse(self.contains_symbols(password))

    def test_generate_password_contains_symbols(self):
        """Symbols only."""
        password = generate_password(12, False, False, False, True)
        self.assertTrue(self.contains_symbols(password))
        self.assertFalse(self.contains_lowercase(password))
        self.assertFalse(self.contains_uppercase(password))
        self.assertFalse(self.contains_digits(password))

    # --- Two-category presence tests ---

    def test_generate_password_contains_upper_and_lower(self):
        """Uppercase + lowercase should both appear."""
        password = generate_password(12, True, True, False, False)
        self.assertTrue(self.contains_uppercase(password))
        self.assertTrue(self.contains_lowercase(password))
        self.assertFalse(self.contains_digits(password))
        self.assertFalse(self.contains_symbols(password))

    def test_generate_password_contains_upper_and_digits(self):
        """Uppercase + digits should appear; others must not."""
        password = generate_password(12, True, False, True, False)
        self.assertTrue(self.contains_uppercase(password))
        self.assertTrue(self.contains_digits(password))
        self.assertFalse(self.contains_symbols(password))
        self.assertFalse(self.contains_lowercase(password))

    def test_generate_password_contains_upper_and_symbols(self):
        """Uppercase + symbols."""
        password = generate_password(12, True, False, False, True)
        self.assertTrue(self.contains_uppercase(password))
        self.assertTrue(self.contains_symbols(password))
        self.assertFalse(self.contains_digits(password))
        self.assertFalse(self.contains_lowercase(password))

    def test_generate_password_contains_lower_and_digits(self):
        """Lowercase + digits."""
        password = generate_password(12, False, True, True, False)
        self.assertTrue(self.contains_digits(password))
        self.assertTrue(self.contains_lowercase(password))
        self.assertFalse(self.contains_symbols(password))
        self.assertFalse(self.contains_uppercase(password))

    def test_generate_password_contains_lower_and_symbols(self):
        """Lowercase + symbols."""
        password = generate_password(12, False, True, False, True)
        self.assertTrue(self.contains_symbols(password))
        self.assertTrue(self.contains_lowercase(password))
        self.assertFalse(self.contains_digits(password))
        self.assertFalse(self.contains_uppercase(password))

    def test_generate_password_contains_digits_and_symbols(self):
        """Digits + symbols."""
        password = generate_password(12, False, False, True, True)
        self.assertTrue(self.contains_digits(password))
        self.assertTrue(self.contains_symbols(password))
        self.assertFalse(self.contains_lowercase(password))
        self.assertFalse(self.contains_uppercase(password))

    # --- Three-category presence tests ---

    def test_generate_password_contains_upper_lower_and_digits(self):
        password = generate_password(12, True, True, True, False)
        self.assertTrue(self.contains_digits(password))
        self.assertTrue(self.contains_lowercase(password))
        self.assertTrue(self.contains_uppercase(password))
        self.assertFalse(self.contains_symbols(password))

    def test_generate_password_contains_upper_lower_and_symbols(self):
        password = generate_password(12, True, True, False, True)
        self.assertTrue(self.contains_symbols(password))
        self.assertTrue(self.contains_lowercase(password))
        self.assertTrue(self.contains_uppercase(password))
        self.assertFalse(self.contains_digits(password))

    def test_generate_password_contains_upper_digits_and_symbols(self):
        password = generate_password(12, True, False, True, True)
        self.assertTrue(self.contains_digits(password))
        self.assertTrue(self.contains_symbols(password))
        self.assertTrue(self.contains_uppercase(password))
        self.assertFalse(self.contains_lowercase(password))

    def test_generate_password_contains_lower_digits_and_symbols(self):
        password = generate_password(12, False, True, True, True)
        self.assertTrue(self.contains_digits(password))
        self.assertTrue(self.contains_symbols(password))
        self.assertTrue(self.contains_lowercase(password))
        self.assertFalse(self.contains_uppercase(password))

    # --- All categories enabled ---

    def test_generate_password_contains_all(self):
        """When all categories are enabled, all must appear."""
        password = generate_password(12, True, True, True, True)
        self.assertTrue(self.contains_digits(password))
        self.assertTrue(self.contains_symbols(password))
        self.assertTrue(self.contains_uppercase(password))
        self.assertTrue(self.contains_lowercase(password))


if __name__ == "__main__":
    unittest.main()
