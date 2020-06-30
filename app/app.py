from flask import Flask, render_template, g, request, redirect
import psycopg2.extras

from local import DB_PASSWORD, SECRET_KEY
from models.database import Database as db
from scraper import Scraper as scrape

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.before_request
def before_request():
    g.con = psycopg2.connect(dbname='pilot_fish',
                             user='postgres',
                             host='localhost',
                             password=DB_PASSWORD,
                             cursor_factory=psycopg2.extras.DictCursor)
    create_tables()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.con.close()


@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/stores')
def get_stores():
    stores = db.get_all_stores()
    return render_template('store.html', stores=stores)


@app.route('/search', methods=['POST'])
def searchbar():
    term = request.form['term']
    return redirect(f'/search/{term}')


@app.route('/search/<string:term>', methods=['GET'])
def search_stores(term):
    search = db.get_search(term)
    if search is None or search == "" or search == []:
        search = db.new_search(term)
        results = scrape.steam(term)
        for result in results:
            db.add_price(title=result['title'],
                         price=result['price'],
                         link=result['link'],
                         img_url=result['img_url'],
                         store=result['store'],
                         search=search['id'])
    else:
        results = db.get_prices_by_search_id(search['id'])

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
    cur = g.con.cursor()
    cur.execute("""DROP TABLE IF EXISTS store""")

    cur.execute("""
                    CREATE TABLE IF NOT EXISTS store
                    (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR NOT NULL
                    );
                """)

    cur.execute("""
                    INSERT INTO store
                        (name)
                    VALUES
                        ('Steam'),
                        ('GreenManGaming'),
                        ('GOG')
                """)

    cur.execute("""
                    CREATE TABLE IF NOT EXISTS search
                    (
                        id SERIAL PRIMARY KEY,
                        term VARCHAR NOT NULL,
                        date DATE NOT NULL
                    );
                """)

    cur.execute("""
                    CREATE TABLE IF NOT EXISTS price
                    (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR NOT NULL,
                        price VARCHAR NOT NULL,
                        link VARCHAR NOT NULL,
                        img_url VARCHAR NOT NULL,
                        store VARCHAR NOT NULL,
                        date DATE NOT NULL,
                        search INTEGER NOT NULL,
                        FOREIGN KEY(search) references search(id)
                    );
                """)

    g.con.commit()


if __name__ == '__main__':
    app.run(debug=True)
