import jwt

data_to_encode = {"some": "payload"}
encryptioin_secret = "secrete"
algorithm = "HS256"


## eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.KXd7QE-GVKXdMF3Gqxo40CVe8nQYCzoxUhD_QL6rUNE
encode = jwt.encode(data_to_encode, encryptioin_secret, algorithm=algorithm)

## {'some': 'payload'}
decode = jwt.decode(encode, encryptioin_secret, algorithms=[algorithm])
print(decode)
