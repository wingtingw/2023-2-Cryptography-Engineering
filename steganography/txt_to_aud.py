import wave

'''
3. Audio Stegonagraphy ( Hiding TEXT in AUDIO )
This is similar to image stegonagraphy.
Audio can be represented as .wav file, which store the audio as bytes.

In aud_encode, we read the cover audio file and transform it to a byte list.
For the message, we add "!@#$%" in the end to detect the end of it.
When doing encoding, we check each audio byte and message bit.
If the message bit and the audio's fourth LSB bit are the same,
then make the audio's second LSB bit to be 0 by AND with 253(11111101).
Otherwise, make the second LSB of the audio byte to be 1 (audio & 253 | 2),
and the last LSB to be the same as the message bit (audio & 254 | msg).

In aud_decode, we go through each byte in the audio.
If the second LSB = 0, it means that the fourth LSB is equal to the msg.
Otherwise, the msg bit is the last LSB.
Converting the binary message to string.
If we detect "!@#$%", then we are done. Output the decode message.
'''

def encode(txt_file, cover_file, output_name):
    # prepare the cover audio file
    f = open(txt_file, "r", encoding='utf-8')
    msg = f.read().replace('\n', '')
    f.close()
    song = wave.open(cover_file, mode = 'rb')
    nframes = song.getnframes()
    frames = song.readframes(nframes)
    frame_list = list(frames)
    frame_byte = bytearray(frame_list)

    msg += "!@#$%"  # end of the message

    # convert msg to binary bit list
    bin_msg = []
    for ch in msg:
        byte = format(ord(ch), "08b")
        for b in byte:
            bin_msg.append(int(b))

    # encode
    j = 0
    for i in range(0, len(bin_msg)):
        b = bin(frame_byte[j])[2:].zfill(8)
        if(b[len(b)-4] == bin_msg[i]):
            frame_byte[j] = frame_byte[j] & 253                 # 253 = 11111101, make the second LSB = 0
        else:
            frame_byte[j] = (frame_byte[j] & 253) | 2           # make the second LSB = 1
            frame_byte[j] = (frame_byte[j] & 254) | bin_msg[i]  # make the last LSB = msg
        j += 1

    # output
    new_frame = bytes(frame_byte)
    with wave.open(output_name, 'wb') as f:
        f.setparams(song.getparams())
        f.writeframes(new_frame)

    song.close()
    print(f"Finish audio steganography encode. Result audio in {output_name}")
    return True

def decode(decode_file, output_file_name):
    song = wave.open(decode_file, "rb")
    nframes = song.getnframes()
    frames = song.readframes(nframes)
    frame_list = list(frames)
    frame_byte = bytearray(frame_list)

    bin_msg = ""
    for i in range(len(frame_byte)):
        b = bin(frame_byte[i])[2:].zfill(8)
        if(b[len(b)-2]==0):     # b[len(b)-4] == bin_msg[i]
            bin_msg += b[len(b)-4]
        else:
            bin_msg += b[len(b)-1]

        total_byte = [bin_msg[i:i+8] for i in range(0, len(bin_msg), 8)]
        char_msg = ""
        for byte in total_byte:
            char_msg += chr(int(byte, 2))
            if(char_msg[-5:] == "!@#$%"):
                # output
                with open(output_file_name, "w", encoding='utf-8') as f:
                    f.write(char_msg[:-5])
                return True

if __name__ == "__main__":
    msg_file = "t.txt"
    cover_file = "cover_audio.wav"
    output_name = "new_audio.wav"
    encode(msg_file, cover_file, output_name)
    decode(output_name)