import hashlib
from tkinter import *
from tkinter import filedialog
import math
import random
import sympy
import pathlib

root = Tk()
root.title("DSA assignment")
root.geometry("700x800")

name = ""
content = ""
hash = ""

e = ""
d = ""
n = 0

content_verify = ""
name_verify = ""

content_sign = ""
name_sign = ""

key_pub = ""
key_prv = ""
content_key_pub = ""
content_key_prv = ""


# function for opening file dialog
def openFD():
    root.filename = filedialog.askopenfilename(initialdir=r"C:\Users\Ayman\PycharmProjects\pythonProject", title="select a file",filetypes=(("all files", "*.*") ,("text files", "*.txt")))
    source = root.filename
    return source


# function for opening the file we want to sign and get its info
def openSrc():
    global name
    global content
    src = openFD()
    with open(src) as f:
        content = f.read()
        lbl_name01.config(text=pathlib.Path(src).name)
        lbl_type01.config(text=pathlib.Path(src).suffix)
        lbl_location01.config(text=src)
        lbl_size01.config(text=f"{pathlib.Path(src).stat().st_size} bytes")
        name = f.name


# function for opening the data file for verification
def openDF():
    global content_verify, name_verify, ct01
    src = openFD()
    with open(src) as f:
        content_verify = f.read()
        lbl_name02.config(text=pathlib.Path(src).name)
        name_verify = f.name


# function for opening the signature file for verification
def openSign():
    global content_sign, name_sign
    src = openFD()
    with open(src) as f:
        content_sign = f.read().splitlines()
        lbl_name04.config(text=pathlib.Path(src).name)
        name_sign = f.name


# function for opening keys, doesn't matter if user makes mistake opening wrong file, function knows
def openKey():
    global key_pub, key_prv, content_key_pub, content_key_prv
    src = openFD()
    if src.lower().endswith((".pub")):
        with open(src) as f:
            content_key_pub = f.read().splitlines()
            lbl_pubKey02.config(text=content_key_pub)
            key_pub = f.name
        return True
    elif src.lower().endswith((".priv")):
        with open(src) as f:
            content_key_prv = f.read().splitlines()
            lbl_prvKey02.config(text=content_key_prv)
            key_prv = f.name
        return True
    else:
        return False


# function for opening public key
def openKeyPub():
    bool01 = openKey()
    if bool01 == False:
        lbl_pubKey02.config(text="the file you have chosen is not a key")


# function for opening private key
def openKeyprv():
    bool01 = openKey()
    if bool01 == False:
        lbl_prvKey02.config(text="the file you have chosen is not a key")


# function for generating and saving keys
def generateKeys():
    global e, d, n

    p = 0
    q = 0
    while p == q:
        p = sympy.randprime(1000000000000000, 9999999999999999)
        q = sympy.randprime(1000000000000000, 9999999999999999)

    n = p * q
    pn = (p - 1) * (q - 1)

    while True:
        e = random.randint(1, pn)
        result = math.gcd(e, pn)
        if result == 1:
            break

    d = pow(e, -1, pn)

    lbl_publicK02.config(text = f"{e}, {n}")
    lbl_privateK02.config(text = f"{d}, {n}")

    with open("public.pub", 'w') as pb:
        pb.write(f"{e}\n{n}")

    with open("private.priv", 'w') as pv:
        pv.write(f"{d}\n{n}")


# function for generating the hash of the chosen source file
def generateHash():
    global name
    global content
    global hash
    if len(name) > 0 and len(content) > 0:
        m = hashlib.new("sha3_512", content.encode())
        hash = m.hexdigest()
        lbl_hash02.config(text = f"{hash}")
    else:
        lbl_hash02.config(text="choose file first")


# function for signing the file and saving it
def signFile():
    global name
    global content
    global hash
    global e, d, n

    if len(name) > 0 and len(content) > 0 and len(hash) > 0 and n != 0:
        rows = math.ceil(len(hash) / 7)
        arr = [["0" for i in range(7)] for j in range(rows)]

        l = 0

        for i in range(len(arr)):
            for j in range(7):
                if l < len(hash):
                    arr[i][j] = hash[l]
                    l += 1
                else:
                    arr[i][j] = " "

        for i in range(len(arr)):
            for j in range(7):
                arr[i][j] = ord(arr[i][j])

        for i in range(len(arr)):
            for j in range(7):
                arr[i][j] = format(arr[i][j], "b")

        temp02 = ["" for i in range(rows)]

        for i in range(len(arr)):
            for j in range(7):
                temp01 = ["0" for i in range(10)]
                for k in range(len(arr[i][j])):
                    temp01[len(temp01) - 1 - k] = arr[i][j][-1 * (k + 1)]
                temp_str = "".join(temp01)
                temp02[i] += temp_str
            temp02[i] = int(temp02[i], 2)

        ct = ["" for i in range(rows)]

        for i in range(len(temp02)):
            ct[i] = pow(temp02[i], e, n)

        with open("sign.sign", 'w') as fs:
            for i in range(len(ct)):
                fs.write(f"{ct[i]}\n")

        lbl_sign.config(text = "file signed and saved")

    else:
        lbl_sign.config(text="one of the above steps missing: browsing/generating keys/ hashing")

    e = ""
    d = ""
    n = ""


