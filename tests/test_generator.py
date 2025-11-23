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
        self.assertEqual(pools, (string.ascii_uppercase, string.ascii_lowercase))
        self.assertEqual(count, 2)

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
                string.ascii_uppercase,
                string.ascii_lowercase,
                string.digits,
            ),
        )
        self.assertEqual(count, 3)

    def test_generate_pools_upper_lower_and_symbols(self):
        """Test pool with uppercase, lowercase letters, and symbols enabled."""
        pools, count = generate_pools(True, True, False, True)
        self.assertEqual(
            pools,
            (
                string.ascii_uppercase,
                string.ascii_lowercase,
                symbols_pool,
            ),
        )
        self.assertEqual(count, 3)

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
                string.ascii_uppercase,
                string.ascii_lowercase,
                string.digits,
                symbols_pool,
            ),
        )
        self.assertEqual(count, 4)

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

    def contains_uppercase(self, s):
        return any(c.isupper() for c in s)

    def contains_lowercase(self, s):
        return any(c.islower() for c in s)

    def contains_digits(self, s):
        return any(c.isdigit() for c in s)

    def contains_symbols(self, s):
        return any(c in symbols_pool for c in s)

    # --- length ---
    def test_generate_password_length(self):
        for _ in range(500):
            for length in (7, 12, 50, 1000):
                password = generate_password(length)
                self.assertEqual(len(password), length)

    # --- single-category ---
    def test_generate_password_contains_upper(self):
        for _ in range(500):
            p = generate_password(12, True, False, False, False)
            self.assertTrue(self.contains_uppercase(p))
            self.assertFalse(self.contains_lowercase(p))
            self.assertFalse(self.contains_digits(p))
            self.assertFalse(self.contains_symbols(p))

    def test_generate_password_contains_lower(self):
        for _ in range(500):
            p = generate_password(12, False, True, False, False)
            self.assertTrue(self.contains_lowercase(p))
            self.assertFalse(self.contains_uppercase(p))
            self.assertFalse(self.contains_digits(p))
            self.assertFalse(self.contains_symbols(p))

    def test_generate_password_contains_digits(self):
        for _ in range(500):
            p = generate_password(12, False, False, True, False)
            self.assertTrue(self.contains_digits(p))
            self.assertFalse(self.contains_lowercase(p))
            self.assertFalse(self.contains_uppercase(p))
            self.assertFalse(self.contains_symbols(p))

    def test_generate_password_contains_symbols(self):
        for _ in range(500):
            p = generate_password(12, False, False, False, True)
            self.assertTrue(self.contains_symbols(p))
            self.assertFalse(self.contains_lowercase(p))
            self.assertFalse(self.contains_uppercase(p))
            self.assertFalse(self.contains_digits(p))

    # --- two categories ---
    def test_generate_password_contains_upper_and_lower(self):
        for _ in range(500):
            p = generate_password(12, True, True, False, False)
            self.assertTrue(self.contains_uppercase(p))
            self.assertTrue(self.contains_lowercase(p))
            self.assertFalse(self.contains_digits(p))
            self.assertFalse(self.contains_symbols(p))

    def test_generate_password_contains_upper_and_digits(self):
        for _ in range(500):
            p = generate_password(12, True, False, True, False)
            self.assertTrue(self.contains_uppercase(p))
            self.assertTrue(self.contains_digits(p))
            self.assertFalse(self.contains_lowercase(p))
            self.assertFalse(self.contains_symbols(p))

    def test_generate_password_contains_upper_and_symbols(self):
        for _ in range(500):
            p = generate_password(12, True, False, False, True)
            self.assertTrue(self.contains_uppercase(p))
            self.assertTrue(self.contains_symbols(p))
            self.assertFalse(self.contains_digits(p))
            self.assertFalse(self.contains_lowercase(p))

    def test_generate_password_contains_lower_and_digits(self):
        for _ in range(500):
            p = generate_password(12, False, True, True, False)
            self.assertTrue(self.contains_lowercase(p))
            self.assertTrue(self.contains_digits(p))
            self.assertFalse(self.contains_uppercase(p))
            self.assertFalse(self.contains_symbols(p))

    def test_generate_password_contains_lower_and_symbols(self):
        for _ in range(500):
            p = generate_password(12, False, True, False, True)
            self.assertTrue(self.contains_lowercase(p))
            self.assertTrue(self.contains_symbols(p))
            self.assertFalse(self.contains_digits(p))
            self.assertFalse(self.contains_uppercase(p))

    def test_generate_password_contains_digits_and_symbols(self):
        for _ in range(500):
            p = generate_password(12, False, False, True, True)
            self.assertTrue(self.contains_digits(p))
            self.assertTrue(self.contains_symbols(p))
            self.assertFalse(self.contains_uppercase(p))
            self.assertFalse(self.contains_lowercase(p))

    # --- three categories ---
    def test_generate_password_contains_upper_lower_and_digits(self):
        for _ in range(500):
            p = generate_password(12, True, True, True, False)
            self.assertTrue(self.contains_uppercase(p))
            self.assertTrue(self.contains_lowercase(p))
            self.assertTrue(self.contains_digits(p))
            self.assertFalse(self.contains_symbols(p))

    def test_generate_password_contains_upper_lower_and_symbols(self):
        for _ in range(500):
            p = generate_password(12, True, True, False, True)
            self.assertTrue(self.contains_uppercase(p))
            self.assertTrue(self.contains_lowercase(p))
            self.assertTrue(self.contains_symbols(p))
            self.assertFalse(self.contains_digits(p))

    def test_generate_password_contains_upper_digits_and_symbols(self):
        for _ in range(500):
            p = generate_password(12, True, False, True, True)
            self.assertTrue(self.contains_uppercase(p))
            self.assertTrue(self.contains_digits(p))
            self.assertTrue(self.contains_symbols(p))
            self.assertFalse(self.contains_lowercase(p))

    def test_generate_password_contains_lower_digits_and_symbols(self):
        for _ in range(500):
            p = generate_password(12, False, True, True, True)
            self.assertTrue(self.contains_lowercase(p))
            self.assertTrue(self.contains_digits(p))
            self.assertTrue(self.contains_symbols(p))
            self.assertFalse(self.contains_uppercase(p))

    # --- all categories ---
    def test_generate_password_contains_all(self):
        for _ in range(500):
            p = generate_password(12, True, True, True, True)
            self.assertTrue(self.contains_uppercase(p))
            self.assertTrue(self.contains_lowercase(p))
            self.assertTrue(self.contains_digits(p))
            self.assertTrue(self.contains_symbols(p))


if __name__ == "__main__":
    unittest.main()
