#!/usr/bin/env python3

import sys
import argparse

import psycopg2

from decrypter import decrypt


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
    db_args_parser.add_argument('-c', '--command', default='dumpall', help='', choices=['dumpall', 'test', 'masterkey'])

    args = parser.parse_args()
    
    try:
        connection = psycopg2.connect(host=args.host, port=args.port, user=args.user, password=args.password, dbname=args.dbname)
    except:
        sys.exit('Failed to connect to PostgreSQL')

    try:
        if args.command == 'test':
            cur = connection.cursor()
            cur.execute("SELECT notesowner FROM Ptrx_NotesInfo WHERE noteid=1;")
            encoded_pmp, *_ = cur.fetchone()
            decrypted_pmp = decrypt(encoded_pmp, args.key)
            if decrypted_pmp == b'PMP':
                print('Success! You have the correct key!')
    except Exception as e:
        raise e
    finally:
        connection.close()


if __name__ == '__main__':
    cli()
