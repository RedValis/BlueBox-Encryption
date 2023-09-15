import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
from PIL import Image, ImageTk
import cv2
import random
from ttkthemes import ThemedStyle

charmap = list(
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&\'*()_+-=[]{};:,./<>?`~ \n')
coordsx = []
coordsy = []

def encodeChar(char):
    if char not in charmap:
        print(f"Unsupported character: {char}")
        return None
    char = charmap.index(char)
    return char

def decodeChar(char):
    if char > len(charmap):
        return '\x00'
    char = charmap[char]
    return char

def encode_text():
    text = input_text.get("1.0", "end-1c")
    letters = []
    if(len(text) > 32):
        result_label.config(text="Text too long.")
        return

    for i in range(len(text)):
        n = encodeChar(text[i])
        if n is not None:
            randomX = random.randint(1, 254)
            randomY = random.randint(1, 254)
            while (randomX, randomY) in coordsx or (randomX, randomY) in coordsy:
                randomX = random.randint(1, 253)
                randomY = random.randint(1, 253)
            coordsx.append(randomX)
            coordsy.append(randomY)
            letters.append(n)

    img = np.zeros([256, 256, 3], dtype=np.uint8)
    for i in range(256):
        for j in range(256):
            img[i, j] = (66, 126, 245)
    img[0, 0] = (69, 126, 245)
    img[0, 1] = (66, 126, 240)
    currentX = 0
    for i in range(len(letters)):
        coordStringX = str(coordsx[i])
        coordStringY = str(coordsy[i])
        for j in range(len(coordStringX)):
            img[254, 255-currentX-j] = (int(coordStringX[j]), 126, 245)
        for j in range(len(coordStringY)):
            img[255, 255-currentX-j] = (int(coordStringY[j]), 126, 245)
        img[254, 255-currentX-len(coordStringX)] = (65, 125, 245)
        img[255, 255-currentX-len(coordStringY)] = (65, 125, 245)
        currentX += len(coordStringX) + len(coordStringY) + 2
    for i in range(len(letters)):
        img[coordsy[i], coordsx[i]] = (letters[i], 126, 245)

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        img_path = file_path
        Image.fromarray(img).save(img_path)
        result_label.config(text=f"Saved as {img_path}")

def decode_text():
    coordsx.clear()
    coordsy.clear()  # Clear coordinates before decoding

    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    if not file_path:
        return

    img = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
    if img.shape != (256, 256, 3):
        result_label.config(text='Not a bluebox image.')
        return
    if tuple(img[0, 0]) != (69, 126, 245) or tuple(img[0, 1]) != (66, 126, 240):
        result_label.config(text='Not an authentic bluebox image.')
        return

    try:
        currentX = 0
        while True:
            coordStringX = ''
            coordStringY = ''
            if tuple(img[254, 255-currentX]) == (66, 126, 245):
                break
            for i in range(255):
                if tuple(img[254, 255-currentX-i]) == (65, 125, 245):
                    break
                coordStringX += str(img[254, 255-currentX-i][0])
            for i in range(255):
                if tuple(img[255, 255-currentX-i]) == (65, 125, 245):
                    break
                coordStringY += str(img[255, 255-currentX-i][0])
            if not coordStringX or not coordStringY:
                break
            coordsx.append(int(coordStringX))
            coordsy.append(int(coordStringY))
            currentX += len(coordStringX) + len(coordStringY) + 2
    except Exception as e:
        result_label.config(text="Failed to decode.\n" + str(e))
        return

    decoded = []
    for i in range(len(coordsx)):
        decoded.append(decodeChar(img[coordsy[i], coordsx[i]][0]))
    
    decoded_text = ''.join(decoded)
    result_label.config(text="Decoded message: " + decoded_text)
    output_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if output_file_path:
        with open(output_file_path, 'w') as f:
            f.write(decoded_text)
        result_label.config(text=f"Saved as {output_file_path}")


root = tk.Tk()
root.title("The Great Glorious Bluebox")

style = ThemedStyle(root)
style.set_theme("equilux")

frame = ttk.Frame(root, padding=0)
frame.grid(row=0, column=0, padx=0, pady=0)

input_text = tk.Text(frame, height=10, width=40, bg='gray', font=("Helvetica", 12))
input_text.grid(row=0, column=0, padx=10, pady=10)

encode_button = ttk.Button(frame, text="Encode", command=encode_text)
encode_button.grid(row=1, column=0, padx=10, pady=10)

decode_button = ttk.Button(frame, text="Decode", command=decode_text)
decode_button.grid(row=2, column=0, padx=10, pady=10)

result_label = ttk.Label(frame, text="", wraplength=400)
result_label.grid(row=3, column=0, padx=10, pady=10)

root.mainloop()
