from aes_pkcs5.algorithms.aes_ecb_pkcs5_padding import AESECBPKCS5Padding

key = "PISMJOD1G6P0VTQ2"
password = "E@sY1n4t"

def encrypt(data,key):
    cipher = AESECBPKCS5Padding(key, "b64")
    encrypted = cipher.encrypt(data)
    print("encrypted",encrypted)
    return encrypted

def decrypt(enc_data,key):
    cipher = AESECBPKCS5Padding(key, "b64")
    decrypted = cipher.decrypt(enc_data)
    print("decrypted",decrypted)
    return decrypted