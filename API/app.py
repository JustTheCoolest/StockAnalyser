from flask import Flask
from flask_restful import Resource, Api
import oracledb

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

class Analyser(Resource):

    def get(self, stock_name):
        return {'hello': 'world'}
    
    def post(self, stock_name):
        return {'hello': 'world'}
    
api.add_resource(Analyser, '/<string:stock_name>')

if __name__ == "__main__":
    table_setup()
    app.run()
