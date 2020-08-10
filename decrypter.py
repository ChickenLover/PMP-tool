#!/usr/bin/env python3

import csv
import sys
import base64
import hashlib
import argparse

from Crypto.Cipher import AES
import Crypto.Util.Counter as Counter

try:
    import pgpy
except:
    print('Warning: no "pgpy" module is installed, decrypting database encrypted data won\'t work! Install it with `pip3 install pgpy`')


def decrypt(ciphertext, key):
    key = base64.b64decode(key).ljust(32, b' ').decode('utf-8', 'replace').encode() # Don't ask...
    c_bytes = base64.b64decode(ciphertext)
    iv, ctext = c_bytes[:16], c_bytes[16:]
    pbkdf2_key = hashlib.pbkdf2_hmac("sha1", key, b"\x01\x02\x03\x04\x05\x06\x07\x08", 1024, dklen=32)
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, 'big'))
    cipher = AES.new(pbkdf2_key, AES.MODE_CTR, counter=ctr)
    return cipher.decrypt(ctext)


def db_decrypt(ciphertext, key):
    if 'pgpy' not in sys.modules:
        raise Exception('No "pgpy" module is installed, decrypting database encrypted data won\'t work! Install it with `pip3 install pgpy`')

    c_bytes = base64.b64decode(ciphertext)
    message = pgpy.PGPMessage.from_blob(c_bytes)
    return message.decrypt(key).message


def cli():
    parser = argparse.ArgumentParser(description='Password Manager Pro decrypter')
    parser.add_argument('-k', '--key', required=True,
                        help='PMP key (base64). You can find it in the PMP/conf/pmp_key.conf' )
    parser.add_argument('-m', '--masterkey',
                        help='Database encryption key (base64). Can be found in Ptrx_NotesInfo, column NOTE_DESCRIPTION')
    parser.add_argument('--cleanmaster', help='Decrypted database encryption key')
    parser.add_argument('--encrypted', action='store_true', help='Pass it if your passwords are database-encrypted')
    parser.add_argument('-f', '--file', help='Path to a file with encrypted passwords (each starting with a newline)')
    parser.add_argument('-p', '--password', help='A single database-encrypted password to decrypt (base64)')
    parser.add_argument('-c', '--ciphertext', help='A single ciphertext to decrypt (base64)')
    args = parser.parse_args()

    if not any([args.file, args.ciphertext, args.password]):
        sys.exit('Please provie either --file or --ciphertext or --password')
    args.key = args.key.replace('\\', '').replace('ENCRYPTIONKEY=', '')
    if not args.cleanmaster and args.masterkey:
        try:
            args.cleanmaster = decrypt(args.masterkey, args.key).decode()
        except:
            sys.exit('Can\'t decrypt master key using provided PMP key!')

    if args.password:
        if args.encrypted:
            args.password = db_decrypt(args.password, args.cleanmaster)
        plainpasswd = decrypt(args.password, args.key)
        print(plainpasswd)
    elif args.ciphertext:
        plaintext = decrypt(args.ciphertext)
        print(plaintext)
    elif args.file:
        try:
            encrypted_passwords = [x for x in open(args.file).read().split('\n') if x]
        except:
            sys.exit(f'No such file! {args.file}')
        with open('plainpasswords.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['ciphertext', 'plaintext'])
            for passwd in encrypted_passwords:
                if args.encrypted:
                    passwd = db_decrypt(passwd, args.cleanmaster)
                try:
                    plain_passwd = decrypt(passwd, args.key).decode()
                    print(f'{passwd} decrypted! Password is - {plain_passwd}')
                except: 
                    print(f'Can\'t decode {passwd}! -_0_0_-')
                    plain_passwd = ''
                writer.writerow([passwd, plain_passwd])
        print('results were written in plainpasswords.csv!')


if __name__ == '__main__':
    cli()
