from flask import Flask, render_template, g
import sqlite3 as sql

from models.database import Database as db

app = Flask(__name__)


@app.before_request
def before_request():
    g.db = sql.connect('pilot_fish.db')
    g.db.row_factory = sql.Row


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


if __name__ == '__main__':
    app.run(debug=True)