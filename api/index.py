from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from seleniumEdgeFinal import main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.app_context().push()
base_stocks = ['tsla', 'aapl', 'msft','uber', 'pins', 'snap','well','arkk','spy']
#base_stocks = ['tsla']
stocks=[]
class Data(db.Model):
    __tablename__ = 'data'
    ticker = db.Column(db.String(10), primary_key=True)
    content = db.Column(db.String(10000))

    def __repr__(self):
        return f'{self.ticker}: {self.content}'
    
def reset_stocks():
    for i in range(len(base_stocks)):
        stocks.append(base_stocks[i])

def add_stock_to_db(ticker, result):
    the_string = ''.join(result)
    ticker_to_delete = Data.query.get(ticker)
    if ticker_to_delete != None:
        db.session.delete(ticker_to_delete)
    else:
        row = Data(ticker=ticker, content=the_string)
        db.session.add(row)
    db.session.commit()

@app.route('/',)
def index():
    rows = Data.query.all()
    print('data :   ',Data.query.filter_by(ticker='aapl').delete())
    if rows:
        print(rows)
        return render_template('index.html', rows=rows)
    else:
        return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    data_to_db = []
    retry_count = 0
    if len(stocks) ==0:
        reset_stocks()
    print('stocks: ',stocks)
    while retry_count<4:
        try:
            if len(stocks) >= 1:
                for stock in stocks:
                    ticker, result = main(stock)
                    data_to_db.append(Data(ticker=ticker, content='\n'.join(result)))

                    ticker_to_delete = Data.query.get(stock)
                    if ticker_to_delete != None:
                        db.session.delete(ticker_to_delete)
                    stocks.remove(stock)
            else:
                break
        except Exception as e:
            app.logger.error(e)
            print(e)
            retry_count+=1
            continue
    db.session.add_all(data_to_db)
    db.session.commit()
    print('all: ',Data.query.all())
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
