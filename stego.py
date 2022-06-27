'''This script runs on PIL.'''
# Magical stegonography machine usage:
#
# This script encodes a message contained in an image inside
# another image using the PIL libary for Python.
#
# All submitted images need to be multi-layer PNGs.
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

import sys
from PIL import Image

def black(img_name):
    '''Opens a file to be turned black.'''
    try:
        validate_format(img_name)
        img = Image.open(img_name, "r")
        validate_multilayer(img)
        make_it_black(img)
    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        sys.exit()

def make_it_black(img):
    '''Creates a black copy of an image.'''
    pix_x = 0
    pix_y = 0
    width = img.size[0]
    height = img.size[1]

    # Copy of the original image.
    new_img = img.copy()

    # Iterates each pixel turning it black.
    for pix_x in range (0, width):
        for pix_y in range(0, height):
            new_img.putpixel((pix_x, pix_y), (0, 0, 0, 255))

    # Saves the image and shows it to the user.
    new_img.show()
    new_img.save("black_" + img.filename)

def inspect(img_name):
    '''Opens an image to be inspected.'''
    try:
        validate_format(img_name)
        img = Image.open(img_name, "r")
        validate_multilayer(img)
        inspect_image(img)

    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        sys.exit()

def inspect_image(img):
    '''Inspects the image.'''
    pix_x = 0
    pix_y = 0
    width = img.size[0]
    height = img.size[1]

    # Iterates over each pixel printing its color.
    for pix_x in range(0, width):
        for pix_y in range(0, height):
            pix = img.getpixel((pix_x, pix_y))

            if pix[2]%2==1:
                print(pix)

    # Shows the image to the user.
    img.show()

def flatten_code(img_name):
    '''Formats the image containing the message to be used by the app.'''
    try:
        validate_format(img_name)
        img = Image.open(img_name, "r")
        validate_multilayer(img)
        flatten_code_image(img)

    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        sys.exit()

def flatten_code_image(img):
    '''Makes the image's balcks extra black.'''
    pix_x = 0
    pix_y = 0
    width = img.size[0]
    height = img.size[1]

    # Copy of the orginal image.
    new_img = img.copy()

    # Iterates over each pixel to make the image usable by turning them black.
    for pix_x in range(0, width):
        for pix_y in range(0, height):
            if img.getpixel((pix_x,pix_y))[0]==0:
                new_img.putpixel((pix_x, pix_y), (0, 0, 0, 255))

    new_img.save("flatCode_"+img.filename)

def flatten(img_name):
    '''Formats the image where the message will be hidden to be used by the app.'''
    try:
        validate_format(img_name)
        img = Image.open(img_name, "r")
        validate_multilayer(img)
        flatten_image(img)
    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        sys.exit()

def flatten_image(img):
    '''Makes sure the message can be encoded in the image.'''
    pix_x = 0
    pix_y = 0
    width = img.size[0]
    height = img.size[1]

    # Copy of the original image.
    new_img = img.copy()

    # Iterates over each pixel in the image to make their RGB value even.
    for pix_x in range(0, width):
        for pix_y in range(0, height):
            pix = list(img.getpixel((pix_x, pix_y)))
            red = pix[0]
            green = pix[1]
            blue = pix[2]

            # Since blue is the "B" in "RGB", that's the value we are making even.
            if blue%2==1:
                blue = blue - 1
                new_img.putpixel((pix_x, pix_y), (red, green, blue, 255))

    new_img.save("flat_"+img.filename)

def encode(coded, img_name):
    '''Opens both images to encode the message.'''
    coded_img = Image.open(coded)
    img = Image.open(img_name)

    validate_multilayer(coded_img)
    validate_multilayer(img)
    validate_image_sizes(coded_img, img)

    encode_images(coded_img, img)

