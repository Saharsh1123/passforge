import string
import unittest

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
        self.assertEqual(pools, (string.ascii_uppercase, string.digits,))
        self.assertEqual(count, 2)

    def test_generate_pools_upper_and_symbols(self):
        """Test pool with uppercase letters and symbols enabled."""
        pools, count = generate_pools(True, False, False, True)
        self.assertEqual(pools, (string.ascii_uppercase, symbols_pool,))
        self.assertEqual(count, 2)

    def test_generate_pools_lower_and_digits(self):
        """Test pool with lowercase letters and digits enabled."""
        pools, count = generate_pools(False, True, True, False)
        self.assertEqual(pools, (string.ascii_lowercase, string.digits,))
        self.assertEqual(count, 2)

    def test_generate_pools_lower_and_symbols(self):
        """Test pool with lowercase letters and symbols enabled."""
        pools, count = generate_pools(False, True, False, True)
        self.assertEqual(pools, (string.ascii_lowercase, symbols_pool,))
        self.assertEqual(count, 2)

    def test_generate_pools_digits_and_symbols(self):
        """Test pool with digits and symbols enabled."""
        pools, count = generate_pools(False, False, True, True)
        self.assertEqual(pools, (string.digits, symbols_pool,))
        self.assertEqual(count, 2)

    def test_generate_pools_upper_lower_and_digits(self):
        """Test pool with uppercase, lowercase letters, and digits enabled."""
        pools, count = generate_pools(True, True, True, False)
        self.assertEqual(pools, (string.ascii_letters, string.digits,))
        self.assertEqual(count, 2)

    def test_generate_pools_upper_lower_and_symbols(self):
        """Test pool with uppercase, lowercase letters, and symbols enabled."""
        pools, count = generate_pools(True, True, False, True)
        self.assertEqual(pools, (string.ascii_letters, symbols_pool,))
        self.assertEqual(count, 2)

    def test_generate_pools_upper_digits_and_symbols(self):
        """Test pool with uppercase letters, digits, and symbols enabled."""
        pools, count = generate_pools(True, False, True, True)
        self.assertEqual(pools, (string.ascii_uppercase, string.digits, symbols_pool,))
        self.assertEqual(count, 3)

    def test_generate_pools_lower_digits_and_symbols(self):
        """Test pool with lowercase letters, digits, and symbols enabled."""
        pools, count = generate_pools(False, True, True, True)
        self.assertEqual(pools, (string.ascii_lowercase, string.digits, symbols_pool,))
        self.assertEqual(count, 3)

    def test_generate_pools_all(self):
        """Test pool with all character categories enabled."""
        pools, count = generate_pools(True, True, True, True)
        self.assertEqual(pools, (string.ascii_letters, string.digits, symbols_pool,))
        self.assertEqual(count, 3)

    def test_generate_pools_none(self):
        """Test pool when no categories are enabled (should return empty)."""
        pools, count = generate_pools(False, False, False, False)
        self.assertEqual(pools, ())
        self.assertEqual(count, 0)


if __name__ == '__main__':
    unittest.main()

