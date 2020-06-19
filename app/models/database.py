import datetime

from flask import g


class Database:
    @staticmethod
    def get_all_stores():
        cur = g.db.cursor()
        cur.execute("""
                        SELECT *
                        FROM store;
                    """)

        return cur.fetchall()


    @staticmethod
    def add_price(title, price, store):
        date = datetime.date.today()

        cur = g.db.cursor()
        cur.execute("""
                        INSERT INTO price
                            (title, price, store, date)
                        VALUES
                            (?,?,?,?)
                    """, (title, price, store, date))
        g.db.commit()

        return "Database updated"

