from backend.generate import generate_keys
from backend.message import *

if __name__ == '__main__':
    private_key_info, public_key_info = generate_keys('name', 'email', 'RSA', 1024, 'passphrase')

    private_key_info1, public_key_info1 = generate_keys('name', 'email', 'RSA', 1024, 'passphrase')
    
    msgBuilder1 = SendMessageBuilder('text', 'a', 'aleksa')
    msgBuilder1.sign(private_key=private_key_info['private_key'], password='passphrase', private_key_id=private_key_info['key_id'], private_key_algorithm=private_key_info['algorithm'])
    msgBuilder1.zip()
    msgBuilder1.encrypt('DES3', public_key_info['public_key'], public_key_info['key_id'], public_key_info['algorithm'])
    msgBuilder1.to_base64()

    msg = msgBuilder1.build()

    with open('plain.msg', "wb") as file:
        file.write(msg)

    print(msg)

    msgReceiver1 = ReceiveMsgBuilder(msg)

    if msgReceiver1.is_base64():
        msgReceiver1.decode_base64()
    if msgReceiver1.is_encripted():
        print('Encription key ' + str(msgReceiver1.get_encription_key_id()))
        msgReceiver1.decrypt(private_key_info['private_key'], 'passphrase')
        print(msgReceiver1.build())
    if msgReceiver1.check_zip():
        msgReceiver1.unzip()
    if msgReceiver1.is_signed():
        key_id = msgReceiver1.get_signature_key_id()
        print(key_id)
        if msgReceiver1.verify_signature(public_key_info['public_key']):
            print('Dobar potpis')
        else:
            print('Los potpis')
        msgReceiver1.remove_signature()

    msg1 = msgReceiver1.build()
    print(msg1)