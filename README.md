# PMP-tool

Some tools for decrypting/dumping Password Manager Pro passwords  

Dependencies:
 - python3
 - pycryptodome
 - pgpy (Only if you wish to decrypt database encrypted data)


## Decrypter

### Examples

Decrypt passwords from file:

```bash
./decrypter.py -k 7mNUUU+qQa9f6FMGRDCwllpdz/+Nf/1ahvEgj75FX/4\= --file example/decrypted_passwords.txt
```

Decrypt database-encrypted passwords from file:

```bash
./decrypter.py -k 7mNUUU+qQa9f6FMGRDCwllpdz/+Nf/1ahvEgj75FX/4\= -m xm6C2pZAC/yCcAxW6lQOUEgbb732ue99BjO9wu0f1tg= --file example/passwords.txt --encrypted
```

Decrypt a single database-encrypted password:

```bash
./decrypter.py -k 7mNUUU+qQa9f6FMGRDCwllpdz/+Nf/1ahvEgj75FX/4\= -m xm6C2pZAC/yCcAxW6lQOUEgbb732ue99BjO9wu0f1tg= --password wwwECQECsR/EjgtjwlTSUQFN8qQRmKRB0manYvU++KDTurezkOX5QwcrZEMdHLdTbAm1M2qHTUmB8LE5MZ5wDxtpzBR73p02ifya3QY5nVL/0y05/CSyEl7E+BoxrUn8+g== --encrypted
```

## Dumper

TO-DO

## PostgreSQL

You can use this commands (or their MySQL equivalent) to gain some info manually

To get encrypted `DB_ENCRYPTION_KEY` (you can than decrypt it with decrypter):

```SQL
select notesdescription from Ptrx_NotesInfo where noteid = 1;
```

To retrieve encrypted passwords (no database decryption):

```SQL
select encode(password, 'base64') from ptrx_passbasedauthen;
```


To retrieve encrypted passwords:

```SQL
select decryptschar(password, <DB_ENCRYPTION_KEY>) from ptrx_passbasedauthen;
```

OR

```SQL
select pgp_sym_decrypt(password, <DB_ENCRYPTION_KEY>, 's2k-mode=1, cipher-algo=aes256') from ptrx_passbasedauthen;
```
