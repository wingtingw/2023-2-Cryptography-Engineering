import cv2
import numpy as np
import os

def msg_to_bin(msg):
    if type(msg) == str:
        msg = msg.encode('utf-8')
        ret = ""
        for byte in msg:
            ret += format(byte, "08b")
        return ret
    elif type(msg) == bytes or type(msg) == np.ndarray:
        ret = [format(i, "08b") for i in msg]
        return ret
    elif type(msg) == int or type(msg) == np.uint8:
        ret = format(msg, "08b")
        return ret

def frame_encode(frame, msg):
    if len(msg) == 0:
        raise ValueError('Data entered to be encoded is empty')

    msg += "!@#$%"
    bin_msg = msg_to_bin(msg)
    # print(f"Binary message to encode: {bin_msg}")
    idx = 0
    for row in frame:
        for pixel in row:
            if idx < len(bin_msg):
                pixel[0] = int(bin_msg[idx], 2)
                idx += 1
            if idx < len(bin_msg):
                pixel[1] = int(bin_msg[idx], 2)
                idx += 1
            if idx < len(bin_msg):
                pixel[2] = int(bin_msg[idx], 2)
                idx += 1
            if idx >= len(bin_msg):
                break
        if idx >= len(bin_msg):
            break
    return frame

def decode_vid_data(input_name):
    f = os.path.splitext(input_name)[0] + '.png'
    f = f.replace('files/', 'steganography/')
    frame = cv2.imread(f)
    bin_msg = ""
    for row in frame:
        for pixel in row:
            r, g, b = msg_to_bin(pixel)
            bin_msg += r[-1]
            bin_msg += g[-1]
            bin_msg += b[-1]
            total_byte = [bin_msg[i: i + 8] for i in range(0, len(bin_msg), 8)]
            char_msg = ""
            for byte in total_byte:
                try:
                    char_msg += chr(int(byte, 2))
                except ValueError:
                    pass
                if char_msg[-5:] == "!@#$%":
                    try:
                        decoded_msg = char_msg[:-5].encode('latin1').decode('utf-8')
                    except UnicodeDecodeError:
                        decoded_msg = char_msg[:-5]
                    print("The decoded msg is: ", decoded_msg)
                    return
    print("Can't decode the message ><")
    
    
def encode_vid_data(input_name, output_name, msg):
    vidcap = cv2.VideoCapture(input_name)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(output_name, fourcc, fps, (frame_width, frame_height))

    frame_number = 0
    while vidcap.isOpened():
        ret, frame = vidcap.read()
        if not ret:
            break
        if frame_number == 0:
            frame = frame_encode(frame, msg)
            input_name = os.path.splitext(output_name)[0] + '.png'
            input_name = input_name.replace('files/', 'steganography/') 
            cv2.imwrite(input_name, frame)           
        out.write(frame)
        frame_number += 1

    vidcap.release()
    out.release()
    cv2.destroyAllWindows()
'''
def decode_vid_data(input_name):
    vidcap = cv2.VideoCapture(input_name)
    frame_number = 0
    while vidcap.isOpened():
        ret, frame = vidcap.read()
        if not ret:
            break
        if frame_number == 0:
            frame_decode(frame)
            break
        frame_number += 1

    vidcap.release()
'''
def vid_steg():
    a = int(input())
    input_name = input()
    output_name = input()
    msg = input()
    if a == 1:
        encode_vid_data(input_name, output_name, msg)
        print("1")
    if a == 2:
        decode_vid_data(input_name)
        print("2")
        
def encode(msg, input_name, output_name):
    encode_vid_data(input_name, output_name, msg)
    
def decode(input_name):
    decode_vid_data(input_name)
    
if __name__ == "__main__":
    vid_steg()
