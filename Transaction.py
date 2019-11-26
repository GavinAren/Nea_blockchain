import datetime
import collections
import binascii
#imports to sign transactions, create hash of the objects, required for PKI
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

#This class allows for exchange of Virtual Currency to complete a Transaction
#When money has to be received, someone else will create a transaction and specify your public key in it.
class Transaction:

	def __init__(self, sender=None, recipient=None, value=None):
		self.sender = sender
		self.recipient = recipient
		self.value = value
		self.time = datetime.datetime.now()

	#This combines all the above 4 instance variables into a DICTIONARY object. This is required so that we can access the 
	#entire transaction information through a single variable.
	def for_dictionary(self):
		if self.sender == "Genesis":
			identity = "Genesis"
		else:
			identity = self.sender.identity #is this an object of the class being created? what does the identity method return and store here?
		return collections.OrderedDict({'sender': identity,#we havent checked if identity exists, will it not use addressses for nodes?? using public keys, like an email
					'recipient':self.recipient,
					'value':self.value,
					'time':self.time})

	#This method will sign the Dictionary Object using the Private Key of the sender.
	#Done using PKI with SHA algorithm. Generated signature is decoded to get ASCII representation 
	#for printing and storing it in Blockchain.
	def sign_transaction(self):
		private_key = self.sender._private_key
		signer = PKCS1_v1_5.new(private_key)
		h = SHA.new(str(self.for_dictionary()).encode('utf8')) #utf 8 uses 8 bits to store characters and includes unicode characters rather than just ascii
		return binascii.hexlify(signer.sign(h)).decode('ascii')


	#Method will be invoked to display all the Transactions
	def display_transaction(self, transactions_list):	
		for transaction in transactions_list:
			dict = transaction.for_dictionary()
			print("\nSender: "+dict['sender'])
			print("\nReceiver: "+dict['recipient'])
			print("\nValue: "+str(dict['value']))
			print("\nTime: "+str(dict['time']))
			print('-------------------------------\n\n')
						#connect my blocchain somewhere here to record these transactions permamaneently?????
		#how will everyone store a copy of the database? dont do that
		
#need to check if person has coins before paying, when initialisng a client, what is wallet balance
#login snot the most important, rather spend time
#start with limited coins