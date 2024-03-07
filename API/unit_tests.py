import unittest
from datetime import date, timedelta
from app import years_and_remaining_days_since, Analyser, compound_interest_ratio
import math

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

class TestTargetSalePrices(unittest.TestCase):
    def test_target_sale_prices(self):
        data = [
            (100, date(2020, 1, 1), 0.02, 0.02, 0.15, 0.1, date(2022, 1, 1)),  # Add more tuples as needed
        ]

        for price_at_buy, purchase_date, fee_ratio_at_buy, fee_ratio_at_sell, capital_gains_tax_ratio, target_annual_profit_interest_ratio, today in data:
            with self.subTest(price_at_buy=price_at_buy, purchase_date=purchase_date, fee_ratio_at_buy=fee_ratio_at_buy, fee_ratio_at_sell=fee_ratio_at_sell, capital_gains_tax_ratio=capital_gains_tax_ratio, target_annual_profit_interest_ratio=target_annual_profit_interest_ratio, today=today):
                cost_price = price_at_buy * (1 + fee_ratio_at_buy)
                years_difference, days_remainder_difference, total_days_in_latest_year = years_and_remaining_days_since(purchase_date, today)
                target_interest_ratio_with_strict_time = compound_interest_ratio(target_annual_profit_interest_ratio, years_difference + days_remainder_difference / total_days_in_latest_year)
                target_interest_ratio_with_yearly_time = compound_interest_ratio(target_annual_profit_interest_ratio, math.ceil(years_difference + days_remainder_difference / total_days_in_latest_year))
                target_sale_price_with_strict_time, target_sale_price_with_yearly_time = Analyser.target_sale_prices(price_at_buy, purchase_date, fee_ratio_at_buy, fee_ratio_at_sell, capital_gains_tax_ratio, target_annual_profit_interest_ratio, today)
                def sale_price_to_profit_ratio(sale_price):
                    gains = sale_price * (1 - fee_ratio_at_sell) - cost_price
                    profit = gains * (1 - capital_gains_tax_ratio)
                    return profit / cost_price + 1
                self.assertAlmostEqual(sale_price_to_profit_ratio(target_sale_price_with_strict_time), target_interest_ratio_with_strict_time, places=10)
                self.assertAlmostEqual(sale_price_to_profit_ratio(target_sale_price_with_yearly_time), target_interest_ratio_with_yearly_time, places=10)

    def test_target_sale_prices_hard_coded(self):
        cost_price = 1000 * (1 + 0.03)
        strict_ratio = (1 + 0.2) ** (1 + 28/366)
        profit = cost_price * (strict_ratio - 1)
        gains = profit / (1 - 0.1)
        sale_price = (cost_price + gains)/(1 - 0.025)
        self.assertAlmostEqual(sale_price, 1310.9522970764065, places=10)
        year_wise_ratio = (1 + 0.2) ** 2
        profit = cost_price * (year_wise_ratio - 1)
        gains = profit / (1 - 0.1)
        sale_price = (cost_price + gains)/(1 - 0.025)
        self.assertAlmostEqual(sale_price, 1572.8774928774928, places=10)
             

if __name__ == '__main__':
    unittest.main()