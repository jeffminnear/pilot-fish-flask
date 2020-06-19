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


