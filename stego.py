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
from stegonosaurus import stego_functions as sf

def get_path_and_name(filename):
    '''Separates the filename from the path'''
    path_list = filename.split("/")
    name = path_list.pop()

    path = ""

    if len(path_list)>0:
        path = "/".join(path_list) + "/"

    return [name, path]

def black(img_name):
    '''Opens a file to be turned black.'''
    try:
        validate_format(img_name)
        img = Image.open(img_name, "r")
        validate_image(img)

        new_img = sf.blacken(img)
        new_path_data = get_path_and_name(img.filename)

        new_img.show()
        new_img.save(new_path_data[1] + "black_" + new_path_data[0])

        img.close()
        new_img.close()

        return new_path_data

    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        sys.exit()

def inspect(img_name):
    '''Opens an image to be inspected.'''
    try:
        validate_format(img_name)

        img = Image.open(img_name, "r")

        validate_image(img)
        print(sf.inspect(img))
        img.show()

        img.close()

        sys.exit()

    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        sys.exit()

def encode(coded, img_name):
    '''Opens both images to encode the message.'''
    try:
        validate_format(coded)
        validate_format(img_name)

        coded_img = Image.open(coded)
        img = Image.open(img_name)

        validate_image(coded_img)
        validate_image(img)
        validate_image_sizes(coded_img, img)

        new_img = sf.encode(coded_img, img)
        new_path_data = get_path_and_name(img_name)

        # Saves the image and shows it to the user.
        new_img.show()
        new_img.save(new_path_data[1] + "encoded_" + new_path_data[0])

        coded_img.close()
        img.close()
        new_img.close()

        return new_path_data
    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        sys.exit()

def decode(img_name):
    '''Opens an image with an encoded message to be decoded.'''
    try:
        validate_format(img_name)
        img = Image.open(img_name)
        validate_image(img)

        # Asks the user how do they want their decoded image to look like.
        mode = input("Would you like your message to be released on top of the original image (T)" +
        " or on top of a black background (B)?\n")
        if mode.lower()=="b" or mode.lower()=="t":
            new_img = sf.decode(img, mode)
            new_path_data = get_path_and_name(img.filename)

            # Saves the image and shows it to the user.
            new_img.show()
            new_img.save(new_path_data[1]+"decoded_"+new_path_data[0])

            img.close()
            new_img.close()

            return new_path_data
        else:
            # Lets the user know the selected mode is not valid.
            print("Invalid mode.")
            sys.exit()

    except FileNotFoundError:
        # Lets the user know there's no such file in the current directory.
        print("File not found.")
        sys.exit()

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

def validate_image(img):
    '''Validates that the file is a multilayer .png image.'''
    if(img.mode != "RGB" and img.mode != "RGBA"):
        img.close()
        print("Image is not multi-band")
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
        coded.close()
        img.close()

        print("Make sure the image that contains the message is smaller than the template.")
        sys.exit()

def main():
    '''Main method'''
    user_input = ""
    options = {
        "encode": "1",
        "decode": "2",
        "inspect": "3",
        "black": "4"
    }

    # Checks if there were any arguments when running the app.
    if len(sys.argv)>1:
        try:
            user_input = options[sys.argv[1].lower()]
        except KeyError:
            print("Input a valid command, please.")
            sys.exit()
    else:
        # Prompts the user for imput if not.
        prompt = (input("Welcome to my awesome stenography machine!\n" +
        "Select one of the following:\n" +
        "1.- Encode\n2.- Decode\n3.- Inspect\n4.- Create black image\n" +
        "5.- Exit\n"))
        user_input = prompt

    # Acts on user input.
    if user_input=="1":
        coded = ""

        # Checks for filenames in the input.
        if len(sys.argv)>2:
            coded = sys.argv[2]
        else:
            coded = input("Input the filename of the image containing your message:\n")

        img = ""

        if len(sys.argv)>3:
            img = sys.argv[3]
        else:
            img = input("Input the image you want to hide your message in:\n")

        # Simplifying the name and path of the images to flatten.
        # Can't believe PIL won't differentiate between filename and path.
        new_path_data = encode(coded, img)

        # Change the message on whether the file is stored at the same
        # dir as the script or not.
        if len(new_path_data[1])>0:
            print("Your image has been encoded at " + new_path_data[1] +
            "! The new filename is encoded_" + new_path_data[0] + ".")
        else:
            print("Your image has been encoded! The new filename is encoded_" +
                  new_path_data[0] + ".")

    elif user_input=="2":
        coded = ""

        # Checks for filenames in the input.
        if len(sys.argv)>2:
            coded = sys.argv[2]
        else:
            coded = input("Input the image that has the hidden message:\n")

        new_path_data = decode(coded)

        # Change the message on whether the file is stored at the same
        # dir as the script or not.
        if len(new_path_data[1])>0:
            print("Your image has been decoded at "+ new_path_data[1] +
            "! The new filename is decoded_" + new_path_data[0]+ ".")
        else:
            print("Your image has been decoded! The new filename is decoded_" +
            new_path_data[0]+ ".")

    elif user_input=="3":
        img = ""

        # Checks for filenames in the input.
        if len(sys.argv)>2:
            img = sys.argv[2]
        else:
            img = input("Input the file to inspect:\n")

        inspect(img)
    elif user_input=="4":
        img = ""

        # Checks for filenames in the input.
        if len(sys.argv)>2:
            img = sys.argv[2]
        else:
            img = input("Input the file you want to create a black copy from:\n")

        new_path_data = black(img)

        # Change the message on whether the file is stored at the same
        # dir as the script or not.
        if len(new_path_data[1])>0:
            print("Your black image has been created at " + new_path_data[1] +
            "! The new filename is black_" + new_path_data[0] + ".")
        else:
            print("Your black image has been created at! The new filename is black_" +
            new_path_data[0] + ".")

    elif user_input=="5":
        sys.exit()
    else:
        # Lets the user know that's an invalid command.
        print("Input a valid command, please.")

if __name__ == "__main__":
    main()
