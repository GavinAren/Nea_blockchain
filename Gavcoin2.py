# Module 2 - Create a cryptocurrency

# Flask==0.12.2
# client: https://www.getpostman.com/

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
#to parse url for all nodes
from uuid import uuid4
from urllib.parse import urlparse
#for encryption
# import Crypto
# from Crypto.PublicKey import RSA
# from Crypto import Random
# import base64
# #to run the timer
from threading import Timer
from database_nea import database
import time

#Building the basic blokchain
class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = [] #has to be before the create block since that needs the transcations already
        self.create_block (proof =1, prev_hash = '0') # calling a function I will make in the future, prev_hash is 0 since this is for the Genesis block which has no prevoius hash
        self.nodes = set()    #set like a maths set
        self.block_mined = False #becomes true every 10 minutes or when TRanscations list has reached its limit

    def create_block(self, proof, prev_hash): #a block is created right after its proof of work is done in another function so we need to take that proof as a parameter
        block = {'index': len(self.chain) + 1 ,
                 'timestamp':str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash' : prev_hash,
                 'transactions': self.transactions} #defined all keys and value pairs in the block
        #need to empty th elist of tranactions
        transaction= []
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1] #returns the last index block in the blockchain list

    #proof of work has to be worked out by miners and has to be hard to work out but easy to verify by others
    def proof_of_work(self, prev_nonce):
        current_nonce = 1 #trying to find the right nonce, so we start at 1
        check_proof = False #will change to true when proof is found
        while check_proof is False: #need to keep incrementing the nonce until roght one is found
            hash_operation =  hashlib.sha256(str(current_nonce**2 - prev_nonce**2).encode()).hexdigest() # need to make the operation non-symmetrical
            #the encode pads the the hash operation with a b at the beginning so the sha256 function requires it, Hexdigest turns it into hexadecimal

            # we have set the difficulty fo 4 leading zeros
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                current_nonce +=1
            return (current_nonce)

    def hash(self, block):
        # we need to take the dumps funtion from the json library to turn it inot a string as well as get it ready for a json format
        encode_block= json.dumps(block, sort_keys = True).encode() #sort_keys sorts our dictionary in terms of keys
        return hashlib.sha256(encode_block).hexdigest()

    def validate_chain(self, chain):
        prev_block =chain[0]
        block_index =1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block): #
                return False
            prev_proof = prev_block['proof']
            proof = block ['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - prev_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            prev_block = block
            block_index +=1
        return True

    def new_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender ,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_prev_block()
        return previous_block['index'] + 1

    def return_true(self):
        return True #simply returns True whenever called

    def block_miner(self):
            value = True
            if len(self.transactions) >= 10:
                return value
            else:
                time.sleep(1)
                return True
                # mining_timer = Timer(30.0, self.return_true()) # required a funtion as 2d parametre so had to create a return_ture function
                # mining_timer.start()#starts the timer, at the end of the timer , the funtion above is called which reuturns true

                #the consesnsus algorithms needs to make sure that all the blocks in the chain have the same latest copy of the blockchain
    def  new_node(self, node_address): #need to add new verified nodes to the network
        #need to parse the address of the node, parse means
        parsed_url = urlparse(node_address)
        self.nodes.add(parsed_url.netloc) #can't use append since nodes is a set, not a list #netlock just returns the address of that node out of all the mutilple things that urlparse would've returned, we only need the netloc
#now we are creating a web app using Flask to interact with the blockchain
#http://127.0.0.1:5000/ use the same address for all nodes except increment the 5000 at the end for all new nodes

    '''def rsakeys():
        length = 1024 #this lenght is still considered very safe and is recommended by US government
        privatekey = RSA.generate(length, Random.new().read)
        publickey = privatekey.publickey()
        return privatekey, publickey

    def sign(privatekey, data):
        return base64.b64encode(str((privatekey.sign(data, ''))[0]).encode())

    def verify(publickey, data, sign):
        return publickey.verify(data, (int(base64.b64decode(sign)),))'''


    def replace_chain(self): #funtion that spots the longest chain held by any node and then makes sure all other nodes with a shorter chain have the same chain
        full_network = self.nodes
        longest_chain = None
        max_len_chain = len(self.chain)
        for node in full_network:
#need to sed a request to get teh length of all the chains in the network to get the longest one
            response = requests.get( f'http://{node}/get_blockchain') #the arguement hta the get funtion expects the full url http://127.0.0.1:5000/get_blockchain
                    # to generalise the node from 50 to the exact address fo the specific node, we just use the self.nodes
                    #returns the dict with 'chain' and 'length'
            if response.status_code == 200:
                length = response.json()['length'] #returns the length of the chain
                chain = response.json()['chain']
                if length > max_len_chain and self.validate_chain(chain):
                    max_len_chain = length
                    longest_chain = chain

        if longest_chain: #menas is longest_chian isn't none
            self.chain = longest_chain
            return True
        return False #is original alue isn't updated then our chain was the longest one so no changes required


    # def send_to_db(self):
    #     return self.chain

app = Flask(__name__)

#Creating an address for the node on port 5000
node_address = str(uuid4()).replace( '-' , '' )#uuid4 funtion returns a randomly generated unique address for anything, it returns is long number with lots of hyphens so we need to get rid of those too
 #needed because the miner needs to be rewarded inGavcoin from the node to itself


#creating one instance  of the blockchain class
blockchain = Blockchain()
storage = database()
#now we need to mine our blockchain
#the route() decorator specifies the url that should trigger teh mineing function
@app.route('/mine_block', methods = ['GET']) #the address is always the same http://127.0.0.1:5000/ apart from teh last part we defined
def mine_block(): #well get everything we need from the blockchain class
    go_ahead = blockchain.block_miner()
    print (go_ahead)
    if go_ahead == True:
        prev_block = blockchain.get_prev_block()
        prev_proof = prev_block['proof'] #key is proof
        proof = blockchain.proof_of_work(prev_proof)
        prev_hash= blockchain.hash(prev_block)
        blockchain.new_transaction(node_address, 'Gavin', 10) #???why is receiver a name
        block = blockchain.create_block(proof, prev_hash)
        #we have the block and it's been appended to the blockchain
        #need to display in UI using postman interface using JSON format
        response = {'message':'Congratulations, you just mined a block',
                    'index': block['index'],
                    'timestmap': block['timestamp'],
                    'proof': block['proof'],
                    'prev_hash':block['prev_hash'],
                    'transactions': block['transactions']}
        #need to add a http code to tell the GET request that everything is OK and its a success
        storage.store_block(block['index'], block['timestamp'], block['proof'], block['prev_hash'], 'ololol')
        return jsonify(response), 200

    else:
        response = {'message':'Everything is broken'}
        return jsonify(response), 400

#to display the full blockchain
@app.route('/get_blockchain', methods = ['GET'])
def get_blockchain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/valid', methods=['GET'])# Checking if the Blockchain is valid
def valid():
    is_valid = blockchain.validate_chain(blockchain.chain)
    if is_valid:
        response = {'message': 'All good, the blockchain is valid'}
    else:
        response = {'message': 'We have a problem, invalid blockchain'}
    return jsonify(response), 200


@app.route('/new_transaction', methods = ['POST'])
def new_transactions():
    json_file = request.get_json() #need t oretrieve the json file containng the transaction which needs tot he posted
    transaction_keys =  ['sender', 'receiver', 'amount'] #making sure that all keys are present in the json file retrieved
    if not all (key in json_file for key in transaction_keys): # if transacition is missing any of the keys, transaction_keys  is list of the needed keys
       return 'some elements of the transaction are missing' , 400#need to return the eroor http status code
    index = blockchain.new_transactions(json_file['sender'], json_file['receiver'], json_file['amount']) #need to add transaction ot the next mined block
 #?why is it retunred wothout jsonify
    response = {'message': f'This transaction will be added to block {index}'} #the f means the index will be replaced by the rigth value instead of just saying index
    return jsonify(response), 201


#connecting a new node, we wil create a new node and then register it, we need to add it to a json file with the full list of nodes on the network and post it
@app.route('/connect_new_node', methods = ['POST'])
def connect_new_node():
        json = request.get_json()
        json.get('node')#we need to get addresses in the json file before we cqn use the new_node funtion since it requires the new adress as a parameter
        #a sinlge node key ni the json file will have the value as all the node addresses
        all_nodes = json.get('nodes')
        if nodes is None: #checking that the list of nodes ins't empty
            return 'no nodes found', 400
        for node in all_nodes:
            blockchain.new_node(node) #will add all the nodes tp the network
        response = {'message':'All nodes are connected. The Gavcoin blockchain now contains nodes:',
                    'total_nodes':list(blockchain.nodes)}
        return jsonify(response), 201

@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain() #since it returns true whenever chain is updated
    if is_chain_replaced:
        response = {'message': 'The chain has been replaced with the longest one',
                    'Full_chain':blockchain.chain} #displays the new updated chain to them
    else:
        response = {'message': 'All good, chain is upto date',
                               'Full_chain': blockchain.chain}
    return jsonify(response), 200

#???I t took me time to realise that these post get requests are not going through or every other node but rather, only there to serve one node and it gets that one node's chain upto date

#DECENTRALISATION OF THE BLOCKCHAIN by creating a network
#transactions make a blockchain a crptocureency
#1- create transctions
#2- need to create  a consensus funtion to make sure everyone has the same copy of the chain

#originally transaction are not in a block, they take place separately and then a record of them is added tot the blockchain whena new block is mined, since it added to the bolck.
#create a list with a limited length, t=when its full a block will be created and then it will be polpulated with these transactions, then mined and put through to the blockchain

# Running the app
app.run(host='0.0.0.0', port=5000)
