# .encode() convierte el texto (str) en bytes (por defecto con UTF-8).
# XOR trabaja con números, así que necesitamos los bytes de cada carácter.
# Aquí cada carácter ASCII ocupa 1 byte, y "ATAQUE AL AMANECER" tiene 18.
mensaje = "ATAQUE AL AMANECER".encode()   # 18 bytes
# Igual con la clave: "CLAVE12345678901" tiene 16 caracteres = 16 bytes.
clave = "CLAVE12345678901".encode()      # 16 bytes
 
# El mensaje tiene 18 bytes y la clave 16: repetimos la clave hasta igualar la longitud
# XOR necesita un byte de clave por cada byte de mensaje. Paso a paso:
#   len(mensaje) // len(clave)  -> división entera: 18 // 16 = 1
#   ... + 1                     -> 2: cuántas veces repetir la clave para
#                                  asegurarnos de que llega (cubre el resto)
#   clave * 2                   -> en Python, multiplicar bytes los repite (32 bytes)
#   [:len(mensaje)]             -> "slicing": nos quedamos solo con los
#                                  primeros 18 bytes y descartamos el sobrante
clave = (clave * (len(mensaje) // len(clave) + 1))[:len(mensaje)]
 
 
# def define una función reutilizable; recibe los datos y la clave.
def xor(datos, clave):
    # Esto es un "docstring": texto que documenta qué hace la función.
    """XOR byte a byte entre datos y clave."""
    # zip(datos, clave) empareja el byte 1 de datos con el byte 1 de clave,
    # el 2 con el 2, etc. Al iterar bytes, Python da números enteros (0-255).
    # d ^ k aplica el XOR bit a bit entre ambos números.
    # bytes(...) vuelve a convertir la secuencia de números en un objeto bytes.
    return bytes(d ^ k for d, k in zip(datos, clave))
 
 
# Cifrar: aplicamos XOR entre el mensaje y la clave.
criptograma = xor(mensaje, clave)      # cifrar
# Descifrar: aplicamos XOR otra vez con la MISMA clave. Como (A ^ K) ^ K = A,
# recuperamos el mensaje original.
descifrado = xor(criptograma, clave)   # descifrar (la misma operación)
 
# .hex() muestra los bytes como texto hexadecimal (2 dígitos por byte),
# porque el criptograma contiene bytes no imprimibles y no se vería bien
# como texto normal.
print("Mensaje:    ", mensaje.hex())
print("Clave:      ", clave.hex())
print("Criptograma:", criptograma.hex())
# .decode() hace lo contrario de .encode(): convierte bytes en texto legible.
print("Descifrado: ", descifrado.decode())
# Comparamos el resultado con el mensaje original: debe dar True.
print("¿Coincide con el original?", descifrado == mensaje)
