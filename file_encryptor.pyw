import random
import string
from tkinter import *


def xor_mask(file_name, key):
    key_index = 0
    content = ''
    encrypted_content = ''
    max_key_index = len(key) - 1
    # extraigo el contenido del archivo
    with open(file_name, 'r') as f:
        content = f.read()

        # aplico la mascara xor
        for char in content:
            encrypted_char = ord(char) ^ ord(key[key_index])
            encrypted_content += chr(encrypted_char)
            if key_index >= max_key_index:
                key_index = 0
            else:
                key_index += 1

    # reemplazo el contenido original por el enmascarado.
    with open(file_name, 'w') as f:
        f.write(encrypted_content)

    print(f'Encrypted content: {encrypted_content}')


def graphic_window():

    root = Tk()
    root.title("File encryptor")
    root.master.iconbitmap("icon.ico")
    root.geometry("500x250")
    root.config(bg="DeepSkyBlue4")

    root.resizable(0,0)

    root.mainloop()

if __name__ == '__main__':

    graphic_window()
    print("nombre de archivo:")
    file_name = input()
    print("clave:")
    key = input()

    xor_mask(file_name=file_name, key=key)