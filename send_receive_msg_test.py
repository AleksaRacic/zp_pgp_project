from backend.generate import generate_keys
from backend.message import *

if __name__ == '__main__':
    private_key_info, public_key_info = generate_keys('name', 'email', 'RSA', 1024, 'passphrase')

    private_key_info1, public_key_info1 = generate_keys('name', 'email', 'RSA', 1024, 'passphrase')

    msgBuilder = SendMessageBuilder('text', 'a')

    msgBuilder.sign(private_key=private_key_info['private_key'], password='passphrase', private_key_id=private_key_info['key_id'], private_key_algorithm=private_key_info['algorithm'])
    
    samo_potpisana_poruka = msgBuilder.build()

    msgBuilder.zip()

    zip_potpis_poruka = msgBuilder.build()

    received_samo_potpisana = ReceiveMsgBuilder(samo_potpisana_poruka)

    if received_samo_potpisana.check_zip():
        received_samo_potpisana.unzip()
    if received_samo_potpisana.is_signed():
        key_id = received_samo_potpisana.get_signature_key_id()
        print(key_id)
        if received_samo_potpisana.verify_signature(public_key_info['public_key']):
            print('Dobar potpis')
        else:
            print('Los potpis')
        
        print('Proveravam los potpis')
        if received_samo_potpisana.verify_signature(public_key_info1['public_key']):
            print('Dobar potpis')
        else:
            print('Los potpis')

    print()
    print()
    print('zzip i potpis')
    received_zip_potpis_poruka = ReceiveMsgBuilder(zip_potpis_poruka)
    if received_zip_potpis_poruka.check_zip():
        received_zip_potpis_poruka.unzip()
    if received_zip_potpis_poruka.is_signed():
        key_id = received_zip_potpis_poruka.get_signature_key_id()
        print(key_id)
        if received_zip_potpis_poruka.verify_signature(public_key_info['public_key']):
            print('Dobar potpis')
        else:
            print('Los potpis')

    
    msgBuilder1 = SendMessageBuilder('text', 'a')

    msgBuilder1.encrypt('DES3', public_key_info['public_key'], public_key_info['key_id'], public_key_info['algorithm'])

    msg = msgBuilder1.build()

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