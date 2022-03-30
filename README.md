# AE3KR-task03-DSAcipher

## task description

* Loading the file for signing (fileDialog)
* Showing the file info in the application -> like file name, path to the file, type (extension), file 
size, etc.
* Signing the file -> hashing and encryption with private key using your previously made RSA 
cipher.
* Verifying the signed file (digital sign verifying) -> here to use public key
* Generating the key pair for RSA with possibility to save public/private key in the files -> files 
with extension .pub and .priv
* GUI with only using fileDialogs and buttons and outputs -> no inputs are necessary … For 
loading keys should be used files .priv and .pub
More details:
* Digital sign should be file with extension .sign (output of hash function encrypted by private 
key and using RSA). File .sign should contains following data:
RSA_SHA3-512 DIGITAL_SIGN_IN_BASE64. (for example "RSA_SHA3-512
QWhvaiBQZXBvLCBqYWsgc2UgbcOhxaEgPw==")
* For verifying the user need to load .sing file + public key file .pub + original file
* Key pair file .pub and .priv should contain data as following: 
RSA PRIVATE_KEY_IN_BASE64.
RSA PUBLIC_KEY_IN_BASE64
