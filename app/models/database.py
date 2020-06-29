import datetime
import psycopg2

from flask import g


class Database:
    @staticmethod
    def get_all_stores():
        cur = g.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
                        SELECT *
                        FROM store;
                    """)

        return cur.fetchall()

    @staticmethod
    def add_price(title, price, link, img_url, store, search):
        date = datetime.date.today()
        title = title.replace("'", "\'")

        cur = g.con.cursor()
        cur.execute("""
                        INSERT INTO price
                            (title, price, link, img_url, store, date, search)
                        VALUES
                            (%s,%s,%s,%s,%s,%s,%s)
                    """, (title, price, link, img_url, store, date, search))
        g.con.commit()

        return "Database updated"

    @staticmethod
    def get_search(term):
        term = term.replace("'", "\'")
        cur = g.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f"""
                        SELECT *
                        FROM search
                        WHERE term = '{term}'
                        AND date = CURRENT_DATE
                    """)

        return cur.fetchone()

    @staticmethod
    def new_search(term):
        date = datetime.date.today()
        term = term.replace("'", "\'")

        cur = g.con.cursor()
        cur.execute("""
                        INSERT INTO search
                            (term, date)
                        VALUES
                            (%s,%s)
                    """, (term, date))
        g.con.commit()

        return Database.get_search(term)

    @staticmethod
    def get_prices_by_search_id(id):
        cur = g.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f"""
                        SELECT *
                        FROM price
                        WHERE date = CURRENT_DATE
                        AND search = {id}
                    """)

        return cur.fetchall()
