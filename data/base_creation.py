import random
import sqlite3
from json import dumps, loads


class DataBase:
    """Main Data Base need to:
        - create db
        - add user
        - show data
        - clear db
        - start giveaway"""
    
    def __init__(self):
        self.con = sqlite3.connect('data/giveaway.db')
        self.cursor = self.con.cursor()


    def create_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS classic_giveaway (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            give_id INTEGER,
                            number_of INTEGER,
                            number_wins INTEGER,
                            nicknames TEXT DEFAULT "[]"
        ) """)
        self.con.commit()


    def close(self):
        self.cursor.close()


    def insert_data(self, give_id, num_of, num_w):

        insert = (give_id, num_of, num_w)

        self.cursor.execute("""SELECT * FROM classic_giveaway WHERE give_id=?""", (give_id,))
        res = self.cursor.fetchall()

        if len(res) == 0:

            self.cursor.execute("""INSERT INTO classic_giveaway
                                (give_id, number_of, number_wins) 
                                VALUES (?, ?, ?)""", insert)
            self.con.commit()
        else:
            print('Give_id is in da base')


    def show_data(self, give_id):
        self.cursor.execute("SELECT * FROM classic_giveaway WHERE give_id=?", (give_id,))
        print(self.cursor.fetchall())


    def show_all(self):
        self.cursor.execute("SELECT * FROM classic_giveaway")
        print(self.cursor.fetchall())


    def add_user(self, new_user, give_id): 

        self.cursor.execute("SELECT number_of FROM classic_giveaway WHERE give_id=?", (give_id,))
        num_of = self.cursor.fetchone()[0]
        

        self.cursor.execute("SELECT nicknames FROM classic_giveaway WHERE give_id=?", (give_id,))
        res = self.cursor.fetchone()
        user_lits = loads(res[0])
        
        if new_user not in user_lits and len(user_lits) < num_of:
            user_lits.append(new_user)

            insert = (dumps(user_lits), give_id)
        

            self.cursor.execute("UPDATE classic_giveaway SET nicknames = ? WHERE give_id = ?", insert)
            self.con.commit()
            return True
        elif len(user_lits) == num_of:
            return 'full'
        return False


    def clear_db(self):
        self.cursor.execute("DELETE FROM classic_giveaway")
        print('db was cleared!')
        self.con.commit()


    def start_give(self, give_id):

        self.cursor.execute("SELECT number_wins FROM classic_giveaway WHERE give_id=?", (give_id,))
        
        try:
            num_w = self.cursor.fetchone()[0]
        except TypeError:
            return []

        self.cursor.execute("SELECT nicknames FROM classic_giveaway WHERE give_id=?", (give_id,))
        res = self.cursor.fetchone()
        user_lits = loads(res[0])

        if len(user_lits) < num_w:
            return []

        winners = random.sample(user_lits, num_w)

        return winners

# db = DataBase()

# db.create_db()
# db.insert_data(1, 5, 2)
# print(db.add_user(new_user='nicksttar5', give_id=1, num_of=5))
# db.show_data(1)


# db.show_all()
# db.clear_db()