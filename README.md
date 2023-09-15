# BlueBox-Encryption
A small encryption system made in python, encrypts any message below 32 characters into a blue square png

there's not much else to it, I've added a small tkinter UI to make it easier to use for laymen, the functionality remains the same, encrypts messages into a blue box


#   Encoding
The encode_text function is responsible for encoding a user-provided text message into an image. It does the following:

- Takes the input text from a tkinter Text widget.
- Checks if the text length exceeds 32 characters and displays an error if it does.
- For each character in the input text, it encodes the character into a numeric value based on the charmap.
- Generates random X and Y coordinates for each character's position in the image.
- Creates a 256x256 pixel image with a blue background.
- Embeds the encoded characters into the image at their respective coordinates.
- Prompts the user to save the encoded image as a PNG file.

# Decoding
The decode_text function decodes an encoded image back into a text message. It does the following:

- Prompts the user to select an image file (assumed to be an encoded Bluebox image).
- Checks if the image is a valid Bluebox image by verifying specific color values at predefined coordinates.
- Extracts the X and Y coordinates of the encoded characters from the image.
- Decodes the characters using the charmap and the extracted pixel values.
- Displays the decoded text message to the user and allows saving it as a text file.

