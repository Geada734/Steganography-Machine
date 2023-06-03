# Stegonography-Machine

Magical steganography machine usage:

This script encodes a message contained in an image inside
another image using the PIL library for Python.

All submitted images need to be multi-layer PNGs.

Functions:

1.- Encode:

Submit two PNG images of the same size, both images most be PNGs.
One of the images must be all-black and have the message written in
bright letters or lines. This message is going to be encoded
in the submitted picture.

A new file called "encoded_x.png" (where "x" is the original filename) will
be saved in the current directory.

2.- Decode:

Provide an image encoded (preferably) by this app to be decoded. This function
operates in two modes: "B" which will return an image containing the message in
bright red letters on a black brackgorund, and "T" which will return the message
in bright red letters on top of the original image.

A new file called "decoded_x.png" (where "x" is the original filename) will
be saved in the current directory, the message in display according
to the selected mode.

3.- Inspect

Provide an image and get a printout of all the pixels' colors.

4.- Create black image

Provide an image to receive an all black image of the same size. This makes
it easier to create the image that contains the message in bright red letters.

A new file called "black_x.png" (where "x" is the original filename) will be
saved in the current directory.
