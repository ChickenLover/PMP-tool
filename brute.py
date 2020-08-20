#!/usr/bin/env python3

import sys

from decrypter import decrypt



if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('Please provide encrypted pmp and a path to a list of keys. Example: `./brute.py 6ogdyCmR1U/MYMJnQJCVNa21HOKzo9oNVR4CnME9S3E= keys.txt`')
    ENC_PMP = sys.argv[1]
    KEY_FILE = sys.argv[2]

    with open(KEY_FILE) as f:
        keys = [x for x in f.read().split('\n') if x]
        for key in keys:
            try:
                dec = decrypt(ENC_PMP, key)
                if dec == b'PMP':
                    print(f'"{key}", should do it!')
            except:
                pass
