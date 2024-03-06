import unittest
from datetime import date, timedelta
from app import years_and_remaining_days_since, Analyser, compound_interest_ratio
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

class TestCompoundInterestRatio(unittest.TestCase):
    def test_compound_interest_ratio(self):
        # Test with rate = 0.05 (5%) and time = 5 years
        result = compound_interest_ratio(0.05, 5)
        self.assertAlmostEqual(result, 1.2762815625, places=10)

        # Test with rate = 0.1 (10%) and time = 10 years
        result = compound_interest_ratio(0.1, 10)
        self.assertAlmostEqual(result, 2.5937424601, places=10)

        # Test with rate = 0.2 (20%) and time = 3 years
        result = compound_interest_ratio(0.2, 3)
        self.assertAlmostEqual(result, 1.728, places=10)

if __name__ == '__main__':
    unittest.main()