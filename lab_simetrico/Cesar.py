# Importamos dos cosas de la librería "langdetect" (hay que instalarla con
# `pip install langdetect`):
#   - detect: función que recibe un texto y devuelve el código del idioma
#             detectado ("es" = español, "en" = inglés, "fr" = francés...).
#   - DetectorFactory: clase que permite configurar el detector.
from langdetect import detect, DetectorFactory
 
# langdetect usa un algoritmo con algo de aleatoriedad, así que dos
# ejecuciones podrían dar resultados distintos en textos cortos.
# Fijando la "semilla" (seed) a 0 hacemos que el resultado sea siempre el mismo.
DetectorFactory.seed = 0  # para que el resultado sea siempre el mismo
 
# Este es el criptograma: el mensaje cifrado que queremos descifrar.
mensaje = "Uunejvxb dw vdwmx wdnex jzdr, nw wdnbcaxb lxajixwnb"
 
# Probamos las 26 claves posibles
# range(26) genera los números 0, 1, 2, ..., 25. En cada vuelta del bucle,
# "clave" vale uno de esos desplazamientos posibles.
for clave in range(26):
    # Empezamos con una cadena vacía donde iremos construyendo el texto
    # descifrado con la clave que estamos probando.
    resultado = ""
 
    # Recorremos el mensaje carácter a carácter ("letra" puede ser una
    # letra, un espacio, una coma...).
    for letra in mensaje:
        # .isalpha() devuelve True si el carácter es una letra.
        # Solo desplazamos letras; el resto (espacios, comas) se deja igual.
        if letra.isalpha():
            # ord() convierte un carácter a su código numérico (ASCII/Unicode):
            #   ord("A") = 65 y ord("a") = 97.
            # Necesitamos la "base" para convertir la letra en un número 0-25.
            # Si la letra es mayúscula la base es la de "A"; si no, la de "a".
            # Así se conserva la mayúscula/minúscula original.
            base = ord("A") if letra.isupper() else ord("a")
 
            # Esta línea es el descifrado en sí. Paso a paso:
            #   ord(letra) - base      -> posición de la letra en el alfabeto (0-25)
            #   ... - clave            -> deshacemos el desplazamiento del cifrado
            #   ... % 26               -> el módulo hace que "dé la vuelta" al
            #                             alfabeto (si sale -3, pasa a 23; en
            #                             Python el % con negativos da positivo)
            #   ... + base             -> volvemos a un código de letra real
            #   chr(...)               -> convierte el código en el carácter
            #                             (es lo contrario de ord)
            # Y con += lo añadimos al final del texto que llevamos descifrado.
            resultado += chr((ord(letra) - base - clave) % 26 + base)
        else:
            # Si no es letra, la copiamos tal cual.
            resultado += letra  # espacios y signos no se tocan
 
    # Nos quedamos con el que esté en español
    # detect(resultado) analiza el texto candidato y devuelve el idioma.
    # Si es "es", lo más probable es que hayamos acertado con la clave.
    # Con claves incorrectas el texto sale como galimatías y no se detecta
    # como español.
    if detect(resultado) == "es":
        # Mostramos la clave que ha funcionado...
        print("Clave:", clave)
        # ...y el mensaje descifrado correspondiente.
        print("Mensaje:", resultado)


