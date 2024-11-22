import cv2
import numpy as np

'''
5. Hiding IMAGE in IMAGE
This is similar to image stegonagraphy, but we replace the message with an image.

In encode, we first get the image to be encode and check wehther this is a valid image.
The number of the show image's pixels should be at least four times bigger than that of the image which we hide.
If the image is too big, then we can't encode it in the show image.
Then we extract the pixel value from the hide image to make a list.
We change the first pixel in the show image to be the size of the hide image.
And for other pixel, we change the last two bits of each r, g, b into the hide image's pixel vaule.
Output the final image. (Notice that it should be png file to preserve all the bits)

In decode, get the size of the hidden image from the first pixel of the show image
and initialize the hide image as a zero np array.
For other pixel, get the hiden image's pixel value from the last two bit.
Use these pixel value to construct the hidden image. (Each r, g, b = 8 bit of the pixel value)
Then output the hidden image.
'''

def rgb_to_bin(pixel):
    ret = []
    for i in pixel:
        ret.append(format(i, "08b"))
    return ret

def encode(hide_img_file, show_img_file, output_name):
    # input
    hide_img = cv2.imread(hide_img_file)
    show_img = cv2.imread(show_img_file)

    if(hide_img is None):
        print(f"There is no {hide_img} / cannot open {hide_img}")
        return False
    if(show_img is None):
        print(f"There is no {show_img} / cannot open {show_img}")
        return False
    
    # get the size of the img
    hide_w, hide_h, _ = hide_img.shape
    show_w, show_h, _ = show_img.shape
    if(hide_w * hide_h * 4 > show_w * show_h):
        print("The hidden image is too big, choose another image.")
        print(f"(The hidden image's pixel number should less than {show_w * show_h / 4})")
        return False
    
    # extract pixel value from the hidden image
    hide_pixel = ""
    for row in hide_img:
        for pixel in row:
            r, g, b = rgb_to_bin(pixel)
            hide_pixel += r + g + b
    
    # encode hide img into show img
    idx = 0
    for i in  range(show_w):
        for j in range(show_h):
            # the first pixel record the size of the hidden image
            if(i == 0 and j == 0):
                encode_w = bin(hide_w)[2:].zfill(12)
                encode_h = bin(hide_h)[2:].zfill(12)
                show_img[i][j][0] = int(encode_w[0:8], 2)
                show_img[i][j][1] = int(encode_w[8:12] + encode_h[0:4], 2)
                show_img[i][j][2] = int(encode_h[4:12], 2)
                
            else:
                r, g, b = rgb_to_bin(show_img[i][j])
                if(idx < len(hide_pixel)):
                    r = int(r[0:6] + hide_pixel[idx:idx+2], 2)
                    idx += 2
                if(idx < len(hide_pixel)):
                    g = int(g[0:6] + hide_pixel[idx:idx+2], 2)
                    idx += 2
                if(idx < len(hide_pixel)):
                    b = int(b[0:6] + hide_pixel[idx:idx+2], 2)
                    idx += 2

                show_img[i][j] = [r, g, b]

                if(idx >= len(hide_pixel)):
                    break   # break inner for loop

        if(idx >= len(hide_pixel)):
                    break   # break outer for loop

    # output
    cv2.imwrite(output_name, show_img)
    print(f"Finish Image in image steganography encode. Result image in {output_name}")
    return True

def decode(decode_file, output_name):
    show_img = cv2.imread(decode_file)
    if(show_img is None):
        print(f"There is no {show_img} / cannot open {show_img}")
        return False
    show_w, show_h, _ = show_img.shape

    # extract pixel value
    hide_pixel = ""
    for i in range(show_w):
        for j in range(show_h):
            if(i == 0 and j == 0):
                img_sz = bin(show_img[i][j][0])[2:].zfill(8) + bin(show_img[i][j][1])[2:].zfill(8) + bin(show_img[i][j][2])[2:].zfill(8)
                hide_w = int(img_sz[0:12], 2)
                hide_h = int(img_sz[12:24], 2)
                hide_img = np.zeros((hide_w, hide_h, 3), np.uint8)      # initialize the hiden img
            else:
                r, g, b = rgb_to_bin(show_img[i][j])
                hide_pixel += r[6:8] + g[6:8] + b[6:8]
            if(len(hide_pixel) >= hide_w * hide_h * 8 * 3):
                break       # break inner for loop
        if(len(hide_pixel) >= hide_w * hide_h * 8 * 3):
            break       # break outer for loop
    
    # construct hidden img
    idx = 0
    n = len(hide_pixel)
    for i in range(hide_w):
        for j in range(hide_h):
            if(idx < n): hide_img[i][j][0] = int(hide_pixel[idx:idx+8], 2)
            if(idx < n): hide_img[i][j][1] = int(hide_pixel[idx+8:idx+16], 2)
            if(idx < n): hide_img[i][j][2] = int(hide_pixel[idx+16:idx+24], 2)
            idx += 24

    # output
    cv2.imwrite(output_name, hide_img)
    print(f"Finish Image in image steganography decode. Result image in {output_name}")
    return True

if __name__ == "__main__":
    # img_in_img()
    hide_img_file = "hide_img.jpg"
    show_img_file = "ann.jpg"
    output_name = "a1.png"
    encode(hide_img_file, show_img_file, output_name)
    decode(output_name, "a2.png")