# function for verifying if the two hashes match
def verify():
    global name_verify, content_verify, content_sign, name_sign

    if len(name_verify) > 0 and len(name_verify) > 0:
        m = hashlib.new("sha3_512", content_verify.encode())
        hash = m.hexdigest()
        lbl_dataHash02.config(text=f"{hash}")
    else:
        lbl_dataHash02.config(text="please choose data file")

    n01 = int(content_key_pub[1])
    d01 = int(content_key_prv[0])

    if len(name_sign) > 0 and len(content_sign) > 0:
        ot = ["" for i in range(len(content_sign))]

        for i in range(len(content_sign)):
            ot[i] = pow(int(content_sign[i]), d01, n01)
            ot[i] = format(ot[i], "b")

        for i in range(len(ot)):
            ot[i] = ((70 - len(ot[i])) * "0") + ot[i]

        final_string = ""

        for i in range(len(ot)):
            temp03 = ["" for i in range(7)]

            for j in range(len(ot[i])):
                if j < 10:
                    temp03[0] += ot[i][j]
                if j >= 10 and j < 20:
                    temp03[1] += ot[i][j]
                if j >= 20 and j < 30:
                    temp03[2] += ot[i][j]
                if j >= 30 and j < 40:
                    temp03[3] += ot[i][j]
                if j >= 40 and j < 50:
                    temp03[4] += ot[i][j]
                if j >= 50 and j < 60:
                    temp03[5] += ot[i][j]
                if j >= 60 and j < 70:
                    temp03[6] += ot[i][j]

            for k in range(len(temp03)):
                temp03[k] = int(temp03[k], 2)
                temp03[k] = chr(temp03[k])

            final_string += "".join(temp03)

        lbl_signHash02.config(text = f"{final_string}")

    else:
        lbl_signHash02.config(text="please choose signature file")

    if hash.strip() == final_string.strip():
        lbl_verify.config(text="the hash of both files match")
    else:
        lbl_verify.config(text="the hash of the two files do not match")





# all the widgets
btn_brows = Button(root, text = "brows", command=openSrc)
lbl_name = Label(root, text = "name: ")
lbl_type = Label(root, text = "type: ")
lbl_location = Label(root, text = "location: ")
lbl_size = Label(root, text = "size: ")

lbl_name01 = Label(root, text = " ")
lbl_type01 = Label(root, text = " ")
lbl_location01 = Label(root, text = " ")
lbl_size01 = Label(root, text = " ")

lbl_break01 = Label(root, text = " -----------------------         key generating ")
lbl_break02 = Label(root, text = " ----------------------------------------- ")

btn_generate = Button(root, text = "generate keys", command = generateKeys)
lbl_publicK01 = Label(root, text = "the public key: ")
lbl_publicK02 = Label(root, text = " ")
lbl_privateK01 = Label(root, text = "the private key: ")
lbl_privateK02 = Label(root, text = " ")

lbl_break03 = Label(root, text = " --------------------        hashing and signing ")
lbl_break04 = Label(root, text = " ----------------------------------------- ")

btn_hash = Button(root, text = "generate hash", command = generateHash)
lbl_hash01 = Label(root, text = "hash: ")
lbl_hash02 = Label(root, text = " ")
btn_sign = Button(root, text = "sign file", command = signFile)
lbl_sign = Label(root, text = " ")

lbl_break05 = Label(root, text = " -----------------------         verification ")
lbl_break06 = Label(root, text = " ----------------------------------------- ")

btn_brows01 = Button(root, text = "brows data file", command=openDF)
btn_brows02 = Button(root, text = "brows sign file", command=openSign)


lbl_name02 = Label(root, text = "name: ")
lbl_name04 = Label(root, text = "name: ")
lbl_type02 = Label(root, text = "type: ")
lbl_location02 = Label(root, text = "location: ")
lbl_size02 = Label(root, text = "size: ")

lbl_name03 = Label(root, text = " ")
lbl_type03 = Label(root, text = " ")
lbl_location03 = Label(root, text = " ")
lbl_size03 = Label(root, text = " ")

