#Login page for the system, first file to be executed
from random import choice
from string import ascii_uppercase
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import string
import random

class login(): #login page

    def __init__(self):
        account = input('Do you have an existing account? Y/N')
        if account == 'Y'  or account == 'y' or account == 'yes':
            self.start() #noral login process
        elif account == 'N'  or account == 'n' or account == 'no':
            self.register() #registration process
        else:
            exit()

        #initialising variables
        self.username = ''
        self.user_valid=' '.join(random.choice(string.ascii_lowercase) for i in range(16))#generates a session password if the user's username is recognised
        self.session_key = get_random_bytes(16)  # generates a new session key as soon as login page is shown to encrypt the actual data with AES encryption
        self.counter = 0

    def start(self): #logging in process
        self.username = input('USERNAME:  ')

        print(self.user_valid)
        #self.user_valid = database.validate(self.username) #returns the public key for that user if user exists in database
        # while self.user_valid == False and self.counter <=3:
        #     self.counter+= 1
        #     self.username = input('Please enter a valid username: ')
        #     self.user_valid = database.validate(self.username)
        # if self.user_valid == False:
        #     print ('Login failed')
        #     exit()
        # else:
            #plaintext = ' '.join(choice(ascii_uppercase) for i in range(128))
            #plaintext.
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        # with open('encrypted_data.bin', 'wb') as out_file:
        #recipient_key = RSA.import_key(self.user_valid)
        user_password  = self.user_valid.encode('utf-8')
        recipient_key = RSA.import_key(public_key)
        self.session_key = get_random_bytes(16)  # creates a ranodmsession key to encrypt the actual data AES
        cipher_rsa = PKCS1_OAEP.new(recipient_key)  # holding the public key, allows us to encrypt an arbitary amount of data
        password = cipher_rsa.encrypt(user_password)

        sender_key = RSA.import_key(private_key)
        decipher_rsa = PKCS1_OAEP.new(sender_key)
        plain = (decipher_rsa.decrypt(password)).decode('utf-8')
        print (self.session_key, '++',cipher_rsa,'++',password,'++',plain)
          # cipher_aes = AES.new(session_key, AES.MODE_EAX)
            # data = b'key'  # has to be plaintext
            # ciphertext, tag = cipher_aes.encrypt_and_digest(data)
            # out_file.write(cipher_aes.nonce)
            # out_file.write(tag)
            # out_file.write(ciphertext)
            # print(session_key, '+', ciphertext)




login = login() #creates an object for login class which causes the initialisation