import jks

keystore = jks.KeyStore.load('../keystore.jks', 'practica3')

print(keystore.private_keys)


