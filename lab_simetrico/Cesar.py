from langdetect import detect, DetectorFactory
 
DetectorFactory.seed = 0  # para que el resultado sea siempre el mismo
 
mensaje = "Uunejvxb dw vdwmx wdnex jzdr, nw wdnbcaxb lxajixwnb"
 
# Probamos las 26 claves posibles
for clave in range(26):
    resultado = ""
    for letra in mensaje:
        if letra.isalpha():
            base = ord("A") if letra.isupper() else ord("a")
            resultado += chr((ord(letra) - base - clave) % 26 + base)
        else:
            resultado += letra  # espacios y signos no se tocan
 
    # Nos quedamos con el que esté en español
    if detect(resultado) == "es":
        print("Clave:", clave)
        print("Mensaje:", resultado)

