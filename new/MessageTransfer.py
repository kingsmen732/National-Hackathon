# import json
# from AESEncryption import *

# key = 'O7%8I#8!Z*9VV&#J'
# iv = 'U^PKMR@D7*1JU&J6'

# class MessageTransfer:
#     def __init__(self):
#         self.aes = AESEncryption(key, iv)

#     def sendJson(self, stream, message):
#         stream.send(self.aes.encrypt(json.dumps(message)))

#     def sendString(self, stream, message):
#         stream.send(self.aes.encrypt(message))

#     def receiveJson(self, stream, bufferSize = 1024):
#         return json.loads(self.aes.decrypt(stream.recv(bufferSize)))

#     def receiveString(self, stream, bufferSize = 1024):
#         return self.aes.decrypt(stream.recv(bufferSize))
