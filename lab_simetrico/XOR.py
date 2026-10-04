mensaje = "ATAQUE AL AMANECER".encode()   # 18 bytes
clave = "CLAVE12345678901".encode()      # 16 bytes
 
# El mensaje tiene 18 bytes y la clave 16: repetimos la clave hasta igualar la longitud
clave = (clave * (len(mensaje) // len(clave) + 1))[:len(mensaje)]
 
 
def xor(datos, clave):
    """XOR byte a byte entre datos y clave."""
    return bytes(d ^ k for d, k in zip(datos, clave))
 
 
criptograma = xor(mensaje, clave)      # cifrar
descifrado = xor(criptograma, clave)   # descifrar (la misma operación)
 
print("Mensaje:    ", mensaje.hex())
print("Clave:      ", clave.hex())
print("Criptograma:", criptograma.hex())
print("Descifrado: ", descifrado.decode())
print("¿Coincide con el original?", descifrado == mensaje)
