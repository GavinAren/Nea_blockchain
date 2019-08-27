import sqlite3
# It is an easy to use serverless database, used in mobile applications usually
class database():

    # chain.execute( ''' CREATE TABLE  full_chain(
    #                                 block_index integer ,
    #                                     timestamp blob,
    #                                 proof integer ,
    #                                 previous_hash integer,
    #                                 transactions TEXT
    #                                 ) ''')
    # table only needs to be created once, then comment everything out
    # conn = sqlite3.connect('full_blockchain.db')
    # chain = conn.cursor()
    def __init__(self):
        self.connect= sqlite3.connect('full_blockchain.db')
        self.chain = self.connect.cursor()
        # self.index = index
        # self.timestamp = timestamp
        # self.proof = proof
        # self.previous_hash = previous_hash
        # self.transactions = transactions

    def  store_block(self,index, timestamp, proof, previous_hash, transactions):

        self.chain.execute("INSERT INTO full_chain VALUES (?,?,?,?,?)",{index, timestamp, proof, previous_hash, transactions})
        self.connect.commit()

        #:block_index, :timestamp, :proof ,:previous_hash, :transactions   'block_index':index, 'timestamp':timestamp, 'proof' : proof, 'previous_hash':previous_hash, 'transactions': transactions
        # chain.execute('''INSERT INTO full_chain VALUES (1, 0,0,120,'bob to alice')''')
        # chain.execute("SELECT * FROM full_chain WHERE transactions='bob to alice'"
        # block1 = Blockchain()
        # p = block1.send_to_db()
        # print (p)
        # chain.execute('INSERT INTO full_chain VALUES (1, 0,0,120,:transactions )', {'transactions': p})
        # chain.execute("SELECT * FROM full_chain WHERE transactions= p")
        # print(chain.fetchall())
        self.conn.close()





    #conn.commit() #commits the current transaction, incase something doesn't show up the in the database


#how do I split up each block and store it into the database
#create a loop that fetches a block everytime a new one is created or check for a new block every 10 minutes
#if there is a new block,

#currently its not letting me test things beacuse the server begins, how do i interact with it?
              
#flask SQLAlchemy is an ORM(Object Relational Matter), can use any database with it eg.sqlite
#https://github.com/CoreyMSchafer/code_snippets/blob/master/Python-SQLite/sqlite_demo.py