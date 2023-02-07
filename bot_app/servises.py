import random


chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def new_password():
    password = ''
    for i in range(6):
        password += random.choice(chars)
    return password

