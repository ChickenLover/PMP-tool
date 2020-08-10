#!/usr/bin/env python3

import argparse

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
    db_args_parser.add_argument('-d', '--database', default='PassTrix', help='PostgreSQL PassTrix database')
    db_args_parser.add_argument('-c', '--command', default='dumpall', help='')

    args = parser.parse_args()


if __name__ == '__main__':
    cli()
