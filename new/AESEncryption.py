# from Crypto.Cipher import AES

# BLOCK_SIZE = 16

# class AESEncryption:
#     def __init__(self, key, iv):
#         self.key = key
#         self.iv = iv

#     def encrypt(self, message):
#         message = self._pad(message)
#         cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
#         encryptedMsg = cipher.encrypt(message)
#         return encryptedMsg

#     def decrypt(self, message):
#         cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
#         decryptedMsg = cipher.decrypt(message)
#         decodedMsg = decryptedMsg.decode() 
#         return self._unpad(decodedMsg)

#     def _pad(self, s):
#         padded = s + (((BLOCK_SIZE - len(s)) % BLOCK_SIZE) * chr((BLOCK_SIZE - len(s)) % BLOCK_SIZE))
#         return padded

#     def _unpad(self, s):
#         lastCharValue = ord(s[len(s)-1:])
#         isPadded = lastCharValue < BLOCK_SIZE
#         if not isPadded:
#             return s
#         unpadded = s[:-lastCharValue]
#         return unpadded