btn_loadPubKey = Button(root, text = "load public key", command = openKeyPub)
btn_loadPrvKey = Button(root, text = "load private key", command = openKeyprv)
lbl_pubKey01 = Label(root, text = "public key: ")
lbl_pubKey02 = Label(root, text = "please open public key")
lbl_prvKey01 = Label(root, text = "private key: ")
lbl_prvKey02 = Label(root, text = "please open private key")

btn_verify = Button(root, text = "verify", command = verify)
lbl_dataHash01 = Label(root, text = "data hash: ")
lbl_dataHash02 = Label(root, text = "please choose data file")
lbl_signHash01 = Label(root, text = "sign hash: ")
lbl_signHash02 = Label(root, text = "please choose signature file")
lbl_verify = Label(root, text = " ")


# putting the widgets on the root
btn_brows.grid(row = 0, column = 0, padx = 10, pady = 5)
lbl_name.grid(row = 1, column = 0, padx = 10, pady = 5)
lbl_type.grid(row = 2, column = 0, padx = 10, pady = 5)
lbl_location.grid(row = 3, column = 0, padx = 10, pady = 5)
lbl_size.grid(row = 4, column = 0, padx = 10, pady = 5)
lbl_name01.grid(row = 1, column = 1, padx = 10, pady = 5)
lbl_type01.grid(row = 2, column = 1, padx = 10, pady = 5)
lbl_location01.grid(row = 3, column = 1, padx = 10, pady = 5)
lbl_size01.grid(row = 4, column = 1, padx = 10, pady = 5)
lbl_break01.grid(row = 5, column = 0, padx = 5, pady = 5)
lbl_break02.grid(row = 5, column = 1, padx = 5, pady = 5)
btn_generate.grid(row = 6, column = 0, padx = 10, pady = 5)
lbl_publicK01.grid(row = 7, column = 0, padx = 10, pady = 5)
lbl_publicK02.grid(row = 7, column = 1, padx = 10, pady = 5)
lbl_privateK01.grid(row = 8, column = 0, padx = 10, pady = 5)
lbl_privateK02.grid(row = 8, column = 1, padx = 10, pady = 5)
lbl_break03.grid(row = 9, column = 0, padx = 5, pady = 5)
lbl_break04.grid(row = 9, column = 1, padx = 5, pady = 5)
btn_hash.grid(row = 10, column = 0, padx = 10, pady = 5)
lbl_hash01.grid(row = 11, column = 0, padx = 10, pady = 5)
lbl_hash02.grid(row = 11, column = 1, padx = 10, pady = 5)
btn_sign.grid(row = 12, column = 0, padx = 10, pady = 5)
lbl_sign.grid(row = 12, column = 1, padx = 10, pady = 5)
lbl_break05.grid(row = 13, column = 0, padx = 5, pady = 5)
lbl_break06.grid(row = 13, column = 1, padx = 5, pady = 5)
btn_brows01.grid(row = 14, column = 0, padx = 10, pady = 5)
lbl_name02.grid(row = 14, column = 1, padx = 10, pady = 5)
#lbl_type02.grid(row = 16, column = 0, padx = 10, pady = 5)
#lbl_location02.grid(row = 17, column = 0, padx = 10, pady = 5)
#lbl_size02.grid(row = 18, column = 0, padx = 10, pady = 5)
btn_brows02.grid(row = 15, column = 0, padx = 10, pady = 5)
lbl_name04.grid(row = 15, column = 1, padx = 10, pady = 5)
#lbl_type03.grid(row = 16, column = 1, padx = 10, pady = 5)
#lbl_location03.grid(row = 17, column = 1, padx = 10, pady = 5)
#lbl_size03.grid(row = 18, column = 1, padx = 10, pady = 5)
btn_loadPubKey.grid(row = 19, column = 0, padx = 10, pady = 5)
btn_loadPrvKey.grid(row = 19, column = 1, padx = 10, pady = 5)
lbl_pubKey01.grid(row = 20, column = 0, padx = 10, pady = 5)
lbl_pubKey02.grid(row = 20, column = 1, padx = 10, pady = 5)
lbl_prvKey01.grid(row = 21, column = 0, padx = 10, pady = 5)
lbl_prvKey02.grid(row = 21, column = 1, padx = 10, pady = 5)
btn_verify.grid(row = 22, column = 0, padx = 10, pady = 5)
lbl_dataHash01.grid(row = 23, column = 0, padx = 10, pady = 5)
lbl_dataHash02.grid(row = 23, column = 1, padx = 10, pady = 5)
lbl_signHash01.grid(row = 24, column = 0, padx = 10, pady = 5)
lbl_signHash02.grid(row = 24, column = 1, padx = 10, pady = 5)
lbl_verify.grid(row = 25, column = 0, padx = 10, pady = 5)



root.mainloop()