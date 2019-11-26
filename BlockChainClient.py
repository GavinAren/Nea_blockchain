import Client
import Transaction
import Block
import Miner
from os import system, name

#As a First, Initialize all the Nodes and add them to a dictionary
print("Initializing all the Nodes ... ")
user1inst = Client.Client()
user2inst = Client.Client()
user3inst = Client.Client()
user4inst = Client.Client()
user5inst = Client.Client()
nodeMap = {"user1":user1inst, "user2":user2inst, "user3":user3inst, "user4":user4inst, "user5":user5inst}
print('All the Nodes initialized')

#Public Transaction Queue - A Global List. Each newly created Transaction will be appended here
global_chain_transactions = []

#Public List of Blocks - To be chained in the actual Blockchain
global_GavCoins = []

#Global variable as each block needs the value of the previous block's hash
global_last_block_hash = ""

#To track number of transactions mined - transaction index
global_last_transaction_index = 0

#Method to get the User Choice as input
def get_user_choice():
	user_input = input('Your Choice: ')
	return user_input

#Method to Add a New Transaction. After the Transaction, there is a need to sign the transaction, so will call the sign_transaction method.
#This will return the signature in printable format, which can be persisted for reference.
def add_new_transaction():
	clientInstance = Client.Client()
	sender = input('Enter the name of the sender: ')
	recipient = input('Enter the name of the receiver: ')
	nosCoin = input("Enter the number of Coins to be Transferred: ")
	#nodeList = clientInstance.get_nodes()
	#print(nodeList)
	#Checks if the entered values exists as nodes
	if (sender in nodeMap) and (recipient in nodeMap):
		#print("Nodes are existing")
		transactionInstance = Transaction.Transaction(nodeMap[sender],nodeMap[recipient].identity,nosCoin)
		transactionInstance.sign_transaction()
		global_chain_transactions.append(transactionInstance)
	else:
		print("Nodes are not existing") 

#Logic to clear the console for clean inputs
def clear_screen():
	#OS Name for Ubuntu is posix - OS NAME check
	if name == 'posix':
		_ = system('clear')
	elif name == 'nt':
		#For Windows
		_ = system('cls')
	#print("Name is: ", name)

#Menu Option for the Blockchain Users
waiting_for_input = True
while waiting_for_input:
	print("Please Choose from the below options: ")
	print("1 - To Add a New Transaction")
	print("2 - See the Transactions Added")
	print("3 - Start a Block Chain")
	print("4 - Add Blocks to the Blockchain")
	print("5 - To see all the Blocks in the Blockchain")
	print("6 - QUIT")
	user_choice = get_user_choice()
	print("USER CHOICE: ", user_choice)
	if user_choice == '1':
		print("User Selected 1")
		clear_screen()
		add_new_transaction()
	
	elif user_choice == '2':
		clear_screen()
		print("The total number of transactions added: ", len(global_chain_transactions))
		print("The transactions are: ")
		trans = Transaction.Transaction()
		trans.display_transaction(global_chain_transactions)
	
	elif user_choice == '3':
		clear_screen()
		print("Starting the Blockchain. This will start a chain afresh with a Genesis Block")
		t0 = Transaction.Transaction("Genesis",user1inst.identity,500)
		block0 = Block.Block()
		#Initializing the block constituents (previous block and nonce) as 'None' as this is the first block of the chain
		block0.previous_block_hash = None
		block0.Nonce = None
		block0.verified_transactions.append(t0)
		
		#Now, hash the Genesis block and store the value in the global variable
		hashVal = hash(block0)
		global_last_block_hash = hashVal
		print("Adding the Genesis Block to the Blockchain")
		global_GavCoins.append(block0)
	
	elif user_choice == '4':
		clear_screen()
		block = Block.Block()
		miner = Miner.Miner()
		for i in range(3):
			temp_transaction = global_chain_transactions[global_last_transaction_index]
			#TBD - VALIDATE TRANSACTION
			#TBD - BELOW TO BE Added only if the transaction is valid
			block.verified_transactions.append(temp_transaction)
			global_last_transaction_index += 1
		
		block.previous_block_hash = global_last_block_hash
		block.Nonce = miner.mine(block, 2)
		digest = hash(block)
		global_GavCoins.append(block)
		global_last_block_hash = digest
		
	
	elif user_choice == '5':
		clear_screen()
		blockInstance = Block.Block()
		blockInstance.showBlockchain(global_GavCoins)
	
	elif user_choice == '6':
		waiting_for_input = False
	
	else:
		print("Invalid Input. Please choose from the options suggested")
 #need to add proof of work,  need to give al miners a chance to mine blockcs.
 #this is more of a
 #menu options give over a browser, new window to use multiple nodes different sessions