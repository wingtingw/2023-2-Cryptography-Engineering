'''
2. Text Steganography ( Hiding TEXT in TEXT )
Use zero-width characters (ZWC) to hide the message in the text.

For the encode part, we first convert the msg into binary and add "11111111" in the end to detect end of msg.
And then encode the message into the text.
We have four ZWCs, so we encode two bit msg as one ZWC. ZWC = {"00":u'\u200C',"01":u'\u202C',"11":u'\u202D',"10":u'\u200E'}
Add the ZWC after each word in the text.
That is, every word in the text will follow by four ZWC representing one msg word.
After all the msg has been encoded in the text, write the remaning text into the output file, then we are done.

For the decode part, we go through every character in the text,
if the character is a ZWC, then record its binary bits to the binary message.
When we read "11111111", meaning we reach the end of the message.
Convert the binary msg into character and print the result.
'''
def encode(msg, cover_file_name, output_name):
    # start encode
    cover_file = open(cover_file_name, "r", encoding='utf-8')
    new_f = open(output_name, "w+", encoding="utf-8")

    # 1. make sure the msg is not too long to encode
    txt = []
    for line in cover_file:
        txt += line.split()

    n_word = len(txt)
    
    # one msg word will be encoded into 4 word, so we need len(msg)*4 <= n_word
    if(len(msg)*4 > n_word):
        print(f"msg length = {len(msg)}, but txt can only encode {int(n_word/4)} words.")
        return False
    
    # 2. msg to binary
    idx = 0
    bin_msg = ""
    while idx < len(msg):
        ch = ord(msg[idx])
        bin_msg += bin(ch)[2:].zfill(8)   # bin(ch) = 0b10101010, so use [2:] to remove '0b'
        idx += 1
    bin_msg += "11111111"                 # to detect the end of the msg when decoding

    # 3. encode and write to the new file
    ZWC = {"00":u'\u200C',"01":u'\u202C',"11":u'\u202D',"10":u'\u200E'}     # a map to convert two bit binary to zero-width characters
    idx = 0
    while(idx < len(bin_msg)):
        word = txt[int(idx/8)]
        j = 0
        tmp = ""
        while(j<8):
            tt = bin_msg[idx+j] + bin_msg[idx+j+1]
            tmp += ZWC[tt]
            j += 2
        new_word = word + tmp + " "
        new_f.write(new_word)
        idx += 8

    # 4. msg has been encoded in the file, write the remaining text to the new file
    idx = int(len(bin_msg)/8)
    while(idx < len(txt)):
        new_f.write(txt[idx])
        new_f.write(" ")
        idx += 1

    # finish
    cover_file.close(), new_f.close()
    print(f"Finish text steganography encode. Result text in {output_name}")
    return True

def decode(decode_file):
    txt = open(decode_file, "r", encoding="utf-8")
    reverse_ZWC={u'\u200C':"00",u'\u202C':"01",u'\u202D':"11",u'\u200E':"10"}

    # get binary message
    bin_msg = ""
    for line in txt:
        for word in line.split():
            tmp = ""
            for ch in word:
                if(ch in reverse_ZWC):
                    tmp += reverse_ZWC[ch]
            if tmp == "11111111":
                break
            else:
                bin_msg += tmp

    # convert binary back to string
    res = ""
    idx = 0
    while(idx < len(bin_msg)):
        dec_ch = int(bin_msg[idx:idx+8], 2)
        res += chr(dec_ch)
        idx += 8
    
    # output
    print("The decoded msg is: ", res)
    return True

if __name__ == "__main__":
    # txt_steg()
    msg = "this is the message."
    cover_file = "cover_txt.txt"
    output_name = "new_txt.txt"
    encode(msg, cover_file, output_name)
    decode(output_name)