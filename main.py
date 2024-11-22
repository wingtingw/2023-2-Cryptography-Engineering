import os
import steganography as steg

def EXIT():
    print("\n好啊都這樣啊你就離開啊都不要理我啊\n")
    os._exit(0)
    
def BACK():
    print("\nGO BACK GO BACK")
    return
  
def check_file_valid(file_format, file_path):
    dic = {2 : "text", 3: "image", 4 : "audio", 5 : "video"}
    f_dic = {2: ".txt", 3 : ".png", 4 : ".wav", 5: ".mp4"}
    _, file_extension = os.path.splitext(file_path)
    if (os.path.exists(file_path)):
        if (file_extension == f_dic[file_format]):
            return True
        else:
            print(f"Wrong file name, please enter the {dic[file_format]} file name.")
            return False
    else:
        print("File not found, please enter again.")
        return False
    
def check_encode(success):
    if (success):
        return True
    else:
        print("Encryption failed, please try to encode again.")
        return False

def check_decode(succes):
    if (succes):
        return True
    else:
        print("Decryption failed, please try to decode again.")

def encode_mode():
    dic = {2: "text", 3: "image", 4: "audio", 5: "video"}
    f_dic = {2: ".txt", 3: ".png", 4: ".wav", 5: ".mp4"}
    file_folder = "files"
    while(True):
        print("\n--- Encode ---")
        print("1. Typing\n2. Text File\n3. Image File\n4. Audio File\n5. Video File\n6. BACK\n7. EXIT")
        while(True):
            message_format = int(input("Select the secret message format: "))
            if (message_format == 1):           
                text_message = input("Enter the message you want to encode: ")
                break
            elif (message_format >= 2 and message_format <= 5):
                while(True):
                    message_file_name = input(f"Enter the {dic[message_format]} file name you want to encode: ")
                    message_file_path = os.path.join(file_folder, message_file_name)
                    if (check_file_valid(message_format, message_file_path)):
                        break
                break
            elif (message_format == 6):
                BACK()
                return
            elif (message_format == 7):
                EXIT()
                break
            else:
                print("Invalid option, please enter again.")
                continue

        while(True):    
            cover_file_format = int(input("Select the cover file format: "))
            if (cover_file_format == 1):
                print("Can not hide message in typing format, please select other format.")
                continue
            elif (cover_file_format >= 2 and cover_file_format <= 5):
                while(True):
                    cover_file_name = input(f"Enter the cover {dic[cover_file_format]} file name: ")
                    cover_file_path = os.path.join(file_folder, cover_file_name)
                    if (check_file_valid(cover_file_format, cover_file_path)):
                        break
                break
            elif (cover_file_format == 6):
                BACK()
                return
            elif (cover_file_format == 7):
                EXIT()
                break
            else:
                print("Invalid option, please enter again.")
                continue
        
        while (True):
            encode_file_name = input(f"Enter the encoded {dic[cover_file_format]} file name you want: ")
            _, file_extension = os.path.splitext(encode_file_name)
            if (file_extension == f_dic[cover_file_format]):
                encode_file_path = os.path.join(file_folder, encode_file_name)
                break
            else:
                print(f"Wrong file name, please enter the {dic[cover_file_format]} file name.")

        #encode
        print("\nEncoding...")
        
        if (message_format == 1 and cover_file_format == 2):
            if (check_encode(steg.typ_to_txt.encode(text_message, cover_file_path, encode_file_path))):
                return
            else:
                continue
        elif (message_format == 1 and cover_file_format == 3):
            if (check_encode(steg.typ_to_img.encode(text_message, cover_file_path, encode_file_path))):
                return
            else:
                continue 
        elif (message_format == 1 and cover_file_format == 4):
            if (check_encode(steg.typ_to_aud.encode(text_message, cover_file_path, encode_file_path))):
                return
            else:
                continue
        elif (message_format == 2 and cover_file_format == 2):
            if (check_encode(steg.txt_to_txt.encode(message_file_path, cover_file_path, encode_file_path))):
                return
            else:
                continue
        elif (message_format == 2 and cover_file_format == 3):
            if (check_encode(steg.txt_to_img.encode(message_file_path, cover_file_path, encode_file_path))):
                return
            else:
                continue
        elif (message_format == 2 and cover_file_format == 4):
            if (check_encode(steg.txt_to_aud.encode(message_file_path, cover_file_path, encode_file_path))):
                return
            else:
                continue
        elif (message_format == 3 and cover_file_format == 3):
            if (check_encode(steg.img_to_img.encode(message_file_path, cover_file_path, encode_file_path))):
                return
            else:
                continue
        elif (message_format == 1 and cover_file_format == 5):
            if (check_encode(steg.typ_to_vid.encode(text_message, cover_file_path, encode_file_path))): 
                return
            else:
                continue
        else:
            print("\nNot implemented yet =D")
            
        
