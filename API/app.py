from flask import Flask
from flask_restful import Resource, Api, reqparse
import oracledb
import datetime
import dateutil.relativedelta

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

def years_and_remaining_days_since(input_date, today = datetime.datetime.now().date()):
    """ Untested for negative dates """
    time_difference_from_now = dateutil.relativedelta.relativedelta(today, input_date)
    years_difference = time_difference_from_now.years
    input_date_in_latest_year = input_date + dateutil.relativedelta.relativedelta(years=years_difference)
    days_remainder_difference = (today - input_date_in_latest_year).days
    input_date_in_its_next_year = input_date_in_latest_year.replace(year = input_date_in_latest_year.year + 1)
    total_days_in_latest_year = (input_date_in_its_next_year - input_date_in_latest_year).days
    return (years_difference, days_remainder_difference, total_days_in_latest_year)

def compound_interest_ratio(rate, time):
    ratio = (1 + rate) ** time
    return ratio

class Analyser(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price_at_buy', type=float)
    parser.add_argument('purchase_date', type=lambda string: datetime.datetime.strptime(string, '%Y-%m-%d'))
    parser.add_argument('fee_ratio_at_buy', type=float)
    parser.add_argument('fee_ratio_at_sell', type=float)
    parser.add_argument('capital_gains_tax_ratio', type=float)
    parser.add_argument('target_profit_ratio', type=float)

    @staticmethod
    def target_profits(price_at_buy, fee_ratio_at_buy, fee_ratio_at_sell, capital_gains_tax_ratio, target_profit_ratio):
        def _intermediate_aggregator():
            pass
        pass

    def get(self, stock_name = None):
        if stock_name == None:
            cursor.execute('SELECT name FROM Stocks')
            return {'Available Stocks': cursor.fetchall()}
        cursor.execute(f"SELECT * FROM Stocks WHERE name = '{stock_name}'")
        stock_data = cursor.fetchone()
        if not stock_data:
            return {'message': 'Stock not found'}, 404
        # price_to_sell_with_strict_target, price_to_sell_with_year_target = 
        return Analyser.target_profits(None, None, None, None, None)


    def post(self, stock_name):
        return {'hello': 'world'}

api.add_resource(Analyser, '/', '/<string:stock_name>')

if __name__ == "__main__":
    table_setup()
    app.run(debug=True)
