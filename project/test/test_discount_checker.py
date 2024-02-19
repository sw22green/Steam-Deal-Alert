# test/test_discount_checker.py
import unittest
from unittest.mock import patch
import os
from project.src.discount_checker import read_file, clear_file, write_intro, write_prices

class TestDiscountChecker(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.links_file = "test_links.txt"
        self.write_file = "test_prices.txt"

    def tearDown(self):
        # Clean up the temporary files
        try:
            os.remove(self.links_file)
            os.remove(self.write_file)
        except FileNotFoundError:
            pass

    def test_read_file(self):
        # Test read_file function with a sample file
        test_content = "Line 1\nLine 2\nLine 3"
        with open(self.links_file, "w") as file:
            file.write(test_content)

        result = read_file(self.links_file)
        self.assertEqual(result, ["Line 1", "Line 2", "Line 3"])

    def test_clear_file(self):
        # Test clear_file function
        with open(self.write_file, 'w') as file:
            file.write("Test Content")

        clear_file(self.write_file)

        with open(self.write_file, 'r') as file:
            content = file.read()

        self.assertEqual(content, "")

    def test_write_intro(self):
        # Test write_intro function with a mock file
        with patch('builtins.open', create=True) as mock_open:
            write_intro()

        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.write.assert_called_once()

    def test_write_prices(self):
        # Test write_prices function with a mock file
        with patch('builtins.open', create=True) as mock_open:
            write_prices(self.write_file, "Test Game", "$19.99, 5 hours left: 50%")

        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.write.assert_called_once_with("Test Game\n$19.99, 5 hours left: 50%\n\n")

if __name__ == '__main__':
    unittest.main()
