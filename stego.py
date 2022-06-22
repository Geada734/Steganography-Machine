# Magical stegonography machine usage:
#
# This script encodes a message contained in an image inside
# another image using the PIL libary for Python.  
# 
# All submitted images need to be PNGs.
#
# Functions:
#
# 1.- Encode:
#
# Submit two PNG images of the same size, both images most be PNGs.
# One of the images must be all-black (#000) and have the message written in
# bright red letters (#F00 recommended). This message is going to be encoded
# in the submitted picture. 
#
# A new file called "encoded_x.png" (where "x" is the original filename) will
# be saved in the current directory.
#
# 2.- Decode:
#
# Provide an image encoded (preferably) by this app to be decoded. This function
# operates in two modes: "B" which will return an image containing the message in
# bright red letters on a black brackgorund, and "T" which will return the message
# in bright red letters on top of the original image.
#
# A new file called "decoded_x.png" (where "x" is the original filename) will
# be saved in the current directory, the message in display according
# to the selected mode.
#
# 3.- Inspect
#
# Provide an image and get a printout of all the pixels' colors.
#
# 4.- Create black image
#
# Provide an image to receive an all black image of the same size. This makes
# it easier to create the image that contains the message in bright red letters.
#
# A new file called "black_x.png" (where "x" is the original filename) will be 
# saved in the current directory.
# 
# -Geada734

# This script runs on PIL.
from PIL import Image

# Opens a file to be turned black.
def black(imgName):
    try:
        img = Image.open(imgName, "r")
        makeItBlack(img)
    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        exit()

# Creates a black copy of an image.
def makeItBlack(img):
    x = 0
    y = 0
    w = img.size[0]
    h = img.size[1]

    # Copy of the original image.
    newImg = img.copy()

    # Iterates each pixel turning it black.
    for x in range (0, w):
        for y in range(0, h):
            newImg.putpixel((x,y), (0, 0, 0, 255))

    # Saves the image and shows it to the user.
    newImg.show()
    newImg.save("black_" + img.filename)   

# Opens an image to be inspected.
def inspect(imgName):
    try: 
        img = Image.open(imgName, "r")
        inspectImage(img)
    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        exit()

# Inspects the image.
def inspectImage(img):
    x = 0
    y = 0
    w = img.size[0]
    h = img.size[1]

    # Iterates over each pixel printing its color.
    for x in range(0,w):
        for y in range(0,h):
            pix = img.getpixel((x,y))
            
            if(pix[2]%2==1):
                print(pix)
    
    # Shows the image to the user.
    img.show()

# Formats the image containing the message to be used by the app.
def flattenCode(imgName):
    try: 
        img = Image.open(imgName, "r")
        flattenCodeImage(img)
    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        exit()

# Makes the image's balcks extra black.
def flattenCodeImage(img):
    x = 0
    y = 0
    w = img.size[0]
    h = img.size[1]

    # Copy of the orginal image.
    newImg = img.copy()

    # Iterates over each pixel to make the image usable by turning them black.
    for x in range(0,w):
        for y in range(0,h):
            if(img.getpixel((x,y))[0]==0):
                newImg.putpixel((x,y), (0,0,0,255))
    
    newImg.save("flatCode_"+img.filename)

# Formats the image where the message will be hidden to be used by the app.
def flatten(imgName):
    try: 
        img = Image.open(imgName, "r")
        flattenImage(img)
    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        exit()

# Makes sure the message can be encoded in the image.
def flattenImage(img):
    x = 0
    y = 0
    w = img.size[0]
    h = img.size[1]

    # Copy of the original image.
    newImg = img.copy()

    # Iterates over each pixel in the image to make their RGB value even.
    for x in range(0,w):
        for y in range(0,h):
            pix = list(img.getpixel((x,y)))
            red = pix[0]
            green = pix[1]
            blue = pix[2]

            # Since blue is the "B" in "RGB", that's the value we are making even.
            if(blue%2==1):
                blue = blue - 1
                newImg.putpixel((x,y), (red, green, blue, 255))

    newImg.save("flat_"+img.filename)

# Opens both images to encode the message.
def encode(coded, img):
    codedImg = Image.open(coded)
    image = Image.open(img)

    encodeImages(codedImg, image)

# Encodes the message inside the other image.
def encodeImages(coded, img):
    x = 0
    y = 0
    w = img.size[0]
    h = img.size[1]

    # Copy of the original image.
    newImg = img.copy()

    # Any red pixels on the black image are turned into odd pixels
    # on the original picture.
    for x in range(0, w):
        for y in range(0, h):
            if(coded.getpixel((x,y))[0]>0):
                pix = list(img.getpixel((x,y)))
                pix[2] = pix[2] + 1
                pix.append(255)
                newImg.putpixel((x,y), tuple(pix))

    # Saves the image and shows it to the user.
    newImg.show()
    newImg.save("encoded_" + img.filename.split("_")[1])

# Opens an image with an encoded message to be decoded.
def decode(img):
    try:
        i = Image.open(img)

        # Asks the user how do they want their decoded image to look like.
        mode = input("Would you like your message to be released on top of the original image (T) or" + " on top of a black background (B)?\n")
        if(mode=="B" or mode=="T"):
            decodeImage(i, mode)
        else:
            # Lets the user know the selected mode is not valid.
            print("Invalid mode.")
            exit()

    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        exit()

# Decodes an image with an encoded message.
def decodeImage(img, mode):
    x = 0
    y = 0
    w = img.size[0]
    h = img.size[1]

    # Copy of the original image.
    newImg = img.copy()

    # Iterate the image to look for odd pixels.
    for x in range(0,w):
        for y in range(0,h):
            pix = img.getpixel((x,y))

            if(pix[2]%2==1):
                # Odd pixels are turned red.
                newImg.putpixel((x,y), (255, 0, 0, 255))
            else:
                # If the mode is "B", even pixels are turned black.
                if(mode=="B"):
                    newImg.putpixel((x,y), (0, 0, 0, 255))

    # Saves the image and shows it to the user.
    newImg.show()
    newImg.save("decoded_" + img.filename)

def main():
    # Ask the user what they want to do.
    prompt = (input("Welcome to my awesome stenography machine!\n" + "Select one of the following:\n" +
    "1.- Encode\n2.- Decode\n3.- Inspect\n4.- Create black image\n"))

    if(prompt=="1"):
        coded = input("Input the filename of the image containing your message:\n")
        flattenCode(coded)
        img = input("Input the image you want to hide your message in:\n")
        flatten(img)
        encode("flatCode_" + coded, "flat_" + img)
        print("Your image has been encoded! The new filename is encoded_" + img + ".")
    elif(prompt=="2"):
        coded = input("Input the image that has the hidden message:\n")
        decode(coded)
        print("Your image has been decoded! The new filename is decoded_" + coded + ".")
    elif(prompt=="3"):
        img = input("Input the file to inspect:\n")
        inspect(img)
    elif(prompt=="4"):
        img = input("Input the file you want to create a black copy from:\n")
        black(img)
        print("Your black image has been created! The new filename is black_" + img + ".")
    else:
        # Lets the user know that's an invalid command.
        print("Input a valid command, please.")

if __name__ == "__main__":
    main() 
