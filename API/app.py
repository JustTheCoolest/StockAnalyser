from flask import Flask
from flask_restful import Resource, Api, reqparse
import oracledb
import datetime
import dateutil.relativedelta
import math

app = Flask(__name__)
api = Api(app)

connection = oracledb.connect(user='system', password=open('API/password.txt').read(), dsn='localhost:1521/xe')
cursor = connection.cursor()

def table_setup():
    # Task: Check if the existing table signature is the same as the table we are trying to create
    try:
        cursor.execute(
            '''
            CREATE TABLE Stocks(
                name VARCHAR(20), 
                price_at_buy FLOAT, 
                purchase_date DATE, 
                fee_ratio_at_buy FLOAT, 
                fee_ratio_at_sell FLOAT, 
                capital_gains_tax_ratio FLOAT, 
                target_profit_ratio FLOAT
            )
            ''')
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 955:
            #print("Table stocks already exists.")
            pass
        else:
            raise

def years_and_remaining_days_since(input_date, today):
    """ Untested for negative dates """
    time_difference_from_now = dateutil.relativedelta.relativedelta(today, input_date)
    years_difference = time_difference_from_now.years
    input_date_in_latest_year = input_date + dateutil.relativedelta.relativedelta(years=years_difference)
    days_remainder_difference = (today - input_date_in_latest_year).days
    input_date_in_its_next_year = input_date_in_latest_year.replace(year = input_date_in_latest_year.year + 1)
    total_days_in_latest_year = (input_date_in_its_next_year - input_date_in_latest_year).days
    return (years_difference, days_remainder_difference, total_days_in_latest_year)

def fractional_years_since(input_date, today):
    years_difference, days_remainder_difference, total_days_in_latest_year = years_and_remaining_days_since(input_date, today)
    return years_difference + days_remainder_difference / total_days_in_latest_year

def compound_interest_ratio(rate, time):
    ratio = (1 + rate) ** time
    return ratio

class Analyser(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price_at_buy', type=float)
    parser.add_argument('purchase_date', type=lambda string: datetime.datetime.strptime(string, '%Y-%m-%d').date())
    parser.add_argument('fee_ratio_at_buy', type=float)
    parser.add_argument('fee_ratio_at_sell', type=float)
    parser.add_argument('capital_gains_tax_ratio', type=float)
    parser.add_argument('target_profit_ratio', type=float)

    @staticmethod
    def target_sale_prices(price_at_buy, purchase_date, fee_ratio_at_buy, fee_ratio_at_sell, capital_gains_tax_ratio, target_annual_profit_interest_ratio, today = datetime.datetime.now().date()):
        """ 
        Ratios: Part to be added. For example, target_annual_profit_interest_ratio = 0.1 for 10% interest.
        Target annual profit is compounded continually.
        """
        def intermediate_aggregator(target_interest_ratio):
            return cost_price / (1 - fee_ratio_at_sell) * ( (target_interest_ratio - 1) / (1 - capital_gains_tax_ratio) + 1)
        if type(purchase_date) is datetime.datetime:
            purchase_date = purchase_date.date()
        cost_price = price_at_buy * (1 + fee_ratio_at_buy)
        fractional_years_difference = fractional_years_since(purchase_date, today)
        target_interest_ratio_with_strict_time = compound_interest_ratio(target_annual_profit_interest_ratio, fractional_years_difference)
        target_interest_ratio_with_yearly_time = compound_interest_ratio(target_annual_profit_interest_ratio, math.ceil(fractional_years_difference))
        return intermediate_aggregator(target_interest_ratio_with_strict_time), intermediate_aggregator(target_interest_ratio_with_yearly_time)

    def get(self, stock_name = None):
        if stock_name == None:
            cursor.execute('SELECT name FROM Stocks')
            return {'Available Stocks': cursor.fetchall()}
        cursor.execute(f"SELECT * FROM Stocks WHERE name = '{stock_name}'")
        stock_data = cursor.fetchall()
        if not stock_data:
            return {'message': 'Stock not found'}, 404
        # price_to_sell_with_strict_target, price_to_sell_with_year_target = 
        return [Analyser.target_sale_prices(*stock_data_row[1:]) for stock_data_row in stock_data]


    def post(self, stock_name):
        return {'hello': 'world'}

api.add_resource(Analyser, '/', '/<string:stock_name>')

if __name__ == "__main__":
    table_setup()
    app.run(debug=True)
