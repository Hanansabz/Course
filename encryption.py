def encrypt_message(key_encrypt, plaintext):
    #Encrypt the message using the secret key
    encrypted_message = ""
    for char in plaintext:
        #ascii value of character + ascii value of key character (cycling through key)
        encrypted_char = chr((ord(char) + ord(key_encrypt[len(encrypted_message) % len(key_encrypt)])) % 256)
        encrypted_message += encrypted_char
    return encrypted_message

def decrypt_message(key_decrypt, encrypted_message):
    #Decrypt the message using the secret key
    decrypted_message = ""
    for char in encrypted_message:
        #ascii value of character - ascii value of key character (cycling through key)
        decrypted_char = chr((ord(char) - ord(key_decrypt[len(decrypted_message) % len(key_decrypt)])) % 256)
        decrypted_message += decrypted_char
    return decrypted_message



#Get secret key from user
key_encrypt = input("Enter secret key: ")
#Get plaintext message from user
plaintext = input("Enter message to encrypt: ")
encrypted = encrypt_message(key_encrypt, plaintext)
print("Encrypted message:", encrypted)


#Get secret key from user
key_decrypt = input("Enter secret key: ")
#Get encrypted message from user
encrypted_message = input("Enter message to decrypt: ")
decrypted = decrypt_message(key_decrypt, encrypted_message)
print("Decrypted message:", decrypted)