from flask import Flask, render_template, g, request
import sqlite3 as sql

from models.database import Database as db
from scraper import Scraper as scrape

app = Flask(__name__)


@app.before_request
def before_request():
    g.db = sql.connect('pilot_fish.db')
    g.db.row_factory = sql.Row
    create_tables()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/stores')
def get_stores():
    stores = db.get_all_stores()
    return render_template('store.html', stores=stores)


@app.route('/search/<string:query>', methods=['GET'])
def search(query):
    results = scrape.steam(query)
    return render_template('results.html', results=results)


@app.route('/newprice')
def new_price():
    return render_template('newprice.html')


@app.route('/add_price', methods=['POST'])
def add_price():
    title = request.form['title']
    price = request.form['price']
    store = request.form['store']

    db.add_price(title=title, price=float(price), store=store)
    return render_template('newprice.html')


def create_tables():
    cur = g.db.cursor()
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS store
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                    );
                """)

    cur.execute("""
                    CREATE TABLE IF NOT EXISTS price
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        price FLOAT NOT NULL,
                        store TEXT NOT NULL,
                        date TEXT NOT NULL,
                        search INTEGER NOT NULL,
                        FOREIGN KEY(search) references search(id)
                    );
                """)

    cur.execute("""
                    CREATE TABLE IF NOT EXISTS search
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        term TEXT NOT NULL,
                        date TEXT NOT NULL
                    );
                """)


if __name__ == '__main__':
    app.run(debug=True)
