import unittest
from datetime import date, timedelta
from app import years_and_remaining_days_since

class TestYearsAndRemainingDaysSince(unittest.TestCase):
    def test_years_and_remaining_days_since(self):
        data = [
            (date(2024, 3, 5), date(2023, 2, 6), (1, 28, 366)),
            (date(2024, 3, 5), date(2023, 3, 5), (1, 0, 365)),
            (date(2024, 3, 5), date(2023, 3, 6), (0, 365, 366)),
            (date(2024, 3, 5), date(2024, 3, 5), (0, 0, 365)),
        ]
        for today, input_date, expected in data:
            with self.subTest(today = today, input_date = input_date, expected = expected):
                self.assertEqual(years_and_remaining_days_since(input_date, today), expected)

if __name__ == '__main__':
    unittest.main()