import sqlite3
from sqlite3 import Error
# It is an easy to use serverless database, used in mobile applications usually

class login_db():
#table only needs to be created once, then comment everything out

    def __init__(self, database  ='login.db'):
        self.db= None#sqlite3.connect('login.db') as db
        self.cursor = None
        self.database = database

    def connect(self):
        self.db = sqlite3.connect(self.database)
        self.cursor = self.db.cursor()

        try:
            login_db =('''
                            CREATE TABLE IF NOT EXISTS login(
                            num_users INTEGER PRIMARY KEY ,
                            username VARCHAR (40) NOT NULL,
                            public_key VARCHAR (2048) NOT NULL);
                            ''')
            self.cursor.execute(login_db)
        except Error as e:
            print(e)
            return (False)

    def query(self, username_entered):

    #     insert = " INSERT INTO full_chain(timestamp, proof, previous_hash, transactions) VALUES (? , ?, ? , ? )"  # ,{timestamp, proof, previous_hash, transactions}
    #
    #
    # parameters = (timestamp, proof, previous_hash, transactions)
    # self.cursor.execute(insert, parameters)
    # self.db.commit()
        self.cursor.execute('SELECT ({public_key}) FROM {table_name} WHERE {username}= username_entered '. \
                  format(public='public_key', table_name='login', username='username'))


        all_rows = self.cursor.fetchall()
        print(all_rows)


    def close(self):
        self.db.close()

logintime = login_db()
logintime.connect()
logintime.query('yayeet')
logintime.close()