def decode_mode():
    dic = {2: "text", 3: "image", 4: "audio", 5: "video"}
    f_dic = {2: ".txt", 3: ".png", 4: ".wav", 5: ".mp4"}
    file_folder = "files"
    while(True):
        print("\n--- Decode Mode ---")
        print("1. Typing\n2. Text File\n3. Image File\n4. Audio File\n5. Video File\n6. BACK\n7. EXIT")
        while(True):
            decode_file_format = int(input("Select the cover file format you want to decode: "))
            if (decode_file_format == 1):
                print("Can not decode typing format, please select other format.")
                continue
            elif (decode_file_format >= 2 and decode_file_format <= 5):
                while(True):
                    decode_file_name = input(f"Enter the {dic[decode_file_format]} file name you want to decode: ")
                    decode_file_path = os.path.join(file_folder, decode_file_name)
                    if (check_file_valid(decode_file_format, decode_file_path)):
                        break
                break
            elif (decode_file_format == 6):
                BACK()
                return
            elif (decode_file_format == 7):
                EXIT()
                break
            else:
                print("Invalid option, please enter again.")
                continue

        while(True):    
            secret_file_format = int(input("Select the secret message format: "))
            if (secret_file_format == 1):
                break
            elif (secret_file_format >= 2 and secret_file_format <= 5):
                while(True):
                    secret_file_name = input(f"Enter the secret {dic[secret_file_format]} file name you want: ")
                    _, file_extension = os.path.splitext(secret_file_name)
                    if (file_extension == f_dic[secret_file_format]):
                        secret_file_path = os.path.join(file_folder, secret_file_name)
                        break
                    else:
                        print(f"Wrong file name, please enter the {dic[secret_file_format]} file name.")
                break
            elif (secret_file_format == 6):
                BACK()
                return
            elif (secret_file_format == 7):
                EXIT()
                break
            else:
                print("Invalid option, please enter again.")
                continue
    
        #decode
        print("\nDecoding...")
        
        if (decode_file_format == 2 and secret_file_format == 1):
            if (check_decode(steg.typ_to_txt.decode(decode_file_path))):
                return
            else:
                continue
        elif (decode_file_format == 2 and secret_file_format == 2):
            if (check_decode(steg.txt_to_txt.decode(decode_file_path, secret_file_path))):
                return
            else:
                continue
        elif (decode_file_format == 3 and secret_file_format == 1):
            if (check_decode(steg.typ_to_img.decode(decode_file_path))):
                return
            else:
                continue
        elif (decode_file_format == 3 and secret_file_format == 2):
            if (check_decode(steg.txt_to_img.decode(decode_file_path, secret_file_path))):
                return
            else:
                continue
        elif (decode_file_format == 3 and secret_file_format == 3):
            if (check_decode(steg.img_to_img.decode(decode_file_path, secret_file_path))):
                return
            else:
                continue
        elif (decode_file_format == 4 and secret_file_format == 1):
            if (check_decode(steg.typ_to_aud.decode(decode_file_path))):
                return
            else:
                continue
        elif (decode_file_format == 4 and secret_file_format == 2):
            if (check_decode(steg.txt_to_aud.decode(decode_file_path, secret_file_path))):
                return
            else:
                continue
        elif (decode_file_format == 5 and secret_file_format == 1):
            if (check_decode(steg.typ_to_vid.decode(decode_file_path))):
                return
            else:
                continue
        else:
            print("\nNot implemented yet =D")

            
if __name__ == '__main__':
    while(True):
        print("\n--- Steganography Tool ---")
        print("1. Encode\n2. Decode\n3. EXIT")
        option = int(input("Please select the mode: "))
    
        if (option == 1):
            encode_mode()
            continue
        elif (option == 2):
            decode_mode()
            continue
        elif (option == 3):
            EXIT()
            break
        else:
            print("\nInvalid option, please enter again.\n")
            continue
        
        
        
'''
1. typing
2. text
3. image
4. audio
5. video

1-2 O encode input: string, cover file name, new file name / decode input: decode file name
1-3 O encode input: string, cover file name, new file name / decode input: decode file name
1-4 O encode input: string, cover file name, new file name / decode input: decode file name
1-5 O encode input: string, cover file name, new file name / decode input: decode file name
2-2 * encode input: text file name, cover file name, new file name / decode input: decode file name, secret file name
2-3 * encode input: text file name, cover file name, new file name / decode input: decode file name, secret file name
2-4 * encode input: text file name, cover file name, new file name / decode input: decode file name, secret file name
2-5 * encode input: text file name, cover file name, new file name / decode input: decode file name, secret file name
3-2 可能太大
3-3 O encode input: image file name, cover file name, new file name / decode input: decode file name, secret file name
3-4 好白癡
3-5 O encode input: image file name, cover file name, new file name / decode input: decode file name, secret file name
4-2 太大
4-3 好白癡
4-4 .
4-5 .
5-2 太大
5-3 太大
5-4 太大
5-5 可能很久

txt_to_img


'''


#https://github.com/Priyansh-15/Steganography-Tools?fbclid=IwZXh0bgNhZW0CMTAAAR0SQsN3BIlUjsIuCC7FRZ533vc_9KOxGV5Uwe6VP3BgnF7OSdQBwtvP-NQ_aem_AbxmkJoKvJbq1_On0l0yDsQKD4DAgWirDl_K3TguM1dXHu-LNNoY5LIOadzsdOzZd72DbKqLShXxdaWB98mpsLkQ