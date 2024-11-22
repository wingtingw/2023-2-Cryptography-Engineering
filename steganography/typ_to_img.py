import cv2
import numpy as np

'''
Convert string / byte / int / np.ndarray / np.uint8 into binary.
'''
def msg_to_bin(msg):
    if type(msg) == str:
        ret = ""
        for ch in msg:
            ret += format(ord(ch), "08b")
            # ret.join(format(ord(ch), "08b"))
        return ret
    elif type(msg) == bytes or type(msg) == np.ndarray: # img[row][pixel] is np.ndarray
        ret = []
        for i in msg:
            ret.append(format(i, "08b"))
        return ret
    elif type(msg) == int or type(msg) == np.uint8:     # img[row][pixel][0] is np.uint8
        ret = format(msg, "08b")
        return ret

'''
1. Image Steganography ( Hiding TEXT in IMAGE )
Use Least Significant Bit Insertion to implement image steganography.

In img_encode, we add "!@#$%" in the end of the message to detect the end of the message when decoing,
and then convert the message into binary ASCII code.
In the image, we change the last bit of each pixel's r, g, b into the binary message.
Output the final image as .png file.
If we output as .jpg, some pixel value may change because .jpg is designed to reduce the file size,
but this will make us not able to decode the message, so we have to save it as .png file.

For img_decode, we go through every pixel in the image and get the last bit of r, g, b.
Convert the binary message into string.
If the last five character is "!@#$%", then we are done.
'''
def encode(msg, cover_file, output_name):
    img = cv2.imread(cover_file)
    n_img_byte = img.shape[0] * img.shape[1] * 3    # *3 because there are r,g,b
    if(len(msg)>n_img_byte):
        print(f"msg length = {len(msg)}, but img only {n_img_byte} bytes")
        return False
    
    # encode to img
    msg += "!@#$%"  # to detect the end of the msg when decoding
    bin_msg = msg_to_bin(msg)
    idx = 0
    for row in img:
        for pixel in row:
            r, g, b = msg_to_bin(pixel)
            if idx < len(bin_msg):
                pixel[0] = int(r[:-1] + bin_msg[idx], 2)
                idx+=1
            if idx < len(bin_msg):
                pixel[1] = int(g[:-1] + bin_msg[idx], 2)
                idx+=1
            if idx < len(bin_msg):
                pixel[2] = int(b[:-1] + bin_msg[idx], 2)
                idx+=1
            if idx >=len(bin_msg):
                break
        if idx >= len(bin_msg): break
    # output
    cv2.imwrite(output_name, img)
    print(f"Finish image steganography encode. Result image in {output_name}")
    return True

def decode(decode_file):
    img = cv2.imread(decode_file)
    bin_msg = ""
    for row in img:
        for pixel in row:
            r, g, b = msg_to_bin(pixel)
            bin_msg += r[-1]
            bin_msg += g[-1]
            bin_msg += b[-1]
            total_byte = [bin_msg[i: i+8] for i in range(0, len(bin_msg), 8)]
            char_msg = ""
            for byte in total_byte:
                char_msg += chr(int(byte, 2))
                if(char_msg[-5:] == "!@#$%"):
                    try:
                        decoded_msg = char_msg[:-5].encode('latin1').decode('utf-8')
                    except UnicodeDecodeError:
                        decoded_msg = char_msg[:-5]
                    print("The decoded msg is: ", decoded_msg)
                    print()
                    return True
    print("Can't decode the message ><")
    return False

if __name__ == "__main__":
    # img_steg()
    msg = "wing ting"
    img = "ann.jpg"
    output_name = "new_img.png"
    encode(msg, img, output_name)
    decode(output_name)