def encode_images(coded, img):
    '''Encodes the message inside the other image.'''
    pix_x = 0
    pix_y = 0
    width = coded.size[0]
    height = coded.size[1]

    # Copy of the original image.
    new_img = img.copy()

    # Any red pixels on the black image are turned into odd pixels
    # on the original picture.
    for pix_x in range(0, width):
        for pix_y in range(0, height):
            if coded.getpixel((pix_x, pix_y))[0]>0:
                pix = list(img.getpixel((pix_x, pix_y)))
                pix[2] = pix[2] + 1
                pix.append(255)
                new_img.putpixel((pix_x, pix_y), tuple(pix))

    # Saves the image and shows it to the user.
    new_img.show()
    new_img.save("encoded_" + img.filename.split("_")[1])

def decode(img_name):
    '''Opens an image with an encoded message to be decoded.'''
    try:
        validate_format(img_name)
        img = Image.open(img_name)
        validate_multilayer(img)

        # Asks the user how do they want their decoded image to look like.
        mode = input("Would you like your message to be released on top of the original image (T)" +
        " or on top of a black background (B)?\n")
        if mode.lower()=="b" or mode.lower()=="t":
            decode_image(img, mode)
        else:
            # Lets the user know the selected mode is not valid.
            print("Invalid mode.")
            sys.exit()

    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        sys.exit()

def decode_image(img, mode):
    '''Decodes an image with an encoded message.'''
    pix_x = 0
    pix_y = 0
    width = img.size[0]
    height = img.size[1]

    # Copy of the original image.
    new_img = img.copy()

    # Iterate the image to look for odd pixels.
    for pix_x in range(0, width):
        for pix_y in range(0, height):
            pix = img.getpixel((pix_x, pix_y))

            if pix[2]%2==1:
                # Odd pixels are turned red.
                new_img.putpixel((pix_x, pix_y), (255, 0, 0, 255))
            else:
                # If the mode is "B", even pixels are turned black.
                if mode.lower()=="b":
                    new_img.putpixel((pix_x, pix_y), (0, 0, 0, 255))

    # Saves the image and shows it to the user.
    new_img.show()
    new_img.save("decoded_" + img.filename)

def validate_format(img):
    '''Validates that the files provided are .png images.'''
    img_components = img.split(".")

    if len(img_components) == 2:
        if img_components[1].lower() != "png":
            print("Invalid file format.")
            sys.exit()
    else:
        print("Invalid file format.")
        sys.exit()

def validate_multilayer(img):
    '''Validates that the file is a multilayer .png image.'''
    pix0 = img.getpixel((0, 0))

    # Checks if the first pixel is a tuple.
    if not isinstance(pix0, tuple):
        # Lets the user know the image is not multi-layer.
        print("Image is not multi-layer")
        sys.exit()

def validate_image_sizes(coded, img):
    '''Validates that the image with the coded message is smaller than the template
    image.
    '''
    coded_x = coded.size[0]
    coded_y = coded.size[1]
    img_x = img.size[0]
    img_y = img.size[1]

    if coded_x>img_x or coded_y>img_y:
        print("Make sure the image that contains the message is smaller than the template.")
        sys.exit()

def main():
    '''Main method'''
    prompt = (input("Welcome to my awesome stenography machine!\n" +
    "Select one of the following:\n" +
    "1.- Encode\n2.- Decode\n3.- Inspect\n4.- Create black image\n"))

    if prompt=="1":
        coded = input("Input the filename of the image containing your message:\n")
        flatten_code(coded)
        img = input("Input the image you want to hide your message in:\n")
        flatten(img)
        encode("flatCode_" + coded, "flat_" + img)
        print("Your image has been encoded! The new filename is encoded_" + img + ".")
    elif prompt=="2":
        coded = input("Input the image that has the hidden message:\n")
        decode(coded)
        print("Your image has been decoded! The new filename is decoded_" + coded + ".")
    elif prompt=="3":
        img = input("Input the file to inspect:\n")
        inspect(img)
    elif prompt=="4":
        img = input("Input the file you want to create a black copy from:\n")
        black(img)
        print("Your black image has been created! The new filename is black_" + img + ".")
    else:
        # Lets the user know that's an invalid command.
        print("Input a valid command, please.")

if __name__ == "__main__":
